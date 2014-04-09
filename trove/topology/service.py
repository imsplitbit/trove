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

from trove.common import apischema
from trove.common import exception
from trove.common import wsgi
from trove.topology.models import Topologies
from trove.topology.models import Topology
from trove.topology.views import TopologyView
from trove.topology.views import TopologiesView
from trove.openstack.common import log as logging
from trove.openstack.common.gettextutils import _

LOG = logging.getLogger(__name__)


class TopologyController(wsgi.Controller):
    schemas = apischema.topology.copy()

    @staticmethod
    def list(req, tenant_id, instance_id):
        """
        Show all topologies for instance {instance_id}

        :param req: wsgi.Request object
        :param tenant_id: Id of the tenant
        :param instance_id: UUID for the instance

        :rtype: wsgi.Result
        """
        context = req.environ[wsgi.CONTEXT_KEY]
        topologies = Topologies(context, instance_id)
        return wsgi.Result(TopologiesView(topologies, req).data(), 200)

    @staticmethod
    def show(req, tenant_id, instance_id, datastore):
        """
        Show topologies for instance {instance_id}

        :param req: wsgi.Request object
        :param tenant_id: Id of the tenant
        :param instance_id: UUID for the instance

        :rtype: wsgi.Result
        """
        context = req.environ[wsgi.CONTEXT_KEY]
        try:
            topology = Topology(context, instance_id, datastore=datastore)
        except exception.ModelNotFoundError:
            return wsgi.Result(None, 404)

        return wsgi.Result(TopologyView(topology, req).data(), 200)

    @staticmethod
    def create(req, body, tenant_id, instance_id, datastore):
        """
        Create new topology for instance {instance_id}

        body example:
        {
            'topology': {
                "slave_of": [{"id": "dfbbd9ca-b5e1-4028-adb7-f78643e17998"}],
                "read_only": true
            }
        }

        :param req: wsgi.Request object
        :param body: Dict deserialized from the user supplied JSON
        :param tenant_id: Id of the tenant
        :param instance_id: UUID for the instance
        :param datastore: datastore for which the topology should apply

        :rtype: wsgi.Result
        """
        context = req.environ[wsgi.CONTEXT_KEY]
        topology = body.get('topology')
        topologies = Topologies(context=context, instance_id=instance_id)
        if datastore not in topologies:
            LOG.debug(_('Datastore %(datastore)s creating') %
                      {'datastore': datastore})
            topologies[datastore] = topology
            LOG.debug(_('Datastore %(datastore)s created') %
                      {'datastore': datastore})
            return wsgi.Result(TopologiesView(topologies, req).data(), 200)
        else:
            LOG.debug(_('Datastore %(datastore)s already in topologies') %
                      {'datastore': datastore})
            return wsgi.Result(None, 403)

    @staticmethod
    def edit(req, body, tenant_id, instance_id, datastore):
        """
        Edit topology for instance {id}.  This edits
        topologies that are already present.

        body example:
        {
            'topology': {
                "slave_of": [{"id": "dfbbd9ca-b5e1-4028-adb7-f78643e17998"}],
                "read_only": false
            }
        }

        :param req: wsgi.Request object
        :param body: Dict deserialized from the user supplied JSON
        :param tenant_id: Id of the tenant
        :param instance_id: UUID for the instance
        :param key: key for the metadata entry

        :rtype: wsgi.Result
        """
        context = req.environ[wsgi.CONTEXT_KEY]
        topology = body.get('topology')
        topologies = Topologies(context=context, instance_id=instance_id)
        if datastore in topologies:
            LOG.debug(_('Datastore %(datastore)s exists, now editing') %
                      {'datastore': datastore})
            topologies[datastore] = topology
            LOG.debug(_('Datastore %(datastore)s edited') %
                      {'datastore': datastore})
            return wsgi.Result(None, 200)
        else:
            LOG.debug(_('Datastore %(datastore)s not in topologies') %
                      {'datastore': datastore})
            return wsgi.Result(None, 404)

    @staticmethod
    def delete(req, tenant_id, instance_id, datastore):
        """
        Delete all topologies for instance {id}

        :param req: wsgi.Request object
        :param tenant_id: Id of the tenant
        :param instance_id: UUID for the instance
        :param datastore: datastore to remove from topologies

        :rtype: wsgi.Result
        """
        context = req.environ[wsgi.CONTEXT_KEY]
        topologies = Topologies(context=context, instance_id=instance_id)
        if datastore in topologies:
            LOG.debug(
                _('Datastore %(datastore)s found in topologies, deleting') %
                {'datastore': datastore})
            del(topologies[datastore])
            LOG.debug(_('Datastore %(datastore)s deleted') %
                      {'datastore': datastore})
            return wsgi.Result(None, 200)
        else:
            LOG.debug(_('Datastore %(datastore)s not in topologies, '
                        'cannot delete.') % {'datastore': datastore})
            return wsgi.Result(None, 404)

    @staticmethod
    def action(req, body, tenant_id, id):
        pass
