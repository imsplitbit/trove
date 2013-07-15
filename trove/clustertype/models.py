# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2013 Rackspace
# All Rights Reserved.
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

"""Model classes that form the core of clustertype functionality."""

from trove.common import exception
from trove.db import models
from trove.openstack.common.gettextutils import _
from trove.openstack.common import log as logging

LOG = logging.getLogger(__name__)


def persisted_models():
    return {'clustertype': DBClusterType}


class ClusterType(object):

    _data_fields = ['id', 'name', 'type', 'max_instances', 'min_instances',
                    'deleted', 'created', 'updated', 'deleted_at']

    def __init__(self, clustertype=None, context=None, clustertype_id=None):
        """
        Create a ClusterType object

        :param self:
        :param clustertype: A preformed clustertype
        :param context: Context to operate as
        :param clustertype_id: UUID of the clustertype
        :return:
        """
        if clustertype:
            LOG.debug(_('ClusterType was given, returning'))
            self.clustertype = clustertype
            return
        elif context and clustertype_id:
            LOG.debug(
                _('ClusterType not given, looking up ClusterType by id: %s') %
                (clustertype_id,))
            try:
                clustertype = DBClusterType.find_by(context, id=clustertype_id)
                self.clustertype = clustertype
            except exception.ModelNotFoundError:
                LOG.error(
                    _("ClusterType id: %s Not Found!") % (clustertype_id,))
                raise exception.ClusterTypeNotFound
        else:
            raise exception.ClusterTypeError(_("No ClusterType or ID given"))

    @property
    def id(self):
        return self.clustertype.id

    @property
    def name(self):
        return self.clustertype.name

    @property
    def description(self):
        return self.clustertype.description

    @property
    def type(self):
        return self.clustertype.type

    @property
    def max_instances(self):
        return self.clustertype.max_instances

    @property
    def min_instances(self):
        return self.clustertype.min_instances


class ClusterTypes(object):
    def __init__(self):
        """
        Fetch a list of all clustertypes

        :return:
        """
        try:
            LOG.debug(_('Finding all cluster types'))
            self.clustertypes = DBClusterType.find_all(deleted=False).all()
            LOG.debug(_('Clustertypes before comprehension: %s') %
                      (self.clustertypes,))
            self.clustertypes = [
                ClusterType(clustertype=ct) for ct in self.clustertypes
            ]
            LOG.debug(_('Clustertypes from DB: %s') % (self.clustertypes,))
            LOG.debug(_('Found all cluster types'))
        except exception.ModelNotFoundError:
            msg = _('No ClusterTypes found!')
            LOG.error(msg)
            raise exception.ClusterTypeNotFound(msg)

    def __iter__(self):
        for ct in self.clustertypes:
            yield ct

    def __getitem__(self, key):
        return self.clustertypes[key]

    def __contains__(self, item):
        return item in self.clustertypes


class DBClusterType(models.DatabaseModelBase):
    _data_fields = ['id', 'name', 'type', 'max_instances', 'min_instances',
                    'deleted', 'created', 'updated', 'deleted_at']
    preserve_on_delete = True
    _table_name = "clustertypes"
