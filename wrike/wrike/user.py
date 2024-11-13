import json

from wrike.core.api import (
    wrike_get,
    wrike_put
)

from wrike.core.constants import (
    WRIKE_BASE_URL,
    WRIKE_CONTACTS_URL,
    WRIKE_USER_URL,
    WRIKE_USER_TYPES_URL
)


def get_user(user_id='', return_all=False, verbose=False):
    """
    Given a user_id, returns metadata for a specific user in Wrike.

    :param user_id:             str, required           ID of user to fetch metadata
    :param return_all:          bool, optional          if True, return full response including metadata
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format, user details if successful
    """

    user_url = WRIKE_BASE_URL + WRIKE_USER_URL + f'{user_id}'
    print(user_url) if verbose else None

    return wrike_get(url=user_url, return_all=return_all, verbose=verbose)


def get_user_types(return_all=False, verbose=False):
    """
    Retrieves a list of available user types from Wrike.

    Exampled returned JSON is as follows:

        [
            {
                'id': 'IEAAB3DENH777777',
                'title': 'Owner',
                'description': 'Owner'
            },
            {
                'id': 'IEAAB3DENH777776',
                'title': 'Admin',
                'description': 'Admin'
            },
            {
                'id': 'IEAAB3DENH777775',
                'title': 'Regular User',
                'description': 'Regular User'
            },
            {
                'id': 'IEAAB3DENH777774',
                'title': 'External User',
                'description': 'External User'
            },
            {
                'id': 'IEAAB3DENH777773',
                'title': 'Collaborator',
                'description': 'Collaborator'
            }
        ]

    :param return_all:          bool, optional          if True, return full response including metadata
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format, user types if successful
    """

    user_types_url = WRIKE_BASE_URL + WRIKE_USER_TYPES_URL
    print(user_types_url) if verbose else None

    return wrike_get(url=user_types_url, return_all=return_all, verbose=verbose)


def get_users_all(metadata=None, deleted=None, custom_fields=None, return_all=False, verbose=False):
    """
    Retrieves all contacts (users and user groups) in the current Wrike account.

    This function constructs a GET request to the '/contacts' endpoint in the Wrike API. It can optionally filter
    contacts by metadata, deleted status, and custom fields.

    Returns JSON of all users as follows:

        todo: add example

    :param metadata:            dict, optional          metadata filter as key-value pair to match contacts
    :param deleted:             bool, optional          if True, include deleted users in results
    :param custom_fields:       list, optional          filter by custom fields
    :param return_all:          bool, optional          if True, return full response including metadata
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format, all contacts if successful
    """

    contacts_url = WRIKE_BASE_URL + WRIKE_CONTACTS_URL
    print(contacts_url) if verbose else None

    params = {}

    if metadata:
        params['metadata'] = json.dumps(metadata)
    if deleted is not None:
        params['deleted'] = str(deleted).lower()                        # convert bool to 'true' or 'false'
    if custom_fields:
        params['customFields'] = json.dumps(custom_fields)
    if verbose:
        print(f'Requesting Wrike Contacts with URL: {contacts_url} and parameters: {params}')

    return wrike_get(url=contacts_url, params=params, return_all=return_all, verbose=verbose)


def update_user(user_id, account_id, role, external=None, verbose=False):
    """
    Updates a user's profile in Wrike. The user_id, account_id, and role are required parameters. Other parameters
    are optional.

    Returns JSON of updated user data, as follows:

        [
            {
                'id': 'KUALDPDC',
                'firstName': 'Matthew',
                'lastName': 'Runde',
                'type': 'Person',
                'profiles': [
                    {
                        'accountId': 'IEAAB3DE',
                        'email': 'matthew@nicejacket.cc',
                        'role': 'User',
                        'external': False,
                        'admin': True,
                        'owner': False
                    }
                ],
                'avatarUrl': 'https://www.wrike.com/avatars//36/26/Box_ff43a047_77-82_v1.png',
                'timezone': 'America/Los_Angeles',
                'locale': 'en',
                'deleted': False,
                'me': True,
                'title': 'Director',
                'primaryEmail':
                'mrunde@splicepm.com'
            }
        ]

    :param user_id:             str, required           ID of user to be updated
    :param account_id:          str, required           account ID associated with user
    :param role:                str, required           new role for user (e.g., 'Collaborator', 'User', 'Admin')
    :param external:            bool, optional          flag to mark user as external
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format
    """

    update_user_url = WRIKE_BASE_URL + WRIKE_USER_URL + f'{user_id}'
    print(update_user_url) if verbose else None

    payload = {
        'profile': {
            'accountId': account_id,
            'role': role
        }
    }

    if external is not None:
        payload['profile']['external'] = external

    return wrike_put(url=update_user_url, payload=payload, verbose=verbose)
