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
from trove.clustertype.views import ClusterTypeView
from trove.clustertype.views import ClusterTypesView
from trove.tests.unittests.clustertypes.base import TestClusterTypeBase


class TestClusterTypeView(TestClusterTypeBase):
    def setUp(self):
        super(TestClusterTypeView, self).setUp()
        self.clustertypes = ClusterTypes()

    def tearDown(self):
        super(TestClusterTypeView, self).tearDown()

    def test_clustertype_view_data(self):
        clustertype = self.clustertypes[0]
        view = ClusterTypeView(clustertype, self.req)
        data = view.data()['clustertype']

        for link in data['links']:
            self.assertIn(self.req.host, link['href'])
            self.assertIn(self.fake_data['id'], link['href'])
            if link['rel'] == 'self':
                self.assertIn(self.req.url_version, link['href'])

        self.assertEqual(data['name'], self.fake_data['name'])
        self.assertEqual(data['id'], self.fake_data['id'])
        self.assertEqual(data['type'], self.fake_data['type'])
        self.assertEqual(
            data['max_instances'], self.fake_data['max_instances'])
        self.assertEqual(
            data['min_instances'], self.fake_data['min_instances'])

    def test_clustertypes_view_data(self):
        clustertype_view = ClusterTypeView(
            self.clustertypes[0], self.req).data()['clustertype']
        view = ClusterTypesView(
            self.clustertypes, self.req).data()['clustertypes']
        self.assertEqual(len(view), 1)
        self.assertIn(clustertype_view, view)
