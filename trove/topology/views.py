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

from trove.openstack.common import log as logging
from trove.openstack.common.gettextutils import _
from trove.common import cfg

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class TopologyView(object):
    def __init__(self, topology, req=None):
        self.topology = topology
        self.req = req

    def data(self):
        data = {
            'topology': self.topology.copy()
        }
        LOG.info(_('Topology: %s') % data)
        return data


class TopologiesView(object):
    def __init__(self, topologies, req=None):
        self.topologies = topologies
        self.req = req

    def data(self):
        data = {
            'topology': self.topologies.copy()
        }
        LOG.info(_('Topologies: %s') % data)
        return data
