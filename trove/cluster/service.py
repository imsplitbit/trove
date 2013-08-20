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

from trove.common import wsgi
from trove.cluster import models
from trove.cluster import views
from trove.instance import models as instance_models
from trove.openstack.common.gettextutils import _
from trove.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class ClusterTypeController(wsgi.Controller):
    """Controller for flavor functionality"""

    def show(self, req, tenant_id, cluster_id):
        """Return a single cluster."""
        context = req.environ[wsgi.CONTEXT_KEY]
        clustertype = models.Cluster(
            None, context=context, cluster_id=cluster_id)
        data = views.ClusterView(clustertype, req).data()
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

        LOG.debug(_('Request: %s') % (req,))
        LOG.debug(_('Body: %s') % (body,))
        LOG.debug(_('Tenant ID: %s') % (tenant_id,))

        context = req.environ[wsgi.CONTEXT_KEY]
        cluster_info = body['cluster']
        cluster_type = body['cluster']['clusterConfig']['type']
        primary_node = body['cluster']['clusterConfig'].get(
            'primaryNode', None)

    def delete(self, req, tenant_id, cluster_id):
        pass

    def modify(self, req, tenant_id, cluster_id):
        pass
