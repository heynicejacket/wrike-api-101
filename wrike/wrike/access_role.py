from wrike.core.api import (
    wrike_get
)

from wrike.core.constants import (
    WRIKE_BASE_URL,
    WRIKE_ACCESS_ROLES_URL
)


def get_access_roles(return_all=False, verbose=False):
    """
    Retrieves a list of access roles from Wrike.

    Returns as follows:

        [
            {
                'id': 'IEAAB3DEND777777',
                'title': 'Full',
                'description': 'Can edit'
            },
            {
                'id': 'IEAAB3DEND777776',
                'title': 'Editor',
                'description': 'Most user rights available. Cannot share or delete items.'
            },
            ...
        ]

    :param return_all:          bool, optional          if True, return full response including metadata
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    dict                    API response in JSON format, access roles if successful
    """

    access_roles_url = WRIKE_BASE_URL + WRIKE_ACCESS_ROLES_URL
    print(access_roles_url) if verbose else None

    return wrike_get(url=access_roles_url, return_all=return_all, verbose=verbose)
