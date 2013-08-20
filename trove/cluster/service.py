#Copyright [2013] Rackspace

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from trove.common import cfg
from trove.common import utils
from trove.common import wsgi
from trove.cluster import models
from trove.cluster import views
from trove.clustertype import models as ctype_models
from trove.instance import models as instance_models
from trove.instance import views as instance_views
from trove.openstack.common.gettextutils import _
from trove.openstack.common import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class ClusterController(wsgi.Controller):
    """Controller for cluster functionality"""

    def show(self, req, tenant_id, cluster_id):
        """Return a single cluster."""
        context = req.environ[wsgi.CONTEXT_KEY]
        cluster = models.Cluster(
            None, context=context, cluster_id=cluster_id)
        data = views.ClusterView(cluster, req).data()
        LOG.debug(_('ClusterType Data: %s') % (data,))
        # Pass in the request to build accurate links.
        return wsgi.Result(data, 200)

    def index(self, req, tenant_id):
        """Return all clusters for a tenant."""
        context = req.environ[wsgi.CONTEXT_KEY]
        clusters = models.Clusters(context=context)
        data = views.ClustersView(clusters, req).data()
        LOG.debug(_('ClusterTypes Data: %s') % (data,))
        return wsgi.Result(data, 200)

    def create(self, req, body, tenant_id):
        """
        Create a cluster

        :param req:
        :param body:
        :param tenant_id:
        :return:
        """
        LOG.info(_('Cluster Info in Cluster.create()'))
        LOG.info(_('Request: %s') % (req,))
        LOG.info(_('Body: %s') % (body,))
        LOG.info(_('Tenant ID: %s') % (tenant_id,))

        # Setup our vars
        context = req.environ[wsgi.CONTEXT_KEY]
        cluster_type_id = utils.get_id_from_href(
            body['cluster']['clusterConfig']['type'])
        ctype = ctype_models.ClusterType(None, context, cluster_type_id)
        primary_node = body['cluster']['clusterConfig'].get(
            'primaryNode', None)
        name = body['cluster']['name']
        description = body['cluster']['description']
        num_instances = body['cluster']['instances']
        volume_size = body['cluster']['volume']['size']
        flavor_id = utils.get_id_from_href(body['cluster']['flavorRef'])

        #TODO(imsplitbit): need to implement service type in clustertypes
        # then fix this.
        service = instance_models.ServiceImage.find_by(
            service_name=CONF.service_type)
        image_id = service['image_id']

        # Create the Cluster Object
        cluster = models.Cluster.create(
            tenant_id=context.tenant,
            name=name,
            type=ctype.type,
            description=description
        )

        LOG.info(_('Context: %(context)s') % locals())
        LOG.info(_('Cluster type id: %(cluster_type_id)s') % locals())
        LOG.info(_('ClusterType: %(ctype)s') % locals())
        LOG.info(_('Cluster ID: %s') % cluster.id)
        LOG.info(_('Primary Node: %(primary_node)s') % locals())
        LOG.info(_('Name: %(name)s') % locals())
        LOG.info(_('Description: %(description)s') % locals())
        LOG.info(_('Instances: %(num_instances)s') % locals())
        LOG.info(_('Volume Size: %(volume_size)s') % locals())
        LOG.info(_('Flavor ID: %(flavor_id)s') % locals())
        LOG.info(_('Image ID: %(image_id)s') % locals())

        # Create the instances
        instances = list()
        cluster_instances = list()
        for i in xrange(num_instances):
            LOG.info(
                _('Creating instance %(i)s of %(num_instance)s') % locals())
            instance = instance_models.Instance.create(
                context, name, flavor_id, image_id, [], [], CONF.service_type,
                volume_size, None)
            # TODO(imsplitbit): do some super mojo here that sets instance
            # attributes when it exists.
            # instance.set_attributes(blah blah blah)
            instances.append(instance)

            # Make a cluster_instance object
            cluster_instances.append(
                models.ClusterInstance.create(
                    tenant_id=context.tenant,
                    cluster_id=cluster.id,
                    instance_id=instance.id
                )
            )

        cluster.instances = cluster_instances
        instances = instance_views.InstancesView(instances, req).data()

        # TODO(imsplitbit): Hook in some magic to make the instances created
        # do the clustering/replication thing

        view = views.ClusterView(cluster, req)
        return wsgi.Result(view.data(), 200)

    def delete(self, req, tenant_id, cluster_id):
        """
        Delete the cluster <cluster_id> and clean up any artifacts.

        :param req:
        :param tenant_id:
        :param cluster_id:
        :return:
        """
        LOG.info(_('Cluster Info in Cluster.delete()'))
        LOG.info(_('Request: %s') % (req,))
        LOG.info(_('Tenant ID: %s') % (tenant_id,))
        LOG.info(_('Cluster ID: %s') % (cluster_id,))

        # Setup our vars
        context = req.environ[wsgi.CONTEXT_KEY]
        cluster = models.Cluster(cluster_id=cluster_id, context=context)
        cluster_instances = models.ClusterInstances(context, cluster_id)

        # Before deleting the cluster object we need to delete all of
        # it's instances.
        for cluster_instance in cluster_instances:
            msg_vars = {
                'instance_id': cluster_instance.instance_id,
                'cluster_id': cluster_id
            }
            LOG.info(
                _('Deleting instance %(instance_id)s from %(cluster_id)s') %
                msg_vars)
            instance = instance_models.load_any_instance(
                context, cluster_instance.instance_id)
            instance.delete()
            LOG.info(
                _('Deleted instance %(instance_id)s from %(cluster_id)s') %
                msg_vars)

        cluster_instances.delete()
        cluster.delete()

        view = views.ClusterView(cluster, req)
        return wsgi.Result(view.data(), 200)

    def modify(self, req, tenant_id, cluster_id):
        pass
