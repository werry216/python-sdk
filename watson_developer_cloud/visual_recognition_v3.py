# coding: utf-8

# Copyright 2017 IBM All Rights Reserved.
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
"""
**Important**: As of September 8, 2017, the beta period for Similarity Search is closed.
For more information, see [Visual Recognition API – Similarity Search
Update](https://www.ibm.com/blogs/bluemix/2017/08/visual-recognition-api-similarity-search-update).

The IBM Watson Visual Recognition service uses deep learning algorithms to identify
scenes, objects, and faces  in images you upload to the service. You can create and train
a custom classifier to identify subjects that suit your needs.

**Tip**: To test calls to the **Custom classifiers** methods with the API explorer,
provide your `api_key` from your Bluemix service instance.
"""

import json
from .watson_developer_cloud_service import WatsonDeveloperCloudService

##############################################################################
# Service
##############################################################################


class VisualRecognitionV3(WatsonDeveloperCloudService):
    """The Visual Recognition V3 service."""

    default_url = 'https://gateway-a.watsonplatform.net/visual-recognition/api'
    latest_version = '2016-05-20'

    def __init__(self, version, url=default_url, api_key=None):
        """
        Construct a new client for the Visual Recognition service.

        :param str version: The API version date to use with the service, in
               "YYYY-MM-DD" format. Whenever the API is changed in a backwards
               incompatible way, a new minor version of the API is released.
               The service uses the API version for the date you specify, or
               the most recent version before that date. Note that you should
               not programmatically specify the current date at runtime, in
               case the API has been updated since your application's release.
               Instead, specify a version date that is compatible with your
               application, and don't change it until your application is
               ready for a later version.

        :param str url: The base url to use when contacting the service (e.g.
               "https://gateway.watsonplatform.net/visual-recognition/api").
               The base url may differ between Bluemix regions.

        :param str api_key: The API Key used to authenticate.

        """

        WatsonDeveloperCloudService.__init__(
            self,
            vcap_services_name='watson_vision_combined',
            url=url,
            api_key=api_key,
            use_vcap_services=True)
        self.version = version

    #########################
    # classify
    #########################

    def classify(self,
                 images_file=None,
                 parameters=None,
                 accept_language=None,
                 images_file_content_type=None,
                 images_filename=None):
        """
        Classify images.

        :param file images_file: An image file (.jpg, .png) or .zip file with images. Include no more than 20 images and limit the .zip file to 5 MB. You can also include images with the `url` property in the **parameters** object.
        :param str parameters: Specifies input parameters. The parameter can include these inputs in a JSON object:  - url: A string with the image URL to analyze. You can also include images in the **images_file** parameter. - classifier_ids: An array of classifier IDs to classify the images against. - owners: An array with the values IBM, me, or both to specify which classifiers to run. - threshold: A floating point value that specifies the minimum score a class must have to be displayed in the response.  For example: {\"url\": \"...\", \"classifier_ids\": [\"...\",\"...\"], \"owners\": [\"IBM\", \"me\"], \"threshold\": 0.4}.
        :param str accept_language: Specifies the language of the output class names.  Can be `en` (English), `ar` (Arabic), `de` (German), `es` (Spanish), `it` (Italian), `ja` (Japanese), or `ko` (Korean).  Classes for which no translation is available are omitted.  The response might not be in the specified language under these conditions: - English is returned when the requested language is not supported. - Classes are not returned when there is no translation for them. - Custom classifiers returned with this method return tags in the language of the custom classifier.
        :param str images_file_content_type: The content type of images_file.
        :param str images_filename: The filename for images_file.
        :return: A `dict` containing the `ClassifiedImages` response.
        :rtype: dict
        """
        headers = {'Accept-Language': accept_language}
        params = {'version': self.version}
        images_file_tuple = None
        if images_file:
            if not images_filename and hasattr(images_file, 'name'):
                images_filename = images_file.name
            mime_type = images_file_content_type or 'application/octet-stream'
            images_file_tuple = (images_filename, images_file, mime_type)
        parameters_tuple = None
        if parameters:
            parameters_tuple = (None, parameters, 'text/plain')
        response = self.request(
            method='POST',
            url='/v3/classify',
            headers=headers,
            params=params,
            files={
                'images_file': images_file_tuple,
                'parameters': parameters_tuple
            },
            accept_json=True)
        return response

    def detect_faces(self,
                     images_file=None,
                     parameters=None,
                     images_file_content_type=None,
                     images_filename=None):
        """
        Detect faces in an image.

        :param file images_file: An image file (.jpg, .png) or .zip file with images. Include no more than 15 images. You can also include images with the `url` property in the **parameters** object.  All faces are detected, but if there are more than 10 faces in an image, age and gender confidence scores might return scores of 0.
        :param str parameters: A JSON string containing the image URL to analyze.   For example: {\"url\": \"...\"}.
        :param str images_file_content_type: The content type of images_file.
        :param str images_filename: The filename for images_file.
        :return: A `dict` containing the `DetectedFaces` response.
        :rtype: dict
        """
        params = {'version': self.version}
        images_file_tuple = None
        if images_file:
            if not images_filename and hasattr(images_file, 'name'):
                images_filename = images_file.name
            mime_type = images_file_content_type or 'application/octet-stream'
            images_file_tuple = (images_filename, images_file, mime_type)
        parameters_tuple = None
        if parameters:
            parameters_tuple = (None, parameters, 'text/plain')
        response = self.request(
            method='POST',
            url='/v3/detect_faces',
            params=params,
            files={
                'images_file': images_file_tuple,
                'parameters': parameters_tuple
            },
            accept_json=True)
        return response

    #########################
    # customClassifiers
    #########################

    def create_classifier(self,
                          name,
                          **kwargs):
        """
        Create a classifier.

        :param str name: The name of the new classifier. Cannot contain special characters.
        :param file <NAME>_positive_examples: A compressed (.zip) file of images that depict the visual subject for a class within the new classifier. Must contain a minimum of 10 images. The swagger limits you to training only one class. To train more classes, use the API functionality.
        :param file negative_examples: A compressed (.zip) file of images that do not depict the visual subject of any of the classes of the new classifier. Must contain a minimum of 10 images.
        :return: A `dict` containing the `Classifier` response.
        :rtype: dict
        """
        if name is None:
            raise ValueError('name must be provided')
        params = {'version': self.version}
        data = {'name': name}
        response = self.request(
            method='POST',
            url='/v3/classifiers',
            params=params,
            data=data,
            files=kwargs,
            accept_json=True)
        return response

    def delete_classifier(self, classifier_id):
        """
        Delete a custom classifier.

        :param str classifier_id: The ID of the classifier.
        :rtype: None
        """
        if classifier_id is None:
            raise ValueError('classifier_id must be provided')
        params = {'version': self.version}
        self.request(
            method='DELETE',
            url='/v3/classifiers/{0}'.format(classifier_id),
            params=params,
            accept_json=True)
        return None

    def get_classifier(self, classifier_id):
        """
        Retrieve information about a custom classifier.

        :param str classifier_id: The ID of the classifier.
        :return: A `dict` containing the `Classifier` response.
        :rtype: dict
        """
        if classifier_id is None:
            raise ValueError('classifier_id must be provided')
        params = {'version': self.version}
        response = self.request(
            method='GET',
            url='/v3/classifiers/{0}'.format(classifier_id),
            params=params,
            accept_json=True)
        return response

    def list_classifiers(self, verbose=None):
        """
        Retrieve a list of custom classifiers.

        :param bool verbose: Specify true to return classifier details. Omit this parameter to return a brief list of classifiers.
        :return: A `dict` containing the `Classifiers` response.
        :rtype: dict
        """
        params = {'version': self.version, 'verbose': verbose}
        response = self.request(
            method='GET',
            url='/v3/classifiers',
            params=params,
            accept_json=True)
        return response

    def update_classifier(self,
                          classifier_id,
                          **kwargs):
        """
        Update a classifier.

        :param str classifier_id: The ID of the classifier.
        :param file <NAME>_positive_examples: A compressed (.zip) file of images that depict the visual subject for a class within the classifier. Must contain a minimum of 10 images.
        :param file negative_examples: A compressed (.zip) file of images that do not depict the visual subject of any of the classes of the new classifier. Must contain a minimum of 10 images.
        :return: A `dict` containing the `Classifier` response.
        :rtype: dict
        """
        if classifier_id is None:
            raise ValueError('classifier_id must be provided')
        params = {'version': self.version}
        response = self.request(
            method='POST',
            url='/v3/classifiers/{0}'.format(classifier_id),
            params=params,
            files=kwargs,
            accept_json=True)
        return response

    #########################
    # collections
    #########################

    def create_collection(self, name, disregard=None, disregard_filename=None):
        """
        Create a new collection - beta.

        Create a new collection of images to search. You can create a maximum of 5
        collections.

        :param str name: The name of the new collection. The name can be a maximum of 128 UTF8 characters, with no spaces.
        :param file disregard: Disregard this parameter. In order for the swagger spec to work, there needs to be at least one file in a multipart/form-data call. Uploading a file using this parameter has no impact on the collection.
        :param str disregard_filename: The filename for disregard.
        :return: A `dict` containing the `Collection` response.
        :rtype: dict
        """
        if name is None:
            raise ValueError('name must be provided')
        params = {'version': self.version}
        name_tuple = (None, name, 'text/plain')
        disregard_tuple = None
        if disregard:
            if not disregard_filename and hasattr(disregard, 'name'):
                disregard_filename = disregard.name
            mime_type = 'application/octet-stream'
            disregard_tuple = (disregard_filename, disregard, mime_type)
        response = self.request(
            method='POST',
            url='/v3/collections',
            params=params,
            files={'name': name_tuple,
                   'disregard': disregard_tuple},
            accept_json=True)
        return response

    def find_similar_images(self,
                            collection_id,
                            image_file,
                            limit=None,
                            image_file_content_type=None,
                            image_filename=None):
        """
        Find similar images - beta.

        :param str collection_id: The ID of your collection.
        :param file image_file: The image file (.jpg or .png) of the image to search against the collection.
        :param int limit: The number of similar results you want returned. Default limit is 10 results, you can specify a maximum limit of 100 results.
        :param str image_file_content_type: The content type of image_file.
        :param str image_filename: The filename for image_file.
        :return: A `dict` containing the `SimilarImages` response.
        :rtype: dict
        """
        if collection_id is None:
            raise ValueError('collection_id must be provided')
        if image_file is None:
            raise ValueError('image_file must be provided')
        params = {'version': self.version, 'limit': limit}
        if not image_filename and hasattr(image_file, 'name'):
            image_filename = image_file.name
        mime_type = image_file_content_type or 'application/octet-stream'
        image_file_tuple = (image_filename, image_file, mime_type)
        response = self.request(
            method='POST',
            url='/v3/collections/{0}/find_similar'.format(collection_id),
            params=params,
            files={'image_file': image_file_tuple},
            accept_json=True)
        return response

    def get_collection(self, collection_id):
        """
        Retrieve collection details - beta.

        Retrieve information about a specific collection. Only user-created collections
        can be specified.

        :param str collection_id: The ID of your collection.
        :return: A `dict` containing the `Collection` response.
        :rtype: dict
        """
        if collection_id is None:
            raise ValueError('collection_id must be provided')
        params = {'version': self.version}
        response = self.request(
            method='GET',
            url='/v3/collections/{0}'.format(collection_id),
            params=params,
            accept_json=True)
        return response

    def list_collections(self):
        """
        List all custom collections - beta.

        :return: A `dict` containing the `Collections` response.
        :rtype: dict
        """
        params = {'version': self.version}
        response = self.request(
            method='GET',
            url='/v3/collections',
            params=params,
            accept_json=True)
        return response

    #########################
    # collectionImages
    #########################

    def add_collection_image(self,
                             collection_id,
                             image_file,
                             metadata=None,
                             image_file_content_type=None,
                             image_filename=None,
                             metadata_filename=None):
        """
        Add images to a collection - beta.

        :param str collection_id: The ID of your collection.
        :param file image_file: The image file (.jpg or .png) of the image to add to the collection. Maximum file size of 2 MB.
        :param file metadata: A json object file that adds metadata to the image. Maximum 2 KB of metadata for each image.
        :param str image_file_content_type: The content type of image_file.
        :param str image_filename: The filename for image_file.
        :param str metadata_filename: The filename for metadata.
        :return: A `dict` containing the `CollectionImages` response.
        :rtype: dict
        """
        if collection_id is None:
            raise ValueError('collection_id must be provided')
        if image_file is None:
            raise ValueError('image_file must be provided')
        params = {'version': self.version}
        if not image_filename and hasattr(image_file, 'name'):
            image_filename = image_file.name
        if not image_filename:
            raise ValueError('image_filename must be provided')
        mime_type = image_file_content_type or 'application/octet-stream'
        image_file_tuple = (image_filename, image_file, mime_type)
        metadata_tuple = None
        if metadata:
            if not metadata_filename and hasattr(metadata, 'name'):
                metadata_filename = metadata.name
            mime_type = 'application/octet-stream'
            metadata_tuple = (metadata_filename, metadata, mime_type)
        response = self.request(
            method='POST',
            url='/v3/collections/{0}/images'.format(collection_id),
            params=params,
            files={'image_file': image_file_tuple,
                   'metadata': metadata_tuple},
            accept_json=True)
        return response

    def delete_collection(self, collection_id):
        """
        Delete a collection - beta.

        :param str collection_id: The ID of your collection.
        :rtype: None
        """
        if collection_id is None:
            raise ValueError('collection_id must be provided')
        params = {'version': self.version}
        self.request(
            method='DELETE',
            url='/v3/collections/{0}'.format(collection_id),
            params=params,
            accept_json=True)
        return None

    def delete_collection_image(self, collection_id, image_id):
        """
        Delete an image - beta.

        :param str collection_id: The ID of your collection.
        :param str image_id: The ID of your image.
        :rtype: None
        """
        if collection_id is None:
            raise ValueError('collection_id must be provided')
        if image_id is None:
            raise ValueError('image_id must be provided')
        params = {'version': self.version}
        self.request(
            method='DELETE',
            url='/v3/collections/{0}/images/{1}'.format(collection_id,
                                                        image_id),
            params=params,
            accept_json=True)
        return None

    def delete_image_metadata(self, collection_id, image_id):
        """
        Delete image metadata - beta.

        :param str collection_id: The ID of your collection.
        :param str image_id: The ID of your image.
        :rtype: None
        """
        if collection_id is None:
            raise ValueError('collection_id must be provided')
        if image_id is None:
            raise ValueError('image_id must be provided')
        params = {'version': self.version}
        self.request(
            method='DELETE',
            url='/v3/collections/{0}/images/{1}/metadata'.format(
                collection_id, image_id),
            params=params,
            accept_json=True)
        return None

    def get_collection_image(self, collection_id, image_id):
        """
        List image details - beta.

        :param str collection_id: The ID of your collection.
        :param str image_id: The ID of your image.
        :return: A `dict` containing the `CollectionImage` response.
        :rtype: dict
        """
        if collection_id is None:
            raise ValueError('collection_id must be provided')
        if image_id is None:
            raise ValueError('image_id must be provided')
        params = {'version': self.version}
        response = self.request(
            method='GET',
            url='/v3/collections/{0}/images/{1}'.format(collection_id,
                                                        image_id),
            params=params,
            accept_json=True)
        return response

    def list_collection_images(self, collection_id):
        """
        List 100 images in a collection - beta.

        :param str collection_id: The ID of your collection.
        :return: A `dict` containing the `CollectionImages` response.
        :rtype: dict
        """
        if collection_id is None:
            raise ValueError('collection_id must be provided')
        params = {'version': self.version}
        response = self.request(
            method='GET',
            url='/v3/collections/{0}/images'.format(collection_id),
            params=params,
            accept_json=True)
        return response


##############################################################################
# Models
##############################################################################


class Class(object):
    """
    A category within a classifier.

    :attr str class_name: The name of the class.
    """

    def __init__(self, class_name):
        """
        Initialize a Class object.

        :param str class_name: The name of the class.
        """
        self.class_name = class_name

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Class object from a json dictionary."""
        args = {}
        if 'class' in _dict:
            args['class_name'] = _dict['class']
        else:
            raise ValueError(
                'Required property \'class\' not present in Class JSON')
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'class_name') and self.class_name is not None:
            _dict['class'] = self.class_name
        return _dict

    def __str__(self):
        """Return a `str` version of this Class object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class ClassResult(object):
    """
    Result of a class within a classifier.

    :attr str class_name: The name of the class.
    :attr float score: (optional) Confidence score for the property. Scores range from 0-1, with a higher score indicating greater correlation.
    :attr str type_hierarchy: (optional) Knowledge graph of the property. For example, `People/Leaders/Presidents/USA/Barack Obama`. Included only if identified.
    """

    def __init__(self, class_name, score=None, type_hierarchy=None):
        """
        Initialize a ClassResult object.

        :param str class_name: The name of the class.
        :param float score: (optional) Confidence score for the property. Scores range from 0-1, with a higher score indicating greater correlation.
        :param str type_hierarchy: (optional) Knowledge graph of the property. For example, `People/Leaders/Presidents/USA/Barack Obama`. Included only if identified.
        """
        self.class_name = class_name
        self.score = score
        self.type_hierarchy = type_hierarchy

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ClassResult object from a json dictionary."""
        args = {}
        if 'class' in _dict:
            args['class_name'] = _dict['class']
        else:
            raise ValueError(
                'Required property \'class\' not present in ClassResult JSON')
        if 'score' in _dict:
            args['score'] = _dict['score']
        if 'type_hierarchy' in _dict:
            args['type_hierarchy'] = _dict['type_hierarchy']
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'class_name') and self.class_name is not None:
            _dict['class'] = self.class_name
        if hasattr(self, 'score') and self.score is not None:
            _dict['score'] = self.score
        if hasattr(self, 'type_hierarchy') and self.type_hierarchy is not None:
            _dict['type_hierarchy'] = self.type_hierarchy
        return _dict

    def __str__(self):
        """Return a `str` version of this ClassResult object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class ClassifiedImage(object):
    """
    Classifier results for one image.

    :attr str source_url: (optional) Source of the image before any redirects. Not returned when the image is uploaded.
    :attr str resolved_url: (optional) Fully resolved URL of the image after redirects are followed. Not returned when the image is uploaded.
    :attr str image: (optional) Relative path of the image file if uploaded directly. Not returned when the image is passed by URL.
    :attr ErrorInfo error: (optional)
    :attr list[ClassifierResult] classifiers:
    """

    def __init__(self,
                 classifiers,
                 source_url=None,
                 resolved_url=None,
                 image=None,
                 error=None):
        """
        Initialize a ClassifiedImage object.

        :param list[ClassifierResult] classifiers:
        :param str source_url: (optional) Source of the image before any redirects. Not returned when the image is uploaded.
        :param str resolved_url: (optional) Fully resolved URL of the image after redirects are followed. Not returned when the image is uploaded.
        :param str image: (optional) Relative path of the image file if uploaded directly. Not returned when the image is passed by URL.
        :param ErrorInfo error: (optional)
        """
        self.source_url = source_url
        self.resolved_url = resolved_url
        self.image = image
        self.error = error
        self.classifiers = classifiers

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ClassifiedImage object from a json dictionary."""
        args = {}
        if 'source_url' in _dict:
            args['source_url'] = _dict['source_url']
        if 'resolved_url' in _dict:
            args['resolved_url'] = _dict['resolved_url']
        if 'image' in _dict:
            args['image'] = _dict['image']
        if 'error' in _dict:
            args['error'] = ErrorInfo._from_dict(_dict['error'])
        if 'classifiers' in _dict:
            args['classifiers'] = [
                ClassifierResult._from_dict(x) for x in _dict['classifiers']
            ]
        else:
            raise ValueError(
                'Required property \'classifiers\' not present in ClassifiedImage JSON'
            )
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'source_url') and self.source_url is not None:
            _dict['source_url'] = self.source_url
        if hasattr(self, 'resolved_url') and self.resolved_url is not None:
            _dict['resolved_url'] = self.resolved_url
        if hasattr(self, 'image') and self.image is not None:
            _dict['image'] = self.image
        if hasattr(self, 'error') and self.error is not None:
            _dict['error'] = self.error._to_dict()
        if hasattr(self, 'classifiers') and self.classifiers is not None:
            _dict['classifiers'] = [x._to_dict() for x in self.classifiers]
        return _dict

    def __str__(self):
        """Return a `str` version of this ClassifiedImage object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class ClassifiedImages(object):
    """
    Classify results for multiple images.

    :attr int images_processed: (optional) Number of images processed for the API call.
    :attr list[ClassifiedImage] images: The array of classified images.
    :attr list[WarningInfo] warnings: (optional) Information about what might cause less than optimal output. For example, a request sent with a corrupt .zip file and a list of image URLs will still complete, but does not return the expected output. Not returned when there is no warning.
    """

    def __init__(self, images, images_processed=None, warnings=None):
        """
        Initialize a ClassifiedImages object.

        :param list[ClassifiedImage] images: The array of classified images.
        :param int images_processed: (optional) Number of images processed for the API call.
        :param list[WarningInfo] warnings: (optional) Information about what might cause less than optimal output. For example, a request sent with a corrupt .zip file and a list of image URLs will still complete, but does not return the expected output. Not returned when there is no warning.
        """
        self.images_processed = images_processed
        self.images = images
        self.warnings = warnings

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ClassifiedImages object from a json dictionary."""
        args = {}
        if 'images_processed' in _dict:
            args['images_processed'] = _dict['images_processed']
        if 'images' in _dict:
            args['images'] = [
                ClassifiedImage._from_dict(x) for x in _dict['images']
            ]
        else:
            raise ValueError(
                'Required property \'images\' not present in ClassifiedImages JSON'
            )
        if 'warnings' in _dict:
            args['warnings'] = [
                WarningInfo._from_dict(x) for x in _dict['warnings']
            ]
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self,
                   'images_processed') and self.images_processed is not None:
            _dict['images_processed'] = self.images_processed
        if hasattr(self, 'images') and self.images is not None:
            _dict['images'] = [x._to_dict() for x in self.images]
        if hasattr(self, 'warnings') and self.warnings is not None:
            _dict['warnings'] = [x._to_dict() for x in self.warnings]
        return _dict

    def __str__(self):
        """Return a `str` version of this ClassifiedImages object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class Classifier(object):
    """
    Information about a classifier.

    :attr str classifier_id: The ID of the classifier.
    :attr str name: The name of the classifier.
    :attr str owner: (optional) Unique ID of the account who owns the classifier.
    :attr str status: (optional) The training status of classifier.
    :attr str explanation: (optional) If classifier training has failed, this field may explain why.
    :attr datetime created: (optional) The time and date when classifier was created.
    :attr list[Class] classes: (optional) An array of classes that define a classifier.
    """

    def __init__(self,
                 classifier_id,
                 name,
                 owner=None,
                 status=None,
                 explanation=None,
                 created=None,
                 classes=None):
        """
        Initialize a Classifier object.

        :param str classifier_id: The ID of the classifier.
        :param str name: The name of the classifier.
        :param str owner: (optional) Unique ID of the account who owns the classifier.
        :param str status: (optional) The training status of classifier.
        :param str explanation: (optional) If classifier training has failed, this field may explain why.
        :param datetime created: (optional) The time and date when classifier was created.
        :param list[Class] classes: (optional) An array of classes that define a classifier.
        """
        self.classifier_id = classifier_id
        self.name = name
        self.owner = owner
        self.status = status
        self.explanation = explanation
        self.created = created
        self.classes = classes

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Classifier object from a json dictionary."""
        args = {}
        if 'classifier_id' in _dict:
            args['classifier_id'] = _dict['classifier_id']
        else:
            raise ValueError(
                'Required property \'classifier_id\' not present in Classifier JSON'
            )
        if 'name' in _dict:
            args['name'] = _dict['name']
        else:
            raise ValueError(
                'Required property \'name\' not present in Classifier JSON')
        if 'owner' in _dict:
            args['owner'] = _dict['owner']
        if 'status' in _dict:
            args['status'] = _dict['status']
        if 'explanation' in _dict:
            args['explanation'] = _dict['explanation']
        if 'created' in _dict:
            args['created'] = _dict['created']
        if 'classes' in _dict:
            args['classes'] = [Class._from_dict(x) for x in _dict['classes']]
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'classifier_id') and self.classifier_id is not None:
            _dict['classifier_id'] = self.classifier_id
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'owner') and self.owner is not None:
            _dict['owner'] = self.owner
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status
        if hasattr(self, 'explanation') and self.explanation is not None:
            _dict['explanation'] = self.explanation
        if hasattr(self, 'created') and self.created is not None:
            _dict['created'] = self.created
        if hasattr(self, 'classes') and self.classes is not None:
            _dict['classes'] = [x._to_dict() for x in self.classes]
        return _dict

    def __str__(self):
        """Return a `str` version of this Classifier object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class ClassifierResult(object):
    """
    Classifier and score combination.

    :attr str name: Name of the classifier.
    :attr str classifier_id: Classifier ID.  Only returned if custom classifier.
    :attr list[ClassResult] classes: An array of classes within a classifier.
    """

    def __init__(self, name, classifier_id, classes):
        """
        Initialize a ClassifierResult object.

        :param str name: Name of the classifier.
        :param str classifier_id: Classifier ID.  Only returned if custom classifier.
        :param list[ClassResult] classes: An array of classes within a classifier.
        """
        self.name = name
        self.classifier_id = classifier_id
        self.classes = classes

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ClassifierResult object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict['name']
        else:
            raise ValueError(
                'Required property \'name\' not present in ClassifierResult JSON'
            )
        if 'classifier_id' in _dict:
            args['classifier_id'] = _dict['classifier_id']
        else:
            raise ValueError(
                'Required property \'classifier_id\' not present in ClassifierResult JSON'
            )
        if 'classes' in _dict:
            args['classes'] = [
                ClassResult._from_dict(x) for x in _dict['classes']
            ]
        else:
            raise ValueError(
                'Required property \'classes\' not present in ClassifierResult JSON'
            )
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'classifier_id') and self.classifier_id is not None:
            _dict['classifier_id'] = self.classifier_id
        if hasattr(self, 'classes') and self.classes is not None:
            _dict['classes'] = [x._to_dict() for x in self.classes]
        return _dict

    def __str__(self):
        """Return a `str` version of this ClassifierResult object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class Classifiers(object):
    """
    Verbose list of classifiers retrieved in the GET v2/classifiers call.

    :attr list[Classifier] classifiers:
    """

    def __init__(self, classifiers):
        """
        Initialize a Classifiers object.

        :param list[Classifier] classifiers:
        """
        self.classifiers = classifiers

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Classifiers object from a json dictionary."""
        args = {}
        if 'classifiers' in _dict:
            args['classifiers'] = [
                Classifier._from_dict(x) for x in _dict['classifiers']
            ]
        else:
            raise ValueError(
                'Required property \'classifiers\' not present in Classifiers JSON'
            )
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'classifiers') and self.classifiers is not None:
            _dict['classifiers'] = [x._to_dict() for x in self.classifiers]
        return _dict

    def __str__(self):
        """Return a `str` version of this Classifiers object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class Collection(object):
    """
    success.

    :attr str collection_id: (optional) The ID of the collection.
    :attr str name: The name of the collection.
    :attr datetime created: The date the collection was created.
    :attr int images: The number of images in the collection.
    :attr str status: The status of collection creation.
    :attr int capacity: The number of images possible in the collection.
    """

    def __init__(self,
                 name,
                 created,
                 images,
                 status,
                 capacity,
                 collection_id=None):
        """
        Initialize a Collection object.

        :param str name: The name of the collection.
        :param datetime created: The date the collection was created.
        :param int images: The number of images in the collection.
        :param str status: The status of collection creation.
        :param int capacity: The number of images possible in the collection.
        :param str collection_id: (optional) The ID of the collection.
        """
        self.collection_id = collection_id
        self.name = name
        self.created = created
        self.images = images
        self.status = status
        self.capacity = capacity

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Collection object from a json dictionary."""
        args = {}
        if 'collection_id' in _dict:
            args['collection_id'] = _dict['collection_id']
        if 'name' in _dict:
            args['name'] = _dict['name']
        else:
            raise ValueError(
                'Required property \'name\' not present in Collection JSON')
        if 'created' in _dict:
            args['created'] = _dict['created']
        else:
            raise ValueError(
                'Required property \'created\' not present in Collection JSON')
        if 'images' in _dict:
            args['images'] = _dict['images']
        else:
            raise ValueError(
                'Required property \'images\' not present in Collection JSON')
        if 'status' in _dict:
            args['status'] = _dict['status']
        else:
            raise ValueError(
                'Required property \'status\' not present in Collection JSON')
        if 'capacity' in _dict:
            args['capacity'] = _dict['capacity']
        else:
            raise ValueError(
                'Required property \'capacity\' not present in Collection JSON')
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'collection_id') and self.collection_id is not None:
            _dict['collection_id'] = self.collection_id
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'created') and self.created is not None:
            _dict['created'] = self.created
        if hasattr(self, 'images') and self.images is not None:
            _dict['images'] = self.images
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status
        if hasattr(self, 'capacity') and self.capacity is not None:
            _dict['capacity'] = self.capacity
        return _dict

    def __str__(self):
        """Return a `str` version of this Collection object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class CollectionImage(object):
    """
    An image contained within an image collection.

    :attr str image_id: Unique ID of the image. Save this to add or remove it from the collection.
    :attr datetime created: Date the image was added to the collection.
    :attr str image_file: File name of the image.
    :attr object metadata: Any metadata associated with the image.
    :attr float score: (optional) The confidence level of the match with similar images. Provided only when searching for similar images.
    """

    def __init__(self, image_id, created, image_file, metadata, score=None):
        """
        Initialize a CollectionImage object.

        :param str image_id: Unique ID of the image. Save this to add or remove it from the collection.
        :param datetime created: Date the image was added to the collection.
        :param str image_file: File name of the image.
        :param object metadata: Any metadata associated with the image.
        :param float score: (optional) The confidence level of the match with similar images. Provided only when searching for similar images.
        """
        self.image_id = image_id
        self.created = created
        self.image_file = image_file
        self.metadata = metadata
        self.score = score

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CollectionImage object from a json dictionary."""
        args = {}
        if 'image_id' in _dict:
            args['image_id'] = _dict['image_id']
        else:
            raise ValueError(
                'Required property \'image_id\' not present in CollectionImage JSON'
            )
        if 'created' in _dict:
            args['created'] = _dict['created']
        else:
            raise ValueError(
                'Required property \'created\' not present in CollectionImage JSON'
            )
        if 'image_file' in _dict:
            args['image_file'] = _dict['image_file']
        else:
            raise ValueError(
                'Required property \'image_file\' not present in CollectionImage JSON'
            )
        if 'metadata' in _dict:
            args['metadata'] = _dict['metadata']
        else:
            raise ValueError(
                'Required property \'metadata\' not present in CollectionImage JSON'
            )
        if 'score' in _dict:
            args['score'] = _dict['score']
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'image_id') and self.image_id is not None:
            _dict['image_id'] = self.image_id
        if hasattr(self, 'created') and self.created is not None:
            _dict['created'] = self.created
        if hasattr(self, 'image_file') and self.image_file is not None:
            _dict['image_file'] = self.image_file
        if hasattr(self, 'metadata') and self.metadata is not None:
            _dict['metadata'] = self.metadata
        if hasattr(self, 'score') and self.score is not None:
            _dict['score'] = self.score
        return _dict

    def __str__(self):
        """Return a `str` version of this CollectionImage object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class CollectionImages(object):
    """
    A collection of images.

    :attr list[CollectionImage] images:
    :attr int images_processed: (optional) The number of images processed in this call.
    """

    def __init__(self, images, images_processed=None):
        """
        Initialize a CollectionImages object.

        :param list[CollectionImage] images:
        :param int images_processed: (optional) The number of images processed in this call.
        """
        self.images = images
        self.images_processed = images_processed

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CollectionImages object from a json dictionary."""
        args = {}
        if 'images' in _dict:
            args['images'] = [
                CollectionImage._from_dict(x) for x in _dict['images']
            ]
        else:
            raise ValueError(
                'Required property \'images\' not present in CollectionImages JSON'
            )
        if 'images_processed' in _dict:
            args['images_processed'] = _dict['images_processed']
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'images') and self.images is not None:
            _dict['images'] = [x._to_dict() for x in self.images]
        if hasattr(self,
                   'images_processed') and self.images_processed is not None:
            _dict['images_processed'] = self.images_processed
        return _dict

    def __str__(self):
        """Return a `str` version of this CollectionImages object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class Collections(object):
    """
    success.

    :attr list[Collection] collections:
    """

    def __init__(self, collections):
        """
        Initialize a Collections object.

        :param list[Collection] collections:
        """
        self.collections = collections

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Collections object from a json dictionary."""
        args = {}
        if 'collections' in _dict:
            args['collections'] = [
                Collection._from_dict(x) for x in _dict['collections']
            ]
        else:
            raise ValueError(
                'Required property \'collections\' not present in Collections JSON'
            )
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'collections') and self.collections is not None:
            _dict['collections'] = [x._to_dict() for x in self.collections]
        return _dict

    def __str__(self):
        """Return a `str` version of this Collections object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class DetectedFaces(object):
    """
    DetectedFaces.

    :attr int images_processed: (optional) Number of images processed for the API call.
    :attr list[ImageWithFaces] images: The array of images.
    :attr list[WarningInfo] warnings: (optional) Information about what might cause less than optimal output. For example, a request sent with a corrupt .zip file and a list of image URLs will still complete, but does not return the expected output. Not returned when there is no warning.
    """

    def __init__(self, images, images_processed=None, warnings=None):
        """
        Initialize a DetectedFaces object.

        :param list[ImageWithFaces] images: The array of images.
        :param int images_processed: (optional) Number of images processed for the API call.
        :param list[WarningInfo] warnings: (optional) Information about what might cause less than optimal output. For example, a request sent with a corrupt .zip file and a list of image URLs will still complete, but does not return the expected output. Not returned when there is no warning.
        """
        self.images_processed = images_processed
        self.images = images
        self.warnings = warnings

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DetectedFaces object from a json dictionary."""
        args = {}
        if 'images_processed' in _dict:
            args['images_processed'] = _dict['images_processed']
        if 'images' in _dict:
            args['images'] = [
                ImageWithFaces._from_dict(x) for x in _dict['images']
            ]
        else:
            raise ValueError(
                'Required property \'images\' not present in DetectedFaces JSON'
            )
        if 'warnings' in _dict:
            args['warnings'] = [
                WarningInfo._from_dict(x) for x in _dict['warnings']
            ]
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self,
                   'images_processed') and self.images_processed is not None:
            _dict['images_processed'] = self.images_processed
        if hasattr(self, 'images') and self.images is not None:
            _dict['images'] = [x._to_dict() for x in self.images]
        if hasattr(self, 'warnings') and self.warnings is not None:
            _dict['warnings'] = [x._to_dict() for x in self.warnings]
        return _dict

    def __str__(self):
        """Return a `str` version of this DetectedFaces object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class ErrorInfo(object):
    """
    Information about what might have caused a failure, such as an image that is too
    large. Not returned when there is no error.

    :attr str error_id: Codified error string. For example, `limit_exceeded`.
    :attr str description: Human-readable error description. For example, `File size limit exceeded`.
    """

    def __init__(self, error_id, description):
        """
        Initialize a ErrorInfo object.

        :param str error_id: Codified error string. For example, `limit_exceeded`.
        :param str description: Human-readable error description. For example, `File size limit exceeded`.
        """
        self.error_id = error_id
        self.description = description

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ErrorInfo object from a json dictionary."""
        args = {}
        if 'error_id' in _dict:
            args['error_id'] = _dict['error_id']
        else:
            raise ValueError(
                'Required property \'error_id\' not present in ErrorInfo JSON')
        if 'description' in _dict:
            args['description'] = _dict['description']
        else:
            raise ValueError(
                'Required property \'description\' not present in ErrorInfo JSON'
            )
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'error_id') and self.error_id is not None:
            _dict['error_id'] = self.error_id
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        return _dict

    def __str__(self):
        """Return a `str` version of this ErrorInfo object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class Face(object):
    """
    Provides information about the face.

    :attr FaceAge age: (optional)
    :attr FaceGender gender: (optional)
    :attr FaceLocation face_location: (optional)
    :attr FaceIdentity identity: (optional)
    """

    def __init__(self, age=None, gender=None, face_location=None,
                 identity=None):
        """
        Initialize a Face object.

        :param FaceAge age: (optional)
        :param FaceGender gender: (optional)
        :param FaceLocation face_location: (optional)
        :param FaceIdentity identity: (optional)
        """
        self.age = age
        self.gender = gender
        self.face_location = face_location
        self.identity = identity

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Face object from a json dictionary."""
        args = {}
        if 'age' in _dict:
            args['age'] = FaceAge._from_dict(_dict['age'])
        if 'gender' in _dict:
            args['gender'] = FaceGender._from_dict(_dict['gender'])
        if 'face_location' in _dict:
            args['face_location'] = FaceLocation._from_dict(
                _dict['face_location'])
        if 'identity' in _dict:
            args['identity'] = FaceIdentity._from_dict(_dict['identity'])
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'age') and self.age is not None:
            _dict['age'] = self.age._to_dict()
        if hasattr(self, 'gender') and self.gender is not None:
            _dict['gender'] = self.gender._to_dict()
        if hasattr(self, 'face_location') and self.face_location is not None:
            _dict['face_location'] = self.face_location._to_dict()
        if hasattr(self, 'identity') and self.identity is not None:
            _dict['identity'] = self.identity._to_dict()
        return _dict

    def __str__(self):
        """Return a `str` version of this Face object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class FaceAge(object):
    """
    Provides age information about a face. If there are more than 10 faces in an image,
    the response might return the confidence score `0g.

    :attr int min: (optional) Estimated minimum age.
    :attr int max: (optional) Estimated maximum age.
    :attr float score: (optional) Confidence score for the property. Scores range from 0-1, with a higher score indicating greater correlation.
    """

    def __init__(self, min=None, max=None, score=None):
        """
        Initialize a FaceAge object.

        :param int min: (optional) Estimated minimum age.
        :param int max: (optional) Estimated maximum age.
        :param float score: (optional) Confidence score for the property. Scores range from 0-1, with a higher score indicating greater correlation.
        """
        self.min = min
        self.max = max
        self.score = score

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a FaceAge object from a json dictionary."""
        args = {}
        if 'min' in _dict:
            args['min'] = _dict['min']
        if 'max' in _dict:
            args['max'] = _dict['max']
        if 'score' in _dict:
            args['score'] = _dict['score']
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'min') and self.min is not None:
            _dict['min'] = self.min
        if hasattr(self, 'max') and self.max is not None:
            _dict['max'] = self.max
        if hasattr(self, 'score') and self.score is not None:
            _dict['score'] = self.score
        return _dict

    def __str__(self):
        """Return a `str` version of this FaceAge object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class FaceGender(object):
    """
    Provides information about the gender of the face. If there are more than 10 faces in
    an image, the response might return the confidence score 0.

    :attr str gender: Gender identified by the face. For example, `MALE` or `FEMALE`.
    :attr float score: (optional) Confidence score for the property. Scores range from 0-1, with a higher score indicating greater correlation.
    """

    def __init__(self, gender, score=None):
        """
        Initialize a FaceGender object.

        :param str gender: Gender identified by the face. For example, `MALE` or `FEMALE`.
        :param float score: (optional) Confidence score for the property. Scores range from 0-1, with a higher score indicating greater correlation.
        """
        self.gender = gender
        self.score = score

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a FaceGender object from a json dictionary."""
        args = {}
        if 'gender' in _dict:
            args['gender'] = _dict['gender']
        else:
            raise ValueError(
                'Required property \'gender\' not present in FaceGender JSON')
        if 'score' in _dict:
            args['score'] = _dict['score']
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'gender') and self.gender is not None:
            _dict['gender'] = self.gender
        if hasattr(self, 'score') and self.score is not None:
            _dict['score'] = self.score
        return _dict

    def __str__(self):
        """Return a `str` version of this FaceGender object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class FaceIdentity(object):
    """
    Provides information about a celebrity who is detected in the image. Not returned when
    a celebrity is not detected.

    :attr str name: Name of the person.
    :attr float score: (optional) Confidence score for the property. Scores range from 0-1, with a higher score indicating greater correlation.
    :attr str type_hierarchy: (optional) Knowledge graph of the property. For example, `People/Leaders/Presidents/USA/Barack Obama`. Included only if identified.
    """

    def __init__(self, name, score=None, type_hierarchy=None):
        """
        Initialize a FaceIdentity object.

        :param str name: Name of the person.
        :param float score: (optional) Confidence score for the property. Scores range from 0-1, with a higher score indicating greater correlation.
        :param str type_hierarchy: (optional) Knowledge graph of the property. For example, `People/Leaders/Presidents/USA/Barack Obama`. Included only if identified.
        """
        self.name = name
        self.score = score
        self.type_hierarchy = type_hierarchy

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a FaceIdentity object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict['name']
        else:
            raise ValueError(
                'Required property \'name\' not present in FaceIdentity JSON')
        if 'score' in _dict:
            args['score'] = _dict['score']
        if 'type_hierarchy' in _dict:
            args['type_hierarchy'] = _dict['type_hierarchy']
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'score') and self.score is not None:
            _dict['score'] = self.score
        if hasattr(self, 'type_hierarchy') and self.type_hierarchy is not None:
            _dict['type_hierarchy'] = self.type_hierarchy
        return _dict

    def __str__(self):
        """Return a `str` version of this FaceIdentity object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class FaceLocation(object):
    """
    Defines the location of the bounding box around the face.

    :attr float width: Width in pixels of face region.
    :attr float height: Height in pixels of face region.
    :attr float left: X-position of top-left pixel of face region.
    :attr float top: Y-position of top-left pixel of face region.
    """

    def __init__(self, width, height, left, top):
        """
        Initialize a FaceLocation object.

        :param float width: Width in pixels of face region.
        :param float height: Height in pixels of face region.
        :param float left: X-position of top-left pixel of face region.
        :param float top: Y-position of top-left pixel of face region.
        """
        self.width = width
        self.height = height
        self.left = left
        self.top = top

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a FaceLocation object from a json dictionary."""
        args = {}
        if 'width' in _dict:
            args['width'] = _dict['width']
        else:
            raise ValueError(
                'Required property \'width\' not present in FaceLocation JSON')
        if 'height' in _dict:
            args['height'] = _dict['height']
        else:
            raise ValueError(
                'Required property \'height\' not present in FaceLocation JSON')
        if 'left' in _dict:
            args['left'] = _dict['left']
        else:
            raise ValueError(
                'Required property \'left\' not present in FaceLocation JSON')
        if 'top' in _dict:
            args['top'] = _dict['top']
        else:
            raise ValueError(
                'Required property \'top\' not present in FaceLocation JSON')
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'width') and self.width is not None:
            _dict['width'] = self.width
        if hasattr(self, 'height') and self.height is not None:
            _dict['height'] = self.height
        if hasattr(self, 'left') and self.left is not None:
            _dict['left'] = self.left
        if hasattr(self, 'top') and self.top is not None:
            _dict['top'] = self.top
        return _dict

    def __str__(self):
        """Return a `str` version of this FaceLocation object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class ImageWithFaces(object):
    """
    ImageWithFaces.

    :attr list[Face] faces: An array of the faces detected in the images.
    :attr str image: (optional) Relative path of the image file if uploaded directly. Not returned when the image is passed by URL.
    :attr str source_url: (optional) Source of the image before any redirects. Not returned when the image is uploaded.
    :attr str resolved_url: (optional) Fully resolved URL of the image after redirects are followed. Not returned when the image is uploaded.
    :attr ErrorInfo error: (optional)
    """

    def __init__(self,
                 faces,
                 image=None,
                 source_url=None,
                 resolved_url=None,
                 error=None):
        """
        Initialize a ImageWithFaces object.

        :param list[Face] faces: An array of the faces detected in the images.
        :param str image: (optional) Relative path of the image file if uploaded directly. Not returned when the image is passed by URL.
        :param str source_url: (optional) Source of the image before any redirects. Not returned when the image is uploaded.
        :param str resolved_url: (optional) Fully resolved URL of the image after redirects are followed. Not returned when the image is uploaded.
        :param ErrorInfo error: (optional)
        """
        self.faces = faces
        self.image = image
        self.source_url = source_url
        self.resolved_url = resolved_url
        self.error = error

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ImageWithFaces object from a json dictionary."""
        args = {}
        if 'faces' in _dict:
            args['faces'] = [Face._from_dict(x) for x in _dict['faces']]
        else:
            raise ValueError(
                'Required property \'faces\' not present in ImageWithFaces JSON'
            )
        if 'image' in _dict:
            args['image'] = _dict['image']
        if 'source_url' in _dict:
            args['source_url'] = _dict['source_url']
        if 'resolved_url' in _dict:
            args['resolved_url'] = _dict['resolved_url']
        if 'error' in _dict:
            args['error'] = ErrorInfo._from_dict(_dict['error'])
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'faces') and self.faces is not None:
            _dict['faces'] = [x._to_dict() for x in self.faces]
        if hasattr(self, 'image') and self.image is not None:
            _dict['image'] = self.image
        if hasattr(self, 'source_url') and self.source_url is not None:
            _dict['source_url'] = self.source_url
        if hasattr(self, 'resolved_url') and self.resolved_url is not None:
            _dict['resolved_url'] = self.resolved_url
        if hasattr(self, 'error') and self.error is not None:
            _dict['error'] = self.error._to_dict()
        return _dict

    def __str__(self):
        """Return a `str` version of this ImageWithFaces object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class SimilarImages(object):
    """
    List of similar images. Maximum response size 200 kB.

    :attr list[CollectionImage] similar_images:
    :attr float images_processed: The number of images processed in this call.
    """

    def __init__(self, similar_images, images_processed):
        """
        Initialize a SimilarImages object.

        :param list[CollectionImage] similar_images:
        :param float images_processed: The number of images processed in this call.
        """
        self.similar_images = similar_images
        self.images_processed = images_processed

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SimilarImages object from a json dictionary."""
        args = {}
        if 'similar_images' in _dict:
            args['similar_images'] = [
                CollectionImage._from_dict(x) for x in _dict['similar_images']
            ]
        else:
            raise ValueError(
                'Required property \'similar_images\' not present in SimilarImages JSON'
            )
        if 'images_processed' in _dict:
            args['images_processed'] = _dict['images_processed']
        else:
            raise ValueError(
                'Required property \'images_processed\' not present in SimilarImages JSON'
            )
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'similar_images') and self.similar_images is not None:
            _dict['similar_images'] = [
                x._to_dict() for x in self.similar_images
            ]
        if hasattr(self,
                   'images_processed') and self.images_processed is not None:
            _dict['images_processed'] = self.images_processed
        return _dict

    def __str__(self):
        """Return a `str` version of this SimilarImages object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class WarningInfo(object):
    """
    Information about something that went wrong.

    :attr str warning_id: Codified warning string, such as `limit_reached`.
    :attr str description: Information about the error.
    """

    def __init__(self, warning_id, description):
        """
        Initialize a WarningInfo object.

        :param str warning_id: Codified warning string, such as `limit_reached`.
        :param str description: Information about the error.
        """
        self.warning_id = warning_id
        self.description = description

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a WarningInfo object from a json dictionary."""
        args = {}
        if 'warning_id' in _dict:
            args['warning_id'] = _dict['warning_id']
        else:
            raise ValueError(
                'Required property \'warning_id\' not present in WarningInfo JSON'
            )
        if 'description' in _dict:
            args['description'] = _dict['description']
        else:
            raise ValueError(
                'Required property \'description\' not present in WarningInfo JSON'
            )
        return cls(**args)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'warning_id') and self.warning_id is not None:
            _dict['warning_id'] = self.warning_id
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        return _dict

    def __str__(self):
        """Return a `str` version of this WarningInfo object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other):
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other
