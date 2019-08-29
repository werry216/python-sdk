import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('your apikey')
assistant = AssistantV2(
    version='2018-09-20',
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    url='https://gateway.watsonplatform.net/assistant/api',
    authenticator=authenticator)

#########################
# Sessions
#########################

session = assistant.create_session("<YOUR ASSISTANT ID>").get_result()
print(json.dumps(session, indent=2))

assistant.delete_session("<YOUR ASSISTANT ID>", "<YOUR SESSION ID>").get_result()

#########################
# Message
#########################

message = assistant.message(
    "<YOUR ASSISTANT ID>",
    "<YOUR SESSION ID>",
    input={'text': 'What\'s the weather like?'},
    context={
        'metadata': {
            'deployment': 'myDeployment'
        }
    }).get_result()
print(json.dumps(message, indent=2))
