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

import jsonschema
from trove.tests.unittests.topology.base import TestTopologyBase


class TestTopologyController(TestTopologyBase):
    def setUp(self):
        super(TestTopologyController, self).setUp()

    def tearDown(self):
        super(TestTopologyController, self).tearDown()

    # def test_get_schema_create(self):
    #     schema = self.controller.get_schema('create', self.topology_view)
    #     self.assertIsNotNone(schema)
    #     self.assertTrue('topology' in schema['properties'])
    #
    # def test_get_schema_update(self):
    #     schema = self.controller.get_schema('update', self.topology_view)
    #     self.assertIsNotNone(schema)
    #     self.assertTrue('topology' in schema['properties'])
    #
    # def test_get_schema_edit(self):
    #     schema = self.controller.get_schema('edit', self.topology_view)
    #     self.assertIsNotNone(schema)
    #     self.assertTrue('topology' in schema['properties'])
    #
    # def test_validate_schema_create(self):
    #     body = self.create_body
    #     schema = self.controller.get_schema('topology:create', body)
    #     validator = jsonschema.Draft4Validator(schema)
    #     self.assertTrue(validator.is_valid(body))
    #
    # def test_validate_schema_edit(self):
    #     body = self.edit_body
    #     schema = self.controller.get_schema('topology:edit', body)
    #     validator = jsonschema.Draft4Validator(schema)
    #     self.assertTrue(validator.is_valid(body))

    # def test_show(self):
    #     result = self.controller.show(
    #         self.req, self.tenant_id, self.instance_id, self.topology_key)
    #     self.assertEqual(
    #         result.data(
    #             self.serialization_type)['topology'][self.topology_key],
    #         self.topology_view['topology'][self.topology_key])
    #     self.assertEqual(200, result.status)

    # def test_show_noexist(self):
    #     result = self.controller.show(self.req, self.tenant_id,
    #                                   self.instance_id,
    #                                   'this_key_doesnt_exist')
    #     self.assertEqual(404, result.status)
    #     self.assertIsNone(result.data(self.serialization_type))

    def test_create(self):
        datastore = 'mysql'
        body = {
            'topology': {
                'slave_of': [{'id': '07085bb9-59a3-40a3-9f10-dc24da644c37'}]
            }
        }
        result = self.controller.create(
            self.req, body, self.tenant_id, self.instance_id, datastore)
        self.assertEqual(200, result.status)
        result = self.controller.list(self.req, self.tenant_id,
                                      self.instance_id)
        data = result.data(self.serialization_type)
        self.assertEqual(data['topology'][datastore], body['topology'])

    def test_create_already_exists(self):
        result = self.controller.create(self.req, self.create_body,
                                        self.tenant_id, self.instance_id,
                                        self.topology_key)
        self.assertEqual(403, result.status)
        self.assertIsNone(result.data(self.serialization_type))

    def test_edit(self):
        meta_to_replace = {
            'topology': {
                'slave_of': [{'id': '07085bb9-59a3-40a3-9f10-dc24da644c37'}]
            }
        }
        result = self.controller.edit(self.req, meta_to_replace,
                                      self.tenant_id, self.instance_id,
                                      self.topology_key)
        self.assertEqual(200, result.status)
        result = self.controller.show(self.req, self.tenant_id,
                                      self.instance_id, self.topology_key)
        data = result.data(self.serialization_type)['topology']
        self.assertEqual(meta_to_replace['topology'], data[self.topology_key])

    def test_edit_noexists(self):
        meta_to_replace = {
            'topology': {
                'slave_of': [{'id': '07085bb9-59a3-40a3-9f10-dc24da644c37'}]
            }
        }
        result = self.controller.edit(self.req, meta_to_replace,
                                      self.tenant_id, self.instance_id,
                                      'this_key_doesnt_exist')
        self.assertEqual(404, result.status)
        self.assertIsNone(result.data(self.serialization_type))

    def test_delete(self):
        old_meta = self.controller.list(self.req, self.tenant_id,
                                        self.instance_id).data(
                                            self.serialization_type)
        result = self.controller.delete(self.req, self.tenant_id,
                                        self.instance_id, self.topology_key)
        # test response from delete
        self.assertEqual(200, result.status)
        new_meta = self.controller.list(self.req, self.tenant_id,
                                        self.instance_id).data(
                                            self.serialization_type)
        # test response code from list
        self.assertEqual(200, result.status)
        self.assertNotEqual(old_meta, new_meta)
        self.assertNotIn(self.topology_key, new_meta.keys())

    def test_delete_noexists(self):
        result = self.controller.delete(self.req, self.tenant_id,
                                        self.instance_id,
                                        'this_key_doesnt_exist')
        self.assertEqual(404, result.status)
        self.assertIsNone(result.data(self.serialization_type))
