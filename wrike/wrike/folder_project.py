from wrike.core.api import (
    wrike_delete,
    wrike_get,
    wrike_post,
    wrike_put
)

from wrike.core.constants import (
    WRIKE_BASE_URL,
    WRIKE_SPACE_URL,
    WRIKE_FOLDER_URL,
    WRIKE_CREATE_FOLDER_URL,
    WRIKE_UPDATE_OR_DELETE_FOLDER_URL
)


def add_child_kv(folder_data):
    """
    Given a Wrike folder dict, adds a 'child' key-value pair to each folder in folder_data, where the key is
    child folder's 'id' and the value is child folder's 'title', creating a parent-child relationship for all folders,
    based on the provided child-parent hierarchy in 'childIds', as follows:

        'childIds': ['IEAAB3DEI5M5NACG', ...]

    Each folder will receive a 'child' key, which contains a dictionary mapping the child folder's ID to its
    title. If a folder has no children, the 'child' key will be an empty dictionary. Dictionary is as follows:

        'childF':  {'IEAAB3DEI5M5NACG': 'folder_1a', ...}

    Returns folder_data with 'child' key-value pair added.

    :param folder_data:         list, required          list of folder data dicts
    :return:                    dict                    folder dict with 'child' key-value pair added
    """

    id_to_title = {item['id']: item['title'] for item in folder_data}

    # add 'child' and drop 'childIds' in a single loop
    for item in folder_data:
        item['child'] = {child_id: id_to_title.get(child_id, '') for child_id in item.get('childIds', [])}
        item.pop('childIds', None)

    return folder_data


def add_level(folder_data):
    """
    Adds a 'level' key to each folder in the folder data, indicating its level in the hierarchy, starting from 0.

    folder_data should at a minimum be structured as follows:

        todo: real example

    Returns folder_data with folder levels added as follows:

        todo: real example

    :param folder_data:         list, required          list of folder data dictionaries
    :return:                    list                    folder data with folder levels added
    """

    id_to_folder = {folder['id']: folder for folder in folder_data}

    # identify root-level folders (folders with no parent) and assign level 0
    for folder in folder_data:
        if not folder.get('parent'):                                                # root folder has no parent
            assign_level(folder_dict=folder, level=0, id_to_folder=id_to_folder)    # pass id_to_folder explicitly

    return folder_data


def add_parent_kv(folder_data):
    """
    Given a Wrike folder or project dict, adds a 'parent' key-value pair to each folder or folder in folder_data, where
    the key is parent's 'id' and the value is parent's 'title', creating a parent-child relationship for all folders or
    projects, based on the provided child-parent hierarchy in 'childIds', as follows:

        'childIds': ['IEAAB3DEI5M5NACG', ...]

    Each folder or project will receive a 'parent' key, which contains a dictionary mapping the parent's ID to its
    title. If a folder or project has no parent, the 'parent' key will be an empty dictionary. Dictionary is as follows:

        'parent': {'IEAAB3DEI5M5NACG': 'folder_a'}

    Returns folder_data with 'parent' key-value pair added.

    :param folder_data:         list, required          list of folder data dicts
    :return:                    dict                    folder dict with 'parent' key-value pair added
    """

    id_to_title = {item['id']: item['title'] for item in folder_data}

    # define function that assigns 'parent' to each item based on its children
    def process_item(item, parent_id=None):
        item['parent'] = {parent_id: id_to_title.get(parent_id, '')} if parent_id else {}
        return item

    # process all items and assign parentFolder, recursively add parent-child relationships
    for item in folder_data:
        if 'childIds' in item and item['childIds']:
            for child_id in item['childIds']:
                child_item = next((child for child in folder_data if child['id'] == child_id), None)
                if child_item:
                    process_item(child_item, item['id'])

    return folder_data


def assign_level(folder_dict, level, id_to_folder):
    """
    Helper function to recursively assign levels to Wrike API JSON folder hierarchy, starting from the root folder.

    The variable folder_dict contains the dict of each folder, in turn, and appears as follows:

    {
        'id': 'IEAAB3IPI5MDEM3K',
        'title': 'Folder Title',
        'scope': 'WsFolder',
        'child': {
            'IEAAB3DEIKC5M4ND': 'folder_d',
            ...
        }
    }

    id_to_folder provides a lookup table to prevent having to loop through entire folder list to find a folder by its
    id; lookup table is created outside this function to save time during recursion.

    Returns nothing directly, modifying in place the JSON dict with the folder level added.

    :param folder_dict:         dict, required          folder dict to which the current level is to be assigned
    :param level:               int, required           current level of the folder
    :param id_to_folder:        dict, required          lookup dict of folder IDs to folder data
    :return:                    dict                    modified in place Wrike folder dict with folder level added
    """

    folder_dict['level'] = level
    for child_id in folder_dict.get('child', {}).keys():
        if child_id in id_to_folder:
            assign_level(folder_dict=id_to_folder[child_id], level=level+1, id_to_folder=id_to_folder)


def create_folder(space_or_folder_id, title, description=None, shareds=None, metadata=None, custom_fields=None,
                        project=None, user_access_roles=None, with_invitations=None, verbose=False):
    """
    Creates new folder within a specified parent folder in Wrike. If new folder is to be created at Space level (0th
    level) space_id is to be used in place of (parent) folder_id. Title parameter is required; the following parameters
    are optional:

        description, shared users, metadata, custom fields, project details, user access roles

    Constructs a POST request to the 'folders/{folder_id}/folders/' endpoint, where folder_id is the parent folder in
    which the new folder will be created.

    Returns API response in JSON format.

    URL to pass to requests.post() as follows:

        https://www.wrike.com/api/v4/folders/IEAVJOU5I7777777/folders

    Parameters to pass into this function as follows:

        space_or_folder_id = 'IEAVJOU5I7777777'
        title = 'Test Folder'
        description = 'Description of test folder'
        shareds = ['KUAAAABF']
        metadata = [{'key': 'testMetaKey', 'value': 'testMetaValue'}]
        custom_fields = [{'id': 'IEAVJOU5JUAAAACG', 'value': 'testValue'}]
        project = {
            'ownerIds': ['KUAAAABF'],
            'startDate': '2024-09-17',
            'endDate': '2024-09-24',
            'contractType': 'Billable',
            'budget': 100
        }
        user_access_roles = {'KUAAAABF': 'IEAVJOU5ND777777'}
        with_invitations = True

    Returned API response as follows:

        {
            'kind': 'folders',
            'data': [
                {
                    'id': 'IEAVJOU5I4AB5BKD',
                    'accountId': 'IEAVJOU5',
                    'title': 'Test Folder',
                    'createdDate': '2024-09-17T07:51:23Z',
                    'updatedDate': '2024-09-17T07:51:23Z',
                    'description': 'Description of test folder',
                    'sharedIds': [
                        'KUAAAABF'
                    ],
                    'parentIds': [
                        'IEAVJOU5I4AB5BKC'
                    ],
                    'childIds': [],
                    'scope': 'WsFolder',
                    'hasAttachments': false,
                    'permalink': 'https://www.wrike.com/open.htm?id=2000195',
                    'workflowId': 'IEAVJOU5K77KWRLD',
                    'metadata': [
                        {
                            'key': 'testMetaKey',
                            'value': 'testMetaValue'
                        }
                    ],
                    'customFields': [
                        {
                            'id': 'IEAVJOU5JUAAAACG',
                            'value': 'testValue'
                        }
                    ],
                    'project': {
                        'authorId': 'KUAAAABF',
                        'ownerIds': [
                            'KUAAAABF'
                        ],
                        'startDate': '2024-09-17',
                        'endDate': '2024-09-24'
                    }
                }
            ]
        }

    :param space_or_folder_id:  str, required           parent folder or space ID where new folder will be created
    :param title:               str, required           title of folder to be created
    :param description:         str, optional           description of folder to be created
    :param shareds:             list, optional          user IDs with whom to share folder (creator always shared)
    :param metadata:            list, optional          metadata entries (key-value pairs) to add to new folder
    :param custom_fields:       list, optional          custom field dict entries to add to new folder
    :param project:             dict, optional          project details to set if creating a project folder
    :param user_access_roles:   dict, optional          user IDs and corresponding access roles
    :param with_invitations:    bool, optional          if True, include invitations in ownerIds and sharedIds list
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    dict                    API response, with details of the created folder
    """

    create_folder_url = WRIKE_BASE_URL + WRIKE_CREATE_FOLDER_URL.format(space_or_folder_id)
    print(create_folder_url) if verbose else None

    payload = {'title': title, }                                            # construct required payload

    if description:                                                         # add optional fields if provided
        payload['description'] = description
    if shareds:
        payload['shareds'] = shareds
    if metadata:
        payload['metadata'] = metadata
    if custom_fields:
        payload['customFields'] = custom_fields
    if project:
        payload['project'] = project
    if user_access_roles:
        payload['userAccessRoles'] = user_access_roles
    if with_invitations is not None:
        payload['withInvitations'] = with_invitations

    return wrike_post(url=create_folder_url, payload=payload, verbose=verbose)


def create_project(space_or_folder_id, title, description=None, shareds=None, metadata=None, custom_fields=None,
                   owner_ids=None, custom_status_id=None, start_date=None, end_date=None, contract_type=None,
                   budget=None, user_access_roles=None, with_invitations=None, verbose=False):
    """
    Creates new project within specified parent folder in Wrike. If project is to be created at Space level (0th
    level), space_id is to be used in place of (parent) folder_id. Title parameter is required; the following parameters
    are optional:

        description, shared users, metadata, custom_fields, owner_ids, custom_status_id, start_date, end_date,
        contract_type, budget, user_access_roles, with_invitations

    Constructs POST request to the 'folders/{folder_id}/folders/' endpoint, where folder_id is the parent folder in
    which new project will be created.

    Returns API response in JSON format.

    URL to pass to requests.post() as follows:

        https://www.wrike.com/api/v4/folders/IEAVJOU5I7777777/folders

    Parameters to pass into this function as follows:

        space_or_folder_id = 'IEAVJOU5I7777777'
        title = 'Test Project'
        description = 'Description of test project'
        shareds = ['KUAAAABF']
        metadata = [{'key': 'testMetaKey', 'value': 'testMetaValue'}]
        custom_fields = [{'id': 'IEAVJOU5JUAAAACG', 'value': 'testValue'}]
        owner_ids = ['KUAAAABF']
        custom_status_id = 'IEAVJOU5JMAAAAAA'
        start_date = '2024-09-17'
        end_date = '2024-09-24'
        contract_type = 'Billable'
        budget = 100
        user_access_roles = {'KUAAAABF': 'IEAVJOU5ND777777'}
        with_invitations = True

    Returned API response as follows:

        {
            'id': 'IEAAB3DEI5M5NKRM',
            'accountId': 'IEAAB3DE',
            'title': 'Test Project',
            'createdDate': '2024-10-06T22:32:37Z',
            'updatedDate': '2024-10-06T22:44:46Z',
            'description': 'Test project description',
            'sharedIds': ['KUAFMCAH', 'KUALDPDC'],
            'parentIds': ['IEAAB3DEI5M4KMIP'],
            'childIds': [],
            'superParentIds': [],
            'scope': 'WsFolder',
            'hasAttachments': False,
            'permalink': 'https://www.wrike.com/open.htm?id=1507240492',
            'workflowId': 'IEAAB3DEK7776E44',
            'metadata': [{'key': 'testMetaKey', 'value': 'testMetaValue'}],
            'customFields': [{'id': 'IEAVJOU5JUAAAACG', 'value': 'testValue'}],
            'project': {
                'authorId': 'KUAAAABF',
                'ownerIds': ['KUAAAABF'],
                'customStatusId': 'IEAVJOU5JMAAAAAA',
                'startDate': '2024-09-17',
                'endDate': '2024-09-24',
                'contractType': 'Billable',
                'budget': 100
            }
        }

    :param space_or_folder_id:  str, required           parent folder or space ID where project will be created
    :param title:               str, required           title of project to be created
    :param description:         str, optional           description of project to be created
    :param shareds:             list, optional          user IDs with whom to share project (creator always shared)
    :param metadata:            list, optional          metadata entries (key-value pairs) to add to project
    :param custom_fields:       list, optional          custom field dict entries to add to project
    :param owner_ids:           list, optional          project owner IDs
    :param custom_status_id:    str, optional           custom status ID for project
    :param start_date:          str, optional           start date of project (format: yyyy-MM-dd)
    :param end_date:            str, optional           end date of project (format: yyyy-MM-dd)
    :param contract_type:       str, optional           contract type for project (e.g., 'Billable')
    :param budget:              float, optional         budget for project
    :param user_access_roles:   dict, optional          user IDs and corresponding access roles
    :param with_invitations:    bool, optional          if True, include invitations in ownerIds and sharedIds list
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    dict                    API response, with details of created project
    """

    create_project_url = WRIKE_BASE_URL + WRIKE_CREATE_FOLDER_URL.format(space_or_folder_id)
    print(create_project_url) if verbose else None

    payload = {'title': title, 'project': {}, }                             # construct required payload

    if description:                                                         # add optional fields if provided
        payload['description'] = description
    if shareds:
        payload['shareds'] = shareds
    if metadata:
        payload['metadata'] = metadata
    if custom_fields:
        payload['customFields'] = custom_fields
    if owner_ids:
        payload['project']['ownerIds'] = owner_ids
    if custom_status_id:
        payload['project']['customStatusId'] = custom_status_id
    if start_date:
        payload['project']['startDate'] = start_date
    if end_date:
        payload['project']['endDate'] = end_date
    if contract_type:
        payload['project']['contractType'] = contract_type
    if budget:
        payload['project']['budget'] = budget
    if user_access_roles:
        payload['userAccessRoles'] = user_access_roles
    if with_invitations is not None:
        payload['withInvitations'] = with_invitations

    return wrike_post(url=create_project_url, payload=payload, verbose=verbose)


def delete_folder_or_project(folder_or_project_id, verbose=False):
    """
    Deletes an existing folder or project in Wrike by moving it to the Recycle Bin, including all descendant folders
    and tasks unless they have parents outside the deletion scope.

    Constructs a DELETE request to the 'folders/{folder_or_project_id}' endpoint, where folder_or_project_id is the ID
    of the folder or project to be deleted.

    URL to pass to requests.delete(), as follows:

        https://www.wrike.com/api/v4/folders/IEAVJOU5I4AB5BKC

    Parameters to pass into this function, as follows:

        folder_or_project_id = 'IEAVJOU5I4AB5BKC'   # can be folder or project ID

    Returned API response in JSON, as follows:

        {
            'id': 'IEAVJOU5I4AB5BKC',
            'accountId': 'IEAVJOU5',
            'title': 'Deleted Folder or Project Title',
            'createdDate': '2024-09-17T07:51:23Z',
            'updatedDate': '2024-09-17T07:51:52Z',
            'description': 'Description before deletion',
            'sharedIds': ['KUAAAABF', 'KUAAAABG'],
            'parentIds': ['IEAVJOU5I7777776'],
            'childIds': ['IEAVJOU5I4AB5BKD', 'IEAVJOU5I4AB5BKE'],
            'scope': 'RbFolder' or 'RbProject',  # Recycle bin scope
            'hasAttachments': False,
            'permalink': 'https://www.wrike.com/open.htm?id=2000194',
            'workflowId': 'IEAVJOU5K77KWRLD',
            'metadata': [{'key': 'testMetaKey', 'value': 'testMetaValue'}],
            'customFields': [{'id': 'IEAVJOU5JUAAAACG', 'value': 'testValue'}]
        }

    :param folder_or_project_id:    str, required       ID of folder or project to be deleted
    :param verbose:                 bool, optional      if True, print status to terminal
    :return:                        dict                API response with details of deleted folder or project
    """

    delete_url = WRIKE_BASE_URL + WRIKE_UPDATE_OR_DELETE_FOLDER_URL + f'{folder_or_project_id}'
    print(delete_url) if verbose else None

    return wrike_delete(url=delete_url, verbose=verbose)


def extract_folder_or_project_hierarchy(data, base_keys=None, additional_keys=None, verbose=False):
    """
    Extracts 'id', 'title', and 'level' key-value pairs from each dict in the list.

    Optionally, a list of additional keys can be given to preserve additional key-value pairs from list of dicts
    provided. Additional keys can be passed as follows:

        additional_keys = ['foo', 'bar']

    Given a dict as follows:

        [
            {'id': 'IEAAB3DEI5M4RE5R', 'accountId': 'IEAAB3DE', 'title': 'folder_a', ..., 'level': 0},
            {'id': 'IEAAB3DEI5M4RE6S', 'accountId': 'IEAAB3DE', 'title': 'folder_b', ..., 'level': 0},
            ...
        ]

    Returns as follows:

        [
            {'id': 'IEAAB3DEI5M4RE5R', 'title': 'folder_a', 'level': 0},
            {'id': 'IEAAB3DEI5M4RE6S', 'title': 'folder_b', 'level': 0},
            ...
        ]

    :param data:                list, required          list of dicts containing 'id', 'title', 'level'
    :param base_keys:           list, optional          if not None, uses default list of keys
    :param additional_keys:     list, optional          list of additional keys for retaining key-value pairs
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    list                    list of dicts of only 'id', 'title', 'level' key-value pairs
    """

    if base_keys is None:
        base_keys = ['id', 'title', 'level']

    keys_to_extract = base_keys + (additional_keys if additional_keys else [])

    extracted_data = []
    for item in data:
        extracted_item = {key: item[key] for key in keys_to_extract if key in item}
        extracted_data.append(extracted_item)

    print(extracted_data) if verbose else None

    return extracted_data


def folder_level_map(folder_metadata, verbose=False):
    """
    Provided folder metadata from get_wrike_folder_or_project_metadata(), returns a dict of folder IDs and levels,
    as follows:

        {
            'IEAAB3DEI5M4RE5R': 0,
            'IEAAB3DEI5M4RE6S': 0,
            'IEAAB3DEI5M4RFCH': 1,
            'IEAAB3DEI5M4RFHK': 0,
            'IEAAB3DEI5M4RFH5': 1,
            'IEAAB3DEI5M4RFNS': 2
        }

    :param folder_metadata:     list, required          folder metadata list of dicts
    :param verbose:             bool, optional          if True, print status to terminal
    :return:
    """

    folder_level_map = {folder['id']: folder['level'] for folder in folder_metadata}
    print(folder_level_map) if verbose else None

    return folder_level_map


def get_folder_or_project_dict(space_id, additional_keys=None, verbose=False):
    """
    Given a space ID, returns a dict containing folder or project ID, and type (e.g. 'folder' or 'project').

    Returns a list of dicts as follows:

        [
            {'id': 'IEAAB3DEI5M4KMIP', 'type': 'folder'},
            {'id': 'IEAAB3DEI5M4RFOO', 'type': 'folder'},
            {'id': 'IEAAB3DEI5NBKLPZ', 'type': 'project'},
            ...
        ]

    :param space_id:
    :param additional_keys:
    :param verbose:             bool, optional          if True, print status to terminal
    :return:
    """

    space_metadata = get_folder_or_project_metadata(space_id=space_id, get_projects=None, verbose=verbose)

    folder_or_project_type_dict = []
    for item in space_metadata:
        simplified_item = {
            'id': item['id'],
            'type': 'project' if 'project' in item else 'folder'
        }

        # preserve additional keys if they exist
        for key in additional_keys:
            if key in item:
                simplified_item[key] = item[key]

        folder_or_project_type_dict.append(simplified_item)

    print(folder_or_project_type_dict) if verbose else None

    return folder_or_project_type_dict


def get_folder_or_project_id(space_id, folder_title=None, project_title=None, verbose=False):
    """
    Given a Wrike space ID and folder or project title, return the ID of the Wrike folder or project.

    :param space_id:            str, required           Wrike space ID from which to retrieve metadata
    :param folder_title:        str, required           Wrike folder name from which to retrieve ID
    :param project_title:       str, required           Wrike project name from which to retrieve ID
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    str                     Wrike folder ID
    """

    if folder_title is None and project_title is None:
        raise ValueError('Either \'folder_id\' or \'project_id\' must be provided.')

    get_projects = None
    if folder_title is not None:
        get_projects = False
        title = folder_title
    elif project_title is not None:
        get_projects = True
        title = project_title

    folder_or_project_dict = get_folder_or_project_metadata(
        space_id=space_id,
        get_projects=get_projects,
        verbose=verbose
    )

    folder_or_project_id = next((item['id'] for item in folder_or_project_dict if item['title'] == title), None)
    print(folder_or_project_id) if verbose else None

    return folder_or_project_id


def get_folder_or_project_metadata(space_id, get_projects=None, verbose=False):
    """
    Given a Wrike space ID, retrieves dict of Wrike folders or projects, based on the parameter folder_or_project.

    By default, 'get_projects' is set to None, which returns both folders and project. To return only Wrike projects,
    set 'get_projects' to True. To return only Wrike folders, set 'get_projects' to False.

    Folder metadata structure is as follows:

        todo: real example

    Project metadata structure is as follows:

        [
            {
                'id': 'IEAAB3DEI5NBKJQW',
                'accountId': 'IEAAB3DE',
                'title': 'Test Project',
                'createdDate': '2024-10-13T15:36:28Z',
                'updatedDate': '2024-10-13T15:37:08Z',
                'description': '',
                'sharedIds': ['KUAFMCAH', 'KUALDPDC', 'KUAP3YOD'],
                'parentIds': ['IEAAB3DEI5M4RE5R'],
                'childIds': [],
                'scope': 'WsFolder',
                'permalink': 'https://www.wrike.com/open.htm?id=1511335446',
                'workflowId': 'IEAAB3DEK7776E44',
                'project': {
                    'authorId': 'KUALDPDC',
                    'ownerIds': [],
                    'status': 'Custom',
                    'customStatusId': 'IEAAB3DEJMAAAAAA',
                    'createdDate': '2024-10-13T15:36:28Z'
                }
            },
            ...
        ]

    Using these dict and childIds, e.g.:

        'childIds': ['IEAAB3DEI5M5NACG', ...]

    create within each folder or project dict child and parent key-value pairs, as follows:

        'child':  {'IEAAB3DEI5M5NACG': 'folder_1a', ...}
        'parent': {'IEAAB3DEI5M5NACG': 'folder_a'}

    Using these, within each folder dict, add a folderLevel key-value for its position in folder hierarchy, as follows:

        'level': 0

    Returns the Wrike folder dict with these added values.

    :param space_id:            str, required           Wrike space ID from which to retrieve metadata
    :param get_projects:        bool, required
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    dict                    processed Wrike folder dict
    """

    folder_url = WRIKE_BASE_URL + WRIKE_SPACE_URL + f'{space_id}/' + WRIKE_FOLDER_URL

    f_meta = wrike_get(url=folder_url, get_projects=get_projects, verbose=verbose)      # get base folder metadata
    f_meta_parent_data_added = add_parent_kv(f_meta)                                    # create parentFolder dict
    f_meta_child_data_added = add_child_kv(f_meta_parent_data_added)                    # create childFolder dict
    f_meta_level_data_added = add_level(f_meta_child_data_added)                        # add 'level': n

    return f_meta_level_data_added


def get_folder_or_project_name(space_id, folder_id=None, project_id=None, verbose=False):
    """
    Given a Wrike space ID and folder ID or project ID, return the title of the Wrike folder or project.

    :param space_id:            str, required           Wrike space ID from which to retrieve metadata
    :param folder_id:           str, optional           Wrike folder ID from which to retrieve folder name
    :param project_id:          str optional            Wrike project ID from which to retrieve project name
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    str                     Wrike folder name
    """

    if folder_id is None and project_id is None:
        raise ValueError('Either \'folder_id\' or \'project_id\' must be provided.')

    if folder_id is not None:
        folder_or_project_dict = get_folder_or_project_metadata(space_id=space_id, get_projects=False)
        folder_or_project_id = folder_id
    elif project_id is not None:
        folder_or_project_dict = get_folder_or_project_metadata(space_id=space_id, get_projects=True)
        folder_or_project_id = project_id

    folder_or_project_name = next(
        (item['title'] for item in folder_or_project_dict if item['id'] == folder_or_project_id), None
    )
    print(folder_or_project_name) if verbose else None

    return folder_or_project_name


def update_folder(folder_id, title=None, description=None, add_parents=None, remove_parents=None,
                        add_shareds=None, remove_shareds=None, metadata=None, custom_fields=None, project=None,
                        user_access_roles=None, with_invitations=None, verbose=False):
    """
    Updates existing folder in Wrike. The following parameters are optional:

        title, description, add_parents, remove_parents, add_shareds, remove_shareds,
        metadata, custom_fields, project, user_acces_roles, with_invitations

    Constructs a PUT request to the 'folders/{folder_id}' endpoint, where folder_id is ID of folder to be updated.

    URL to pass to requests.post(), as follows:

        https://www.wrike.com/api/v4/folders/IEAVJOU5I4AB5BKC

    Parameters to pass into this function, as follows:

        folder_id = 'IEAVJOU5I4AB5BKC'
        title = 'Updated Folder Title'
        description = 'Updated folder description'
        add_parents = ['IEAVJOU5I7777777']
        remove_parents = ['IEAVJOU5I4AB5BKA']
        add_shareds = ['KUAAAABF']
        remove_shareds = ['KUAAAABG']
        metadata = [{'key': 'updatedMetaKey', 'value': 'updatedMetaValue'}]
        custom_fields = [{'id': 'IEAVJOU5JUAAAACG', 'value': 'updatedValue'}]
        project = {
            'ownersAdd': ['KUAAAABF'],
            'ownersRemove': ['KUAAAABG'],
            'startDate': '2024-09-17',
            'endDate': '2024-09-24'
        }
        user_access_roles = {'KUAAAABF': 'IEAVJOU5ND777777'}
        with_invitations = True

    Returned API response IN JSON format, as follows:

        {
            'id': 'IEAAB3DEI5M5NKRM',
            'accountId': 'IEAAB3DE',
            'title': 'Updated Folder Title',
            'createdDate': '2024-10-06T22:32:37Z',
            'updatedDate': '2024-10-06T22:44:46Z',
            'description': 'Updated folder description',
            'sharedIds': ['KUAFMCAH', 'KUALDPDC', 'KUAP3YOD'],
            'parentIds': ['IEAAB3DEI5M4KMIP'],
            'childIds': [],
            'superParentIds': [],
            'scope': 'WsFolder',
            'hasAttachments': False,
            'permalink': 'https://www.wrike.com/open.htm?id=1507240492',
            'workflowId': 'IEAAB3DEK7776E44',
            'metadata': [{'key': 'updatedMetaKey', 'value': 'updatedMetaValue'}],
            'customFields': [{'id': 'IEAVJOU5JUAAAACG', 'value': 'updatedValue'}]
        }

    :param folder_id:           str, required           ID of folder to be updated
    :param title:               str, optional           new title for folder
    :param description:         str, optional           updated description of folder
    :param add_parents:         list, optional          parent folder IDs to add
    :param remove_parents:      list, optional          parent folder IDs to remove
    :param add_shareds:         list, optional          user IDs to add to shared users
    :param remove_shareds:      list, optional          user IDs to remove from shared users
    :param metadata:            list, optional          metadata entries (key-value pairs) to update
    :param custom_fields:       list, optional          custom field dict entries to update
    :param project:             dict, optional          project details for updating project settings
    :param user_access_roles:   dict, optional          user IDs and corresponding access roles
    :param with_invitations:    bool, optional          if True, include invitations in ownerIds and sharedIds list
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    dict                    API response, with details of updated folder
    """

    update_folder_url = WRIKE_BASE_URL + WRIKE_UPDATE_OR_DELETE_FOLDER_URL.format(folder_id)
    print(update_folder_url) if verbose else None

    payload = {}                                                            # construct required payload

    if title:                                                               # add optional fields if provided
        payload['title'] = title
    if description:
        payload['description'] = description
    if add_parents:
        payload['addParents'] = add_parents
    if remove_parents:
        payload['removeParents'] = remove_parents
    if add_shareds:
        payload['addShareds'] = add_shareds
    if remove_shareds:
        payload['removeShareds'] = remove_shareds
    if metadata:
        payload['metadata'] = metadata
    if custom_fields:
        payload['customFields'] = custom_fields
    if project:
        payload['project'] = project
    if user_access_roles:
        payload['userAccessRoles'] = user_access_roles
    if with_invitations is not None:
        payload['withInvitations'] = with_invitations

    return wrike_put(url=update_folder_url, payload=payload, verbose=verbose)


def update_project(project_id, title=None, description=None, add_parents=None, remove_parents=None,
                   add_shareds=None, remove_shareds=None, metadata=None, custom_fields=None, owners_add=None,
                   owners_remove=None, custom_status_id=None, start_date=None, end_date=None, contract_type=None,
                   budget=None, user_access_roles=None, with_invitations=None, verbose=False):
    """
    Updates existing project in Wrike. The following parameters are optional:

        title, description, add_parents, remove_parents, add_shareds, remove_shareds, metadata, custom_fields,
        project details (owners_add, owners_remove, custom_status_id, start_date, end_date, contract_type, budget),
        user_access_roles, with_invitations

    Constructs PUT request to 'folders/{project_id}' endpoint, where project_id is ID of the project to be updated.

    Parameters to pass into this function, as follows:

        project_id = 'IEAVJOU5I4AB5BKC'
        title = 'Updated Project Title'
        description = 'Updated project description'
        add_parents = ['IEAVJOU5I7777777']
        remove_parents = ['IEAVJOU5I4AB5BKA']
        add_shareds = ['KUAAAABF']
        remove_shareds = ['KUAAAABG']
        metadata = [{'key': 'updatedMetaKey', 'value': 'updatedMetaValue'}]
        custom_fields = [{'id': 'IEAVJOU5JUAAAACG', 'value': 'updatedValue'}]
        owners_add = ['KUAAAABF']
        owners_remove = ['KUAAAABG']
        custom_status_id = 'IEAVJOU5JMAAAAAA'
        start_date = '2024-10-01'
        end_date = '2024-10-15'
        contract_type = 'Billable'
        budget = 5000
        user_access_roles = {'KUAAAABF': 'IEAVJOU5ND777777'}
        with_invitations = True

    Returned API response IN JSON format, as follows:

        {
            'id': 'IEAAB3DEI5M5NKRM',
            'accountId': 'IEAAB3DE',
            'title': 'Updated Project Title',
            'createdDate': '2024-10-06T22:32:37Z',
            'updatedDate': '2024-10-06T22:44:46Z',
            'description': 'Updated project description',
            'sharedIds': ['KUAFMCAH', 'KUALDPDC', 'KUAP3YOD'],
            'parentIds': ['IEAAB3DEI5M4KMIP'],
            'childIds': [],
            'superParentIds': [],
            'scope': 'WsProject',
            'hasAttachments': False,
            'permalink': 'https://www.wrike.com/open.htm?id=1507240492',
            'workflowId': 'IEAAB3DEK7776E44',
            'metadata': [
                {
                    'key': 'updatedMetaKey',
                    'value': 'updatedMetaValue'
                }
            ],
            'customFields': [
                {
                    'id': 'IEAVJOU5JUAAAACG',
                    'value': 'updatedValue'
                }
            ],
            'project': {
                'authorId': 'KUAAAABF',
                'ownerIds': ['KUAAAABF'],
                'customStatusId': 'IEAVJOU5JMAAAAAA',
                'startDate': '2024-10-01',
                'endDate': '2024-10-15',
                'contractType': 'Billable',
                'budget': 5000,
                'createdDate': '2024-10-06T22:32:37Z',
                'completedDate': null
            },
            'userAccessRoles': {
                'KUAAAABG': [
                    'IEAVJOU5ND777777'
                ],
                'KUAAAABF': [
                    'IEAVJOU5ND777777'
                ]
            }
        }

    :param project_id:          str, required           ID of project to be updated
    :param title:               str, optional           new title for project
    :param description:         str, optional           updated description of project
    :param add_parents:         list, optional          parent folder IDs to add
    :param remove_parents:      list, optional          parent folder IDs to remove
    :param add_shareds:         list, optional          user IDs to add to shared users
    :param remove_shareds:      list, optional          user IDs to remove from shared users
    :param metadata:            list, optional          metadata entries (key-value pairs) to update
    :param custom_fields:       list, optional          custom field dict entries to update
    :param owners_add:          list, optional          user ID list to add as project owners
    :param owners_remove:       list, optional          user ID list to remove from project owners
    :param custom_status_id:    str, optional           custom status ID for the project
    :param start_date:          str, optional           project start date (format: yyyy-MM-dd)
    :param end_date:            str, optional           project end date (format: yyyy-MM-dd)
    :param contract_type:       str, optional           contract type for project
    :param budget:              float, optional         budget for project
    :param user_access_roles:   dict, optional          user IDs and corresponding access roles
    :param with_invitations:    bool, optional          if True, include invitations in ownerIds and sharedIds list
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    dict                    API response with details of the updated project
    """

    update_project_url = WRIKE_BASE_URL + WRIKE_UPDATE_OR_DELETE_FOLDER_URL.format(project_id)
    print(update_project_url) if verbose else None

    payload = {}                                                            # construct required payload

    if title:                                                               # add optional fields if provided
        payload['title'] = title
    if description:
        payload['description'] = description
    if add_parents:
        payload['addParents'] = add_parents
    if remove_parents:
        payload['removeParents'] = remove_parents
    if add_shareds:
        payload['addShareds'] = add_shareds
    if remove_shareds:
        payload['removeShareds'] = remove_shareds
    if metadata:
        payload['metadata'] = metadata
    if custom_fields:
        payload['customFields'] = custom_fields

    project_payload = {}                                                    # add optional project-specific fields
    if owners_add:
        project_payload['ownersAdd'] = owners_add
    if owners_remove:
        project_payload['ownersRemove'] = owners_remove
    if custom_status_id:
        project_payload['customStatusId'] = custom_status_id
    if start_date:
        project_payload['startDate'] = start_date
    if end_date:
        project_payload['endDate'] = end_date
    if contract_type:
        project_payload['contractType'] = contract_type
    if budget:
        project_payload['budget'] = budget

    if project_payload:
        payload['project'] = project_payload

    if user_access_roles:
        payload['userAccessRoles'] = user_access_roles
    if with_invitations is not None:
        payload['withInvitations'] = with_invitations

    return wrike_put(url=update_project_url, payload=payload, verbose=verbose)
