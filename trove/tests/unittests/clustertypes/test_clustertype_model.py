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

from trove.clustertype.models import ClusterType
from trove.clustertype.models import ClusterTypes
from trove.clustertype.models import DBClusterType
from trove.tests.unittests.clustertypes.base import TestClusterTypeBase


class TestClusterTypeModel(TestClusterTypeBase):
    def setUp(self):
        super(TestClusterTypeModel, self).setUp()
        self.clustertypes = DBClusterType.find_all(deleted=False).all()

    def tearDown(self):
        super(TestClusterTypeModel, self).tearDown()

    def test_dbclustertypes(self):
        self.assertEqual(len(self.clustertypes), 1)

    def test_clustertype_using_clustertype(self):
        clustertype = ClusterType(clustertype=self.clustertypes[0])
        self.assertEqual(clustertype.id, self.fake_data['id'])

    def test_clustertype_using_db(self):
        clustertype = ClusterType(
            context=self.context, clustertype_id=self.clustertypes[0].id)
        self.assertEqual(clustertype.id, self.fake_data['id'])

    def test_clustertype_properties(self):
        clustertype = ClusterType(clustertype=self.clustertypes[0])
        self.assertEqual(clustertype.id, self.fake_data['id'])
        self.assertEqual(clustertype.type, self.fake_data['type'])
        self.assertEqual(clustertype.name, self.fake_data['name'])
        self.assertEqual(
            clustertype.max_instances, self.fake_data['max_instances'])
        self.assertEqual(
            clustertype.min_instances, self.fake_data['min_instances'])

    def test_clustertypes(self):
        clustertypes = ClusterTypes()
        for ct in clustertypes:
            self.assertEqual(ct.id, self.clustertypes[0].id)
