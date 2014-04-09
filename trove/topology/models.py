#    Copyright 2014 Rackspace Hosting
#    All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Model classes that form the core of Topology functionality
"""

import json
from trove.common import exception
from trove.db import models
from trove.openstack.common.gettextutils import _
from trove.openstack.common import log as logging

LOG = logging.getLogger(__name__)


def persisted_models():
    return {'instance_topologies': DBTopologies}


class DBTopologies(models.DatabaseModelBase):
    _data_fields = ['id', 'instance_id', 'datastore', 'topology', 'created',
                    'updated', 'deleted', 'deleted_at']
    preserve_on_delete = False
    _table_name = 'instance_topologies'


class Topology(object):
    def __init__(self, context, instance_id, topology_entry=None, **kwargs):
        """
        Create an instance of Topology.  This represents a row within
        the topology table for a given instance.

        This class should not be called directly, rather use the Topologies
        model class and act upon topologies as a dictionary.
        """
        datastore = kwargs.get('datastore')
        topology = kwargs.get('topology')

        if topology_entry:
            # A pre-instantiated topology entry was passed in, favor this.
            self.topology_entry = topology_entry
        elif context and instance_id and datastore and not topology:
            # We have everything we need to find an entry in the database
            self.topology_entry = DBTopologies.find_by(
                context=context, instance_id=instance_id, datastore=datastore)
            # if not isinstance(self.topology_entry, DBTopologies):
            #     raise Exception('OH NOES, Im not a DBTopologies: %s' %
            #                     type(self.topology_entry))
        elif context and instance_id and datastore and topology:
            # Last chance, create a new one
            self.topology_entry = DBTopologies.create(context=context,
                                                      datastore=datastore,
                                                      topology=json.dumps(
                                                          topology),
                                                      instance_id=instance_id)
            self.save()
        else:
            # Nowhere else to go, gotta raise
            raise exception.TopologyModelError(model_name=Topology.__name__)

    @property
    def datastore(self):
        return self.topology_entry.datastore

    @property
    def topology(self):
        return json.loads(self.topology_entry.topology)

    def __getitem__(self, item):
        return self.topology_entry[item]

    def save(self):
        self.topology_entry.save()

    def delete(self):
        self.topology_entry.delete()

    def set_datastore(self, datastore):
        self.topology.datastore = datastore
        self.save()

    def set_topology(self, topology):
        self.topology_entry.topology = json.dumps(topology)
        self.save()

    def copy(self):
        return {
            self.datastore: self.topology
        }


class Topologies(object):
    def __init__(self, context, instance_id):
        """
        Create an instance of Topologies.  This represents the topology of a
        given trove instance.

        This satisfies the dictionary interface to keep interacting with
        the topology simple.
        """
        self.context = context
        self.instance_id = instance_id
        self._load_topologies()

    def _load_topologies(self):
        """
        Helper method for refreshing topology from the database.  This is
        called at instantiation and anytime topology is added to the instance.
        """
        # NOTE(imsplitbit): if this becomes too expensive of an operation we
        # can break it out into 2 methods.  One for when instantiation happens
        # and one for just loading the newly created topology entries into
        # the self.topologies list.  Ideally this would only contain one or two
        # topologies for a given datastore and this is done with a key based
        # SELECT so it should be an extremely fast operation.
        if self.context:
            self.topologies = DBTopologies.find_all(
                instance_id=self.instance_id, deleted=False).all()
            self.topologies = [Topology(self.context, self.instance_id,
                                        topology_entry=t)
                               for t in self.topologies]
        else:
            # if context is None you get nothing.
            self.topologies = []

        LOG.info(_('Topologies: %s') % self.topologies)

    def __iter__(self):
        for topology in self.topologies:
            yield topology.datastore

    def __len__(self):
        LOG.info(_('Getting length of topologies'))
        return len(self.topologies)

    def __getitem__(self, item):
        for topology in self.topologies:
            if topology.datastore == item:
                return topology.topology

    def __delitem__(self, item):
        for topology in self.topologies:
            if topology.datastore == item:
                topology.delete()

        self._load_topologies()

    def __setitem__(self, key, value):
        # NOTE(imsplitbit): There is a known issue here where users of
        # this model will need to act upon each key/value pair in whole
        # because the topology values are stored in marshaled form so there
        # is no way to do an operation on nested objects.

        # If new topology is created we will want to reload all topology from
        # the db after successful creation
        force_reload = False

        found_topology = None
        for topology in self.topologies:
            if topology.datastore == key:
                # The key already exists so this an update operation
                found_topology = topology
                found_topology.set_topology(value)

        if not found_topology:
            # This isn't an update operation so make a new topology entry
            force_reload = True
            DBTopologies.create(instance_id=self.instance_id,
                                datastore=key,
                                topology=json.dumps(value)).save()

        # Now reload topology from the DB so as to keep all data current in
        # the instance variable self.topologies
        if force_reload:
            self._load_topologies()

    def __contains__(self, item):
        for topology in self.topologies:
            if topology.datastore == item:
                return True

        return False

    def __eq__(self, other):
        # use self.copy() to render a dictionary and then allow python's
        # dict builtin to do the comparison.
        return self.copy() == other

    def __ne__(self, other):
        # use self.copy() to render a dictionary and then allow python's
        # dict builtin to do the comparison.
        return self.copy() != other

    def __repr__(self):
        # use self.copy() to render a dictionary and then allow python's
        # dict builtin __repr__
        return self.copy().__repr__()

    def __str__(self):
        # use self.copy() to render a dictionary and then allow python's
        # dict builtin __str__
        return self.copy().__str__()

    def __dict__(self):
        return self.copy()

    def keys(self):
        datastores = list()
        for topology in self.topologies:
            datastores.append(topology.datastore)

        return datastores

    def values(self):
        topologies = list()

        for topology in self.topologies:
            topologies.append(topology.topology)

        return topologies

    def items(self):
        items = list()

        for topology in self.topologies:
            items.append((topology.datastore, topology.topology))

        return items

    def get(self, key, default=None):
        value = default

        for topology in self.topologies:
            if topology.datastore == key:
                value = topology.topology

        return value

    def clear(self):
        for topology in self.topologies:
            topology.delete()

        self._load_topologies()

    def iterkeys(self):
        for datastore in self.keys():
            yield datastore

    def pop(self, key):
        for topology in self.topologies:
            if topology.datastore == key:
                return topology.topology

        raise KeyError(key)

    def itervalues(self):
        for topology in self.values():
            yield topology

    def iteritems(self):
        for item in self.items():
            yield item

    def copy(self):
        result = {}
        for topology in self.topologies:
            result[topology.datastore] = topology.topology

        return result

    def save(self):
        """
        Iterate through all Topology objects and call save() on them
        to synchronize them to the underlying database.
        """
        for topology in self.topologies:
            topology.save()
