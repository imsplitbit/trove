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

from trove.common import wsgi
from trove.clustertype import models
from trove.clustertype import views
from trove.openstack.common.gettextutils import _
from trove.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class ClusterTypeController(wsgi.Controller):
    """Controller for flavor functionality"""

    def show(self, req, tenant_id, id):
        """Return a single clustertype."""
        context = req.environ[wsgi.CONTEXT_KEY]
        clustertype = models.ClusterType(None, context=context,
                                         clustertype_id=id)
        data = views.ClusterTypeView(clustertype, req).data()
        LOG.debug(_('ClusterType Data: %s') % (data,))
        # Pass in the request to build accurate links.
        return wsgi.Result(data, 200)

    def index(self, req, tenant_id):
        """Return all clustertypes."""
        clustertypes = models.ClusterTypes()
        data = views.ClusterTypesView(clustertypes, req).data()
        LOG.debug(_('ClusterTypes Data: %s') % (data,))
        return wsgi.Result(data, 200)
