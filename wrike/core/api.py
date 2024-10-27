import json
import requests

from wrike.core.constants import (
    API_HEADER_WRIKE,
    API_HEADER_UPLOAD_WRIKE
)


def wrike_delete(url, return_all=False, verbose=False):
    """
    Helper function to execute DELETE request to the specified Wrike API endpoint.

    :param url:                 str, required           URL for DELETE request
    :param return_all:          bool, optional          if True, only return data dict; else, entire json dict
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format
    """

    try:
        response = requests.delete(url, headers=API_HEADER_WRIKE)
        response.raise_for_status()
        return response.json() if return_all else response.json().get('data')

    except requests.exceptions.HTTPError as err:
        print(f'HTTP Error: {err}') if verbose else None
        return None


def wrike_get(url, return_response=False, return_all=False, get_projects=None, params=None, verbose=False):
    """
    Helper function to send GET request to the specified Wrike API endpoint with the provided payload.

    By default, _wrike_get() returns all content as specified by its url. For all content other than Wrike projects and
    folders, get_projects should remain None. The Wrike API treats folders and projects as the same, with the latter
    having additional fields. Thus, to separate the two, we need to specify the difference in the API call.

    By default, 'get_projects' is set to None. However, if the GET request is for Wrike projects, 'get_projects' should
    be set to True. If for Wrike folders, 'get_projects' should be set to False. If wishing to return both folders and
    projects, set to None.

    By default, returns the entire JSON response. If return_all is True, only returns the subset of the JSON response
    associated with the 'data' key from the JSON response. If return_response is True, returns the entire response (this
    is necessary to

    :param url:                 str, required           Wrike API URL GET request
    :param return_response:     bool, optional          if True, only return full response
    :param return_all:          bool, optional          if True, only return data dict; else, entire json dict
    :param get_projects:        bool, optional          filter only projects (True), only folders (False), or both (None)
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format
    """

    url += f'?project={str(get_projects).lower()}' if get_projects is not None else ''

    try:
        response = requests.get(url, headers=API_HEADER_WRIKE, params=params)
        response.raise_for_status()
        if return_response:
            return response                                                             # return full response
        else:
            return response.json() if return_all else response.json().get('data')       # return json response

    except requests.exceptions.HTTPError as err:
        print(f'HTTP Error: {err}') if verbose else None
        return None


def wrike_post(url, payload, return_all=False, verbose=False):
    """
    Helper function to execute POST request to the specified Wrike API endpoint with the provided payload.

    By default, returns the entire JSON response; if return_all is True, only returns the subset of the JSON response
    associated with the 'data' key from the JSON response.

    :param url:                 str, required           Wrike API URL POST request
    :param payload:             dict, required          payload containing data to be sent in request
    :param return_all:          bool, optional          if True, only return data dict; else, entire json dict
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format
    """

    try:
        response = requests.post(url, headers=API_HEADER_WRIKE, data=json.dumps(payload))
        response.raise_for_status()
        return response.json() if return_all else response.json().get('data')

    except requests.exceptions.HTTPError as err:
        print(f'HTTP Error: {err}') if verbose else None
        return None


def wrike_post_upload(url, filepath, filename, verbose=False):
    """
    Uploads a file to a specified Wrike API endpoint using the POST method.

    This function reads content of a file from a given filepath and sends it to a provided Wrike API URL as a
    multipart/form-data request. Uploaded file is streamed to server and function returns JSON response from the API.

    :param url:                 str, required           task- or folder-specific Wrike API URL where file should be uploaded
    :param filepath:            str, required           local filepath of file to be uploaded (e.g. 'C:\...\file.xlsx')
    :param filename:            str, required           name of file to be uploaded
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format
    """

    try:
        with open(filepath, 'rb') as file:
            files = {'file': (filename, file, 'application/octet-stream')}
            response = requests.post(url=url, headers=API_HEADER_UPLOAD_WRIKE, files=files)
            response.raise_for_status()
            return response.json()

    except FileNotFoundError:
        raise FileNotFoundError(f'File not found: {filepath}')

    except requests.exceptions.RequestException as err:
        print(f'Error uploading {filename}: {err}') if verbose else None


def wrike_put(url, payload, return_all=False, verbose=False):
    """
    Helper function to execute PUT request to the specified Wrike API endpoint with the provided payload.

    By default, returns the entire JSON response; if return_all is True, only returns the subset of the JSON response
    associated with the 'data' key from the JSON response.

    :param url:                 str, required           Wrike API URL PUT request
    :param payload:             dict, required          payload containing data to be sent in request
    :param return_all:          bool, optional          if True, only return data dict; else, entire json dict
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format
    """

    try:
        response = requests.put(url, headers=API_HEADER_WRIKE, data=json.dumps(payload))
        response.raise_for_status()
        return response.json() if return_all else response.json().get('data')

    except requests.exceptions.HTTPError as err:
        print(f'HTTP Error: {err}') if verbose else None
        return None


def wrike_put_upload(url, filepath, filename, verbose=False):
    """
    Updates a file to a specified Wrike API endpoint using the POST method.

    This function reads content of a file from a given filepath and sends it to a provided Wrike API URL as a
    multipart/form-data request. Uploaded file is streamed to server and function returns JSON response from the API.

    :param url:                 str, required           task- or folder-specific Wrike API URL where file should be updated
    :param filepath:            str, required           local filepath of file to be updated (e.g. 'C:\...\file.xlsx')
    :param filename:            str, required           name of file to be updated
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format
    """

    try:
        with open(filepath, 'rb') as file:
            files = {'file': (filename, file, 'application/octet-stream')}
            response = requests.put(url=url, headers=API_HEADER_UPLOAD_WRIKE, files=files)
            response.raise_for_status()
            return response.json()

    except FileNotFoundError:
        raise FileNotFoundError(f'File not found: {filepath}')

    except requests.exceptions.RequestException as err:
        print(f'Error uploading {filename}: {err}') if verbose else None
