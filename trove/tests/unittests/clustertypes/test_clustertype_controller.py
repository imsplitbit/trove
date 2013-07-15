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

from trove.clustertype.models import ClusterTypes
from trove.clustertype.service import ClusterTypeController
from trove.clustertype.views import ClusterTypeView
from trove.clustertype.views import ClusterTypesView
from trove.tests.unittests.clustertypes.base import TestClusterTypeBase


class TestClusterTypeController(TestClusterTypeBase):
    def setUp(self):
        super(TestClusterTypeController, self).setUp()
        self.clustertypes = ClusterTypes()
        self.controller = ClusterTypeController()

    def tearDown(self):
        super(TestClusterTypeController, self).tearDown()

    def test_show(self):
        clustertype_view = ClusterTypeView(self.clustertypes[0], self.req)
        result = self.controller.show(
            self.req, self.context.tenant, self.fake_data['id'])
        self.assertEqual(result.status, 200)
        self.assertEqual(result._data, clustertype_view.data())

    def test_list(self):
        clustertypes_view = ClusterTypesView(self.clustertypes, self.req)
        result = self.controller.index(self.req, self.context.tenant)
        self.assertEqual(result.status, 200)
        self.assertEqual(result._data, clustertypes_view.data())
        self.assertEqual(len(clustertypes_view.data()['clustertypes']), 1)
