# coding: utf-8
from unittest import TestCase
import os
import watson_developer_cloud
import random
import pytest

@pytest.mark.skipif(
    os.getenv('VCAP_SERVICES') is None, reason='requires VCAP_SERVICES')
class Discoveryv1(TestCase):
    def setUp(self):
        self.discovery = watson_developer_cloud.DiscoveryV1(
            version='2017-10-16',
            username="YOUR SERVICE USERNAME",
            password="YOUR SERVICE PASSWORD")
        self.discovery.set_default_headers({
            'X-Watson-Learning-Opt-Out': '1',
            'X-Watson-Test': '1'
        })
        self.environment_id = 'e15f6424-f887-4f50-b4ea-68267c36fc9c'  # This environment is created for integration testing
        collections = self.discovery.list_collections(self.environment_id)['collections']
        self.collection_id = collections[0]['collection_id']

    def tearDown(self):
        collections = self.discovery.list_collections(self.environment_id)['collections']
        for collection in collections:
            if collection['name'] != 'DO-NOT-DELETE':
                self.discovery.delete_collection(self.environment_id, collection['collection_id'])

    def test_environments(self):
        envs = self.discovery.list_environments()
        assert envs is not None
        env = self.discovery.get_environment(
            envs['environments'][0]['environment_id'])
        assert env is not None
        fields = self.discovery.list_fields(self.environment_id,
                                            self.collection_id)
        assert fields is not None

    def test_configurations(self):
        configs = self.discovery.list_configurations(self.environment_id)
        assert configs is not None

        name = 'test' + random.choice('ABCDEFGHIJKLMNOPQ')
        new_configuration_id = self.discovery.create_configuration(
            self.environment_id, name,
            'creating new config for python sdk')['configuration_id']
        assert new_configuration_id is not None
        self.discovery.get_configuration(self.environment_id,
                                         new_configuration_id)

        updated_config = self.discovery.update_configuration(
            self.environment_id, new_configuration_id, 'lala')
        assert updated_config['name'] == 'lala'

        deleted_config = self.discovery.delete_configuration(
            self.environment_id, new_configuration_id)
        assert deleted_config['status'] == 'deleted'

    def test_collections_and_expansions(self):
        name = 'Example collection for python' + random.choice('ABCDEFGHIJKLMNOPQ')
        new_collection_id = self.discovery.create_collection(
            self.environment_id,
            name,
            description="Integration test for python sdk")['collection_id']
        assert new_collection_id is not None

        self.discovery.get_collection(self.environment_id, new_collection_id)
        updated_collection = self.discovery.update_collection(
            self.environment_id, new_collection_id, name, description='Updating description')
        assert updated_collection['description'] == 'Updating description'

        self.discovery.create_expansions(self.environment_id,
                                         new_collection_id, [{
                                             'input_terms': ['a'],
                                             'expanded_terms': ['aa']
                                         }])
        expansions = self.discovery.list_expansions(self.environment_id,
                                                    new_collection_id)
        assert expansions['expansions']
        self.discovery.delete_expansions(self.environment_id,
                                         new_collection_id)

        deleted_collection = self.discovery.delete_collection(
            self.environment_id, new_collection_id)
        assert deleted_collection['status'] == 'deleted'

    def test_documents(self):
        with open(os.path.join(os.path.dirname(__file__), '../../resources/simple.html'), 'r') as fileinfo:
            add_doc = self.discovery.add_document(
                environment_id=self.environment_id,
                collection_id=self.collection_id,
                file=fileinfo)
        assert add_doc['document_id'] is not None

        doc_status = self.discovery.get_document_status(
            self.environment_id, self.collection_id, add_doc['document_id'])
        assert doc_status is not None

        with open(os.path.join(os.path.dirname(__file__), '../../resources/simple.html'), 'r') as fileinfo:
            update_doc = self.discovery.update_document(
                self.environment_id,
                self.collection_id,
                add_doc['document_id'],
                file=fileinfo,
                filename='newname.html')
        assert update_doc is not None
        delete_doc = self.discovery.delete_document(
            self.environment_id, self.collection_id, add_doc['document_id'])
        assert delete_doc['status'] == 'deleted'

    def test_queries(self):
        query_results = self.discovery.query(
            self.environment_id,
            self.collection_id,
            filter='extracted_metadata.sha1::9181d244*',
            return_fields='extracted_metadata.sha1')
        assert query_results is not None

    def test_credentials(self):
        credential_details = {
            'credential_type': 'username_password',
            'url': 'https://login.salesforce.com',
            'username': 'user@email.com',
            'password': 'xxx'
        }
        credentials = self.discovery.create_credentials(self.environment_id,
                                                        'salesforce',
                                                        credential_details)
        assert credentials['credential_id'] is not None
        credential_id = credentials['credential_id']

        get_credentials = self.discovery.get_credentials(self.environment_id, credential_id)
        assert get_credentials['credential_id'] == credential_id

        list_credentials = self.discovery.list_credentials(self.environment_id)
        assert list_credentials is not None

        new_credential_details = {
            'credential_type': 'username_password',
            'url': 'https://logo.salesforce.com',
            'username': 'user@email.com',
            'password': 'xxx'
        }
        updated_credentials = self.discovery.update_credentials(self.environment_id, credential_id, 'salesforce', new_credential_details)
        assert updated_credentials is not None

        get_credentials = self.discovery.get_credentials(self.environment_id, credentials['credential_id'])
        assert get_credentials['credential_details']['url'] == new_credential_details['url']

        delete_credentials = self.discovery.delete_credentials(self.environment_id, credential_id)
        assert delete_credentials['credential_id'] is not None
