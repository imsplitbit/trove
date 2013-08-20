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

from trove.tests.unittests.clusters.base import TestClusterBase
from trove.clustertype.models import DBClusterType
from trove.tests.unittests.util import util
from trove.cluster.models import DBCluster
from trove.cluster.models import DBClusterInstance
from trove.cluster.models import Cluster
from trove.cluster.models import Clusters
from trove.cluster.models import ClusterInstance
from trove.cluster.models import ClusterInstances


class TestClusterModel(TestClusterBase):
    def setUp(self):
        super(TestClusterModel, self).setUp()

        # Setup the test db
        util.init_db()

        # Create a cluster type in the db
        DBClusterType.create(**self.fake_cluster_type)

        # Create a test cluster in the db
        DBCluster.create(**self.fake_cluster)

        # create some fake instances in the db for testing
        for cluster_instance in self.fake_cluster_instances:
            DBClusterInstance.create(**cluster_instance)

    def tearDown(self):
        super(TestClusterModel, self).tearDown()

        # Clean things up
        cluster = DBCluster.find_by(
            self.context, id=self.fake_cluster['id'])
        cluster.delete()

        #for cluster_instance in self.fake_cluster_instances:
        #    cluster_instance = DBClusterInstance.find_by(
        #        self.context, id=cluster_instance['id'], deleted=False)
        #    if cluster_instance:
        #        cluster_instance.delete()

    def test_dbcluster(self):
        # Verify the DBCluster class doesn't mangle data from it's origin
        cluster = DBCluster.find_by(self.context, id=self.fake_cluster['id'])
        self.assertEqual(cluster.id, self.fake_cluster['id'])
        self.assertEqual(cluster.tenant_id, self.fake_cluster['tenant_id'])
        self.assertEqual(cluster.name, self.fake_cluster['name'])
        self.assertEqual(cluster.description, self.fake_cluster['description'])
        self.assertEqual(cluster.type, self.fake_cluster['type'])

    def test_dbcluster_instance(self):
        # Verify the DBClusterInstance class doesn't mangle data from
        # it's origin
        cluster_instance = DBClusterInstance.find_by(
            self.context, id=self.fake_master_1['id'])
        self.assertEqual(cluster_instance.id, self.fake_master_1['id'])
        self.assertEqual(
            cluster_instance.instance_id, self.fake_master_1['instance_id'])
        self.assertEqual(
            cluster_instance.cluster_id, self.fake_master_1['cluster_id'])
        self.assertEqual(
            cluster_instance.tenant_id, self.fake_master_1['tenant_id'])

    def test_cluster(self):
        # Verify the Cluster class doesn't mangle any data from it's origin
        cluster = Cluster(
            cluster_id=self.fake_cluster['id'], context=self.context)
        self.assertIsNotNone(cluster.instances)
        self.assertEqual(type(cluster.instances[0]), ClusterInstance)
        self.assertEqual(cluster.id, self.fake_cluster['id'])
        self.assertEqual(cluster.name, self.fake_cluster['name'])
        self.assertEqual(cluster.type, self.fake_cluster['type'])
        self.assertEqual(cluster.description, self.fake_cluster['description'])
        self.assertEqual(cluster.tenant_id, self.fake_cluster['tenant_id'])

    def test_clusters(self):
        clusters = Clusters(context=self.context)
        for cluster in clusters:
            self.assertEqual(cluster.tenant_id, self.fake_cluster['tenant_id'])
            self.assertEqual(cluster.id, self.fake_cluster['id'])
            for cluster_instance in cluster.instances:
                self.assertEqual(cluster_instance.cluster_id, cluster.id)
                self.assertIn(cluster_instance.id,
                              [
                                  self.fake_master_1['id'],
                                  self.fake_slave_1['id'],
                                  self.fake_slave_2['id']
                              ])

    def test_cluster_instance(self):
        cluster_instance = ClusterInstance(
            context=self.context, cluster_instance_id=self.fake_master_1['id'])
        self.assertEqual(cluster_instance.id, self.fake_master_1['id'])
        self.assertEqual(
            cluster_instance.cluster_id, self.fake_master_1['cluster_id'])
        self.assertEqual(
            cluster_instance.tenant_id, self.fake_master_1['tenant_id'])
        self.assertEqual(
            cluster_instance.instance_id, self.fake_master_1['instance_id'])

    def test_cluster_instances(self):
        cluster_instances = ClusterInstances(
            context=self.context, cluster_id=self.fake_cluster['id'])

        for cluster_instance in cluster_instances:
            self.assertEqual(
                cluster_instance.cluster_id, self.fake_cluster['id'])
            self.assertEqual(
                cluster_instance.tenant_id, self.fake_cluster['tenant_id'])
            self.assertIn(cluster_instance.id,
                          [
                              self.fake_master_1['id'],
                              self.fake_slave_1['id'],
                              self.fake_slave_2['id']
                          ])
            self.assertIn(cluster_instance.instance_id,
                          [
                              self.fake_master_1['instance_id'],
                              self.fake_slave_1['instance_id'],
                              self.fake_slave_2['instance_id']
                          ])
