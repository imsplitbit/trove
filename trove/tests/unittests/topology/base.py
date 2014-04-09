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

import uuid
import testtools
from trove.topology.models import Topologies
from trove.topology.service import TopologyController
from trove.topology.views import TopologiesView
from trove.tests.unittests.util import util
import time
from trove.common import context
from trove.common import wsgi

CONTEXT = context.TroveContext(tenant='TENANT-' + str(int(time.time())))


class FakeRequest(object):
    def __init__(self):
        self.__dict__[wsgi.CONTEXT_KEY] = CONTEXT

    @property
    def host(self):
        return 'service.host.com'

    @property
    def url_version(self):
        return '1.1'

    @property
    def environ(self):
        return self.__dict__


class TestTopologyBase(testtools.TestCase):
    def setUp(self):
        # Basic setup and mock/fake structures for testing only
        super(TestTopologyBase, self).setUp()
        util.init_db()
        self.topology_key = 'redis'
        self.topology_value = {
            'slave_of': [{'id': 'c3027dbc-aa36-4f28-97dd-9e93d7e076c6'}]
        }
        self.topology = {
            self.topology_key: self.topology_value,
            'mongodb': {'type': 'member', 'replSet': 'products'}
        }
        self.create_body = {
            'topology': {
                self.topology_key: self.topology_value
            }
        }
        self.edit_body = {
            'topology': {
                'slave_of': [{'id': '25ca2b07-6091-4542-8eaa-fa3e737279ab'}]
            }
        }
        self.instance_id = str(uuid.uuid4())
        self.second_instance_id = str(uuid.uuid4())
        self.tenant_id = 'bae4c4d3-3188-4da9-9d97-d2cea9d8c062'
        self.context = CONTEXT
        self.req = FakeRequest()
        self.controller = TopologyController()
        self.serialization_type = 'application/json'
        self.dbtopology = Topologies(self.context, self.instance_id)

        for k, v in self.topology.iteritems():
            self.dbtopology[k] = v

        # This helps to make sure we test the unique constraint and foreign
        # key constrain on the database model.
        self.second_dbtopology = Topologies(self.context,
                                            self.second_instance_id)

        for k, v in self.topology.iteritems():
            self.second_dbtopology[k] = v

        self.topology_view = TopologiesView(self.dbtopology, self.req).data()

    def tearDown(self):
        super(TestTopologyBase, self).tearDown()
