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

import testtools
import time
from trove.common import context
from trove.common import wsgi

CURRENT_TIME = str(int(time.time()))

CONTEXT = context.TroveContext(tenant='TENANT-' + CURRENT_TIME)

CLUSTERTYPE_DATA = {
    'id': '0c6941ba-e2f9-4d35-93b9-ac56588eaec7',
    'type': 'master-slave',
    'name': 'Master/Slave Replication/Clustering',
    'max_instances': 5,
    'min_instances': 3
}

CLUSTER_DATA = {
    'id': 'b67ba2e0-7a9c-4dd2-b175-62e263bba165',
    'tenant_id': CONTEXT.tenant,
    'type': CLUSTERTYPE_DATA['id'],
    'name': 'test',
    'description': 'test cluster'
}

CLUSTER_INSTANCE_MASTER_1 = {
    'id': 'a8968fd7-8ad4-45b2-a813-730c58df6733',
    'tenant_id': CONTEXT.tenant,
    'cluster_id': CLUSTER_DATA['id'],
    'instance_id': 'c5f70573-1255-431d-9a6e-429bed816d99'
}

CLUSTER_INSTANCE_SLAVE_1 = {
    'id': 'ce7e8262-aef9-4e35-9dc2-f84ff585c72c',
    'tenant_id': CONTEXT.tenant,
    'cluster_id': CLUSTER_DATA['id'],
    'instance_id': 'd8a94cd6-b86b-4756-a738-976be3dcf63d'
}

CLUSTER_INSTANCE_SLAVE_2 = {
    'id': '86042661-1e72-4dba-8411-2996565347e4',
    'tenant_id': CONTEXT.tenant,
    'cluster_id': CLUSTER_DATA['id'],
    'instance_id': 'c8f79772-300e-42c2-8c32-b44b8448267d'
}

CLUSTER_INSTANCES = [
    CLUSTER_INSTANCE_MASTER_1,
    CLUSTER_INSTANCE_SLAVE_1,
    CLUSTER_INSTANCE_SLAVE_2
]


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


class TestClusterBase(testtools.TestCase):
    def setUp(self):
        super(TestClusterBase, self).setUp()

        # make constants available for verification
        self.fake_cluster = CLUSTER_DATA
        self.fake_master_1 = CLUSTER_INSTANCE_MASTER_1
        self.fake_slave_1 = CLUSTER_INSTANCE_SLAVE_1
        self.fake_slave_2 = CLUSTER_INSTANCE_SLAVE_2
        self.fake_cluster_instances = [
            self.fake_master_1,
            self.fake_slave_1,
            self.fake_slave_2,
        ]
        self.fake_cluster_type = CLUSTERTYPE_DATA
        self.req = FakeRequest()
        self.context = CONTEXT

    def tearDown(self):
        super(TestClusterBase, self).tearDown()
