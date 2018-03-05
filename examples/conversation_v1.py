from __future__ import print_function
import json
import os
from watson_developer_cloud import ConversationV1

conversation = ConversationV1(
    username='YOUR SERVICE USERNAME',
    password='YOUR SERVICE PASSWORD',
    version='2017-04-21')

# When you send multiple requests for the same conversation, include the
# context object from the previous response.
# response = conversation.message(workspace_id=workspace_id, message_input={
# 'text': 'turn the wipers on'},
#                                context=response['context'])
# print(json.dumps(response, indent=2))

#########################
# workspaces
#########################

response = conversation.create_workspace(name='test_workspace',
                                         description='Test workspace.',
                                         language='en',
                                         metadata={})
print(json.dumps(response, indent=2))

workspace_id = response['workspace_id']

response = conversation.get_workspace(workspace_id=workspace_id, export=True)
print(json.dumps(response, indent=2))

#  message
response = conversation.message(workspace_id=workspace_id, input={
    'text': 'What\'s the weather like?'})
print(json.dumps(response, indent=2))

response = conversation.list_workspaces()
print(json.dumps(response, indent=2))

response = conversation.update_workspace(workspace_id=workspace_id,
                                         description='Updated test workspace.')
print(json.dumps(response, indent=2))

# see cleanup section below for delete_workspace example

#########################
# intents
#########################

response = conversation.create_intent(workspace_id=workspace_id,
                                      intent='test_intent',
                                      description='Test intent.')
print(json.dumps(response, indent=2))

response = conversation.get_intent(workspace_id=workspace_id,
                                   intent='test_intent',
                                   export=True)
print(json.dumps(response, indent=2))

response = conversation.list_intents(workspace_id=workspace_id,
                                     export=True)
print(json.dumps(response, indent=2))

response = conversation.update_intent(workspace_id=workspace_id,
                                      intent='test_intent',
                                      new_intent='updated_test_intent',
                                      new_description='Updated test intent.')
print(json.dumps(response, indent=2))

# see cleanup section below for delete_intent example

#########################
# examples
#########################

response = conversation.create_example(workspace_id=workspace_id,
                                       intent='updated_test_intent',
                                       text='Gimme a pizza with pepperoni')
print(json.dumps(response, indent=2))

response = conversation.get_example(workspace_id=workspace_id,
                                    intent='updated_test_intent',
                                    text='Gimme a pizza with pepperoni')
print(json.dumps(response, indent=2))

response = conversation.list_examples(workspace_id=workspace_id,
                                      intent='updated_test_intent')
print(json.dumps(response, indent=2))

response = conversation.update_example(workspace_id=workspace_id,
                                       intent='updated_test_intent',
                                       text='Gimme a pizza with pepperoni',
                                       new_text='Gimme a pizza with pepperoni')
print(json.dumps(response, indent=2))

response = conversation.delete_example(workspace_id=workspace_id,
                                       intent='updated_test_intent',
                                       text='Gimme a pizza with pepperoni')
print(json.dumps(response, indent=2))

#########################
# counterexamples
#########################

response = conversation.create_counterexample(workspace_id=workspace_id,
                                              text='I want financial advice today.')
print(json.dumps(response, indent=2))

response = conversation.get_counterexample(workspace_id=workspace_id,
                                           text='I want financial advice today.')
print(json.dumps(response, indent=2))

response = conversation.list_counterexamples(workspace_id=workspace_id)
print(json.dumps(response, indent=2))

response = conversation.update_counterexample(workspace_id=workspace_id,
                                              text='I want financial advice today.',
                                              new_text='I want financial advice today.')
print(json.dumps(response, indent=2))

response = conversation.delete_counterexample(workspace_id=workspace_id,
                                              text='I want financial advice today.')
print(json.dumps(response, indent=2))

#########################
# entities
#########################

values = [{"value": "juice"}]
response = conversation.create_entity(workspace_id=workspace_id,
                                      entity='test_entity',
                                      description='A test entity.',
                                      values=values)
print(json.dumps(response, indent=2))

entities = [{
    'entity': 'pattern_entity',
    'values': [{
        'value': 'value0', 'patterns': ['\\d{6}\\w{1}\\d{7}'], 'value_type': 'patterns'
     },
     {'value': 'value1',
      'patterns': ['[-9][0-9][0-9][0-9][0-9]~! [1-9][1-9][1-9][1-9][1-9][1-9]'],
      'value_type': 'patterns'},
     {'value': 'value2',
      'patterns': ['[a-z-9]{17}'],
      'value_type': 'patterns'},
     {'value': 'value3',
      'patterns': [
           '\\d{3}(\\ |-)\\d{3}(\\ |-)\\d{4}',
           '\\(\\d{3}\\)(\\ |-)\\d{3}(\\ |-)\\d{4}'],
      'value_type': 'patterns'},
     {'value': 'value4',
      'patterns': ['\\b\\d{5}\\b'],
      'value_type': 'patterns'}]
}]
response = conversation.create_entity(workspace_id,
                                     entity=entities[0]['entity'],
                                     values=entities[0]['values'])
print(json.dumps(response, indent=2))

response = conversation.get_entity(workspace_id=workspace_id,
                                   entity='test_entity',
                                   export=True)
print(json.dumps(response, indent=2))

response = conversation.list_entities(workspace_id=workspace_id)
print(json.dumps(response, indent=2))

response = conversation.update_entity(workspace_id=workspace_id,
                                      entity='test_entity',
                                      new_description='An updated test entity.')
print(json.dumps(response, indent=2))

response = conversation.delete_entity(workspace_id=workspace_id,
                                      entity='test_entity')
print(json.dumps(response, indent=2))

#########################
# synonyms
#########################

values = [{"value": "orange juice"}]
conversation.create_entity(workspace_id, 'beverage', values=values)

response = conversation.create_synonym(workspace_id, 'beverage', 'orange juice', 'oj')
print(json.dumps(response, indent=2))

response = conversation.get_synonym(workspace_id, 'beverage', 'orange juice', 'oj')
print(json.dumps(response, indent=2))

response = conversation.list_synonyms(workspace_id, 'beverage', 'orange juice')
print(json.dumps(response, indent=2))

response = conversation.update_synonym(workspace_id, 'beverage', 'orange juice', 'oj', 'OJ')
print(json.dumps(response, indent=2))

response = conversation.delete_synonym(workspace_id, 'beverage', 'orange juice', 'OJ')
print(json.dumps(response, indent=2))

conversation.delete_entity(workspace_id, 'beverage')

#########################
# values
#########################

conversation.create_entity(workspace_id, 'test_entity')

response = conversation.create_value(workspace_id, 'test_entity', 'test')
print(json.dumps(response, indent=2))

response = conversation.get_value(workspace_id, 'test_entity', 'test')
print(json.dumps(response, indent=2))

response = conversation.list_values(workspace_id, 'test_entity')
print(json.dumps(response, indent=2))

response = conversation.update_value(workspace_id, 'test_entity', 'test', 'example')
print(json.dumps(response, indent=2))

response = conversation.delete_value(workspace_id, 'test_entity', 'example')
print(json.dumps(response, indent=2))

conversation.delete_entity(workspace_id, 'test_entity')

#########################
# logs
#########################

response = conversation.list_logs(workspace_id=workspace_id)
print(json.dumps(response, indent=2))

#########################
# clean-up
#########################

response = conversation.delete_intent(workspace_id=workspace_id,
                                      intent='updated_test_intent')
print(json.dumps(response, indent=2))

response = conversation.delete_workspace(workspace_id=workspace_id)
print(json.dumps(response, indent=2))
