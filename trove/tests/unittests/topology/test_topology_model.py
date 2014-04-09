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

from trove.common.exception import TopologyModelError
from trove.topology.models import Topologies
from trove.topology.models import Topology
from trove.tests.unittests.topology.base import TestTopologyBase


class TestTopologyModel(TestTopologyBase):
    def setUp(self):
        super(TestTopologyModel, self).setUp()
        self.datastore = 'redis'

    def tearDown(self):
        super(TestTopologyModel, self).tearDown()

    def test_topology__getitem__(self):
        self.assertEqual(
            self.dbtopology[self.datastore],
            self.topology[self.datastore])

    def test_topology_keys(self):
        self.assertIn(self.datastore, self.dbtopology.keys())

    def test_topology_values(self):
        self.assertIn(
            self.topology[self.datastore], self.dbtopology.values())

    def test_topology__iter__(self):
        for meta in self.dbtopology:
            self.assertIn(meta, self.topology.keys())

    def test_topology__eq__(self):
        self.assertTrue(self.dbtopology == self.topology)

    def test_topology__ne__(self):
        self.assertFalse(self.dbtopology != self.topology)

    def test_topology_len(self):
        self.assertEqual(len(self.dbtopology), len(self.topology))

    def test_topology_delete(self):
        del(self.dbtopology[self.datastore])
        self.assertNotIn(self.datastore, self.dbtopology.keys())

    def test_topology_copy(self):
        topology_copy = self.dbtopology.copy()
        for key in topology_copy.keys():
            self.assertIn(key, self.topology.keys())
            self.assertIn(topology_copy[key], self.topology.values())

    def test_topology_iteritems(self):
        for k, v in self.dbtopology.iteritems():
            self.assertIn(k, self.topology.keys())
            self.assertEqual(self.topology[k], v)

    def test_topology_itervalues(self):
        for v in self.dbtopology.itervalues():
            self.assertIn(v, self.topology.values())

    def test_topology_iterkeys(self):
        for k in self.dbtopology.iterkeys():
            self.assertIn(k, self.topology.keys())

    def test_topology_pop(self):
        key = self.datastore
        data = self.dbtopology.pop(key)
        self.assertEqual(data, self.topology[key])

    def test_topology_pop_no_key(self):
        key = 'this_key_doesnt_exist'
        self.assertRaises(KeyError, self.dbtopology.pop, key)

    def test_topology_items(self):
        for k, v in self.dbtopology.items():
            self.assertIn(k, self.topology.keys())
            self.assertIn(v, self.topology.values())

    def test_topology_get(self):
        key = self.datastore
        data = self.dbtopology.get(key)
        self.assertEqual(self.topology[key], data)

    def test_topology_get_default(self):
        key = 'this_key_doesnt_exist'
        default = 'this_is_the_default_value'
        data = self.dbtopology.get(key, default)
        self.assertEqual(default, data)

    def test_topology_get_default_none(self):
        key = 'this_key_doesnt_exist'
        data = self.dbtopology.get(key)
        self.assertIsNone(data)

    def test_topology_in(self):
        key = self.datastore
        self.assertIn(key, self.dbtopology)

    def test_topology_not_in(self):
        key = 'this_key_doesnt_exist'
        self.assertNotIn(key, self.dbtopology)

    def test_topology_clear(self):
        self.dbtopology.clear()
        self.assertEqual(0, len(self.dbtopology))

    def test_topology_copy_type(self):
        self.dbtopology.clear()
        meta_copy = self.dbtopology.copy()
        self.assertIsInstance(meta_copy, dict)

    def test_topologyentry_create_by_key_value(self):
        datastore = 'couchbase'
        topology = {
            'cluster_name': 'products',
            'join': True
        }
        newtopology = {datastore: topology}
        me = Topology(context=self.context, instance_id=self.instance_id,
                      datastore=datastore, topology=newtopology[datastore])
        result = me.copy()
        topologies = Topologies(self.context, self.instance_id)
        self.assertIn(datastore, topologies.keys())
        self.assertEqual(newtopology, result)

    def test_topologyentry_failed_create(self):
        self.assertRaises(TopologyModelError, Topology, None, None,
                          key='Test')

    def test_topology_failed_init(self):
        self.assertRaises(TopologyModelError, Topology, None, None)
