# Copyright 2016 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from watson_developer_cloud.watson_developer_cloud_service import \
    WatsonDeveloperCloudService
import json


class NaturalLanguageUnderstandingV1(WatsonDeveloperCloudService):
    """
    All methods taking features use the feature classes
    from watson_developer_cloud/nlu/features/v1

    """
    base_url = 'https://gateway.watsonplatform.net'
    default_url = '{0}/natural-language-understanding/api'.format(base_url)
    latest_version = '2017-01-23'

    def __init__(self,
                 version,
                 url=default_url,
                 username=None,
                 password=None,
                 use_vcap_services=True):
        WatsonDeveloperCloudService.__init__(
            self, 'natural_language_understanding', url,
            username, password, use_vcap_services)
        self.version = version

    def analyze(self, featureList, text=None, url=None, html=None,
                clean=True, xpath=None, fallback_to_raw=True,
                return_analyzed_text=False, language=None):
        body = {'clean': clean, 'fallback_to_raw': fallback_to_raw,
                'return_analyzed_text': return_analyzed_text}
        if xpath:
            body['xpath'] = xpath

        if language:
            body['language']=language

        feature_dict = {}
        for feature in featureList:
            feature_dict[feature.name()] = feature.toDict()
        body['features'] = feature_dict

        if text:
            body['text'] = text
        elif url:
            body['url'] = url
        elif html:
            body['html'] = html
        else:
            msg = "html, text, or url must have content"
            raise ValueError(msg)

        if len(featureList) < 1:
            raise ValueError("Must supply at least one feature")

        return self.request(method='POST', url='/v1/analyze',
                            params={"version": self.version},
                            headers={'content-type': 'application/json'},
                            data=body,
                            accept_json=True)