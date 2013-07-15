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

import testtools
from trove.clustertype.models import DBClusterType
from trove.tests.unittests.util import util
import time
from trove.common import context
from trove.common import wsgi

CURRENT_TIME = str(int(time.time()))

CLUSTERTYPE_DATA = {
    'id': '0c6941ba-e2f9-4d35-93b9-ac56588eaec7',
    'type': 'master-slave',
    'name': 'Master/Slave Replication/Clustering',
    'max_instances': 5,
    'min_instances': 3
}

CONTEXT = context.TroveContext(tenant='TENANT-' + CURRENT_TIME)


class FakeRequest(object):
    def __init__(self):
        self.__dict__[wsgi.CONTEXT_KEY] = context.TroveContext(
            tenant='TENANT-' + CURRENT_TIME)

    @property
    def host(self):
        return 'service.host.com'

    @property
    def url_version(self):
        return '1.1'

    @property
    def environ(self):
        return self.__dict__


class TestClusterTypeBase(testtools.TestCase):
    def setUp(self):
        super(TestClusterTypeBase, self).setUp()

        util.init_db()
        DBClusterType.create(
            id=CLUSTERTYPE_DATA['id'],
            type=CLUSTERTYPE_DATA['type'],
            name=CLUSTERTYPE_DATA['name'],
            max_instances=CLUSTERTYPE_DATA['max_instances'],
            min_instances=CLUSTERTYPE_DATA['min_instances']
        )

        self.fake_data = CLUSTERTYPE_DATA
        self.context = CONTEXT
        self.req = FakeRequest()

    def tearDown(self):
        super(TestClusterTypeBase, self).tearDown()
