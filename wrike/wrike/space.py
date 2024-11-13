from wrike.core.api import (
    wrike_delete,
    wrike_get,
    wrike_post,
    wrike_put
)

from wrike.core.constants import (
    WRIKE_BASE_URL,
    WRIKE_SPACE_URL,
    WRIKE_UPDATE_OR_DELETE_FOLDER_URL
)


def create_space(access_type, title, description=None, members=None, guest_role_id=None,
                 default_project_workflow_id=None, suggested_project_workflows=None, default_task_workflow_id=None,
                 suggested_task_workflows=None, fields=None, verbose=False):
    """
    Creates a new space in Wrike. The title and access type are required parameters. Other parameters are optional.

    Constructs a POST request to the '/spaces' endpoint.

    Returns JSON response confirming space has been created as follows:

        todo: add example

    :param access_type:                     str, required           space type (e.g., 'Public' or 'Private')
    :param title:                           str, required           title of space to be created
    :param description:                     str, optional           description of space
    :param members:                         list, optional          list of dicts containing member IDs and access roles
    :param guest_role_id:                   str, optional           guest role ID (only for public spaces)
    :param default_project_workflow_id:     str, optional           default project workflow ID
    :param suggested_project_workflows:     list, optional          suggested project workflows (list of workflow IDs)
    :param default_task_workflow_id:        str, optional           default task workflow ID
    :param suggested_task_workflows:        list, optional          suggested task workflows (list of workflow IDs)
    :param fields:                          list, optional          fields to include in the response model
    :param verbose:                         bool, optional          if True, print status to terminal
    :return:                                JSON                    API response in JSON format
    """

    create_space_url = WRIKE_BASE_URL + WRIKE_SPACE_URL
    print(create_space_url) if verbose else None

    payload = {                                                             # construct required payload
        'accessType': access_type,
        'title': title
    }

    if description:                                                         # add optional fields if provided
        payload['description'] = description
    if members:
        payload['members'] = members
    if guest_role_id:
        payload['guestRoleId'] = guest_role_id
    if default_project_workflow_id:
        payload['defaultProjectWorkflowId'] = default_project_workflow_id
    if suggested_project_workflows:
        payload['suggestedProjectWorkflows'] = suggested_project_workflows
    if default_task_workflow_id:
        payload['defaultTaskWorkflowId'] = default_task_workflow_id
    if suggested_task_workflows:
        payload['suggestedTaskWorkflows'] = suggested_task_workflows
    if fields:
        payload['fields'] = fields

    return wrike_post(url=create_space_url, payload=payload, verbose=verbose)


def delete_space(space_id, verbose=False):
    """
    Deletes an existing project in Wrike by moving it to the Recycle Bin, including all descendant folders and tasks
    unless they have parents outside the deletion scope.

    Returns JSON response confirming space has been deleted as follows:

        todo: add example

    :param space_id:            str, required           ID of folder or project to be deleted
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response, with details of deleted folder or project
    """

    delete_space_url = WRIKE_BASE_URL + WRIKE_UPDATE_OR_DELETE_FOLDER_URL.format(space_id)
    print(delete_space_url) if verbose else None

    return wrike_delete(url=delete_space_url, verbose=verbose)


def get_space_metadata(space_id='', return_all=False, verbose=False):
    """
    Returns a dictionary of Wrike Spaces metadata. If no space_id is provided, returns metadata of all Wrike spaces; if
    space_id is given, returns metadata only for that Space.

    Metadata structure for Wrike Spaces is as follows:

        {
            'kind': 'spaces',
            'data': [
                {
                    'id': 'IEAAB3DEI5M4KMIP',
                    ...
                },
                {
                    ...
                }
            ]
        }

    Metadata for each Space is as follows:

        'id': 'IEANB3AEI56MGSS1',
        'title': 'Wrike Space',
        'avatarUrl': 'https://www.wrike.com/static/spaceicons2/v3/6/space-avatar.png',
        'accessType': 'Public',
        'archived': False,
        'guestRoleId': 'IEAND3DEVD712645',
        'defaultProjectWorkflowId': 'IEAABUQW23DIEK4E',
        'defaultTaskWorkflowId': 'IEANEB3D1QUK4EX3'

    :param space_id:            str, optional           Wrike space ID to retrieve metadata from; if '', return all spaces
    :param return_all:          bool, optional          if True, only return data dictionary
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response of space metadata
    """

    space_url = WRIKE_BASE_URL + WRIKE_SPACE_URL + f'{space_id}'
    print(space_url) if verbose else None

    return wrike_get(url=space_url, return_all=return_all, verbose=verbose)


def get_space_name(space_id, verbose=False):
    """
    Given a Wrike Space ID, return the Name of the Wrike Space.

    :param space_id:            str, required           Wrike space ID to retrieve metadata from
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    str                     name of Wrike space
    """

    space_dict = get_space_metadata(space_id=space_id)
    space_name = next((item['title'] for item in space_dict if item['id'] == space_id), None)

    print(space_name) if verbose else None

    return space_name


def get_space_id(space_title, verbose=False):
    """
    Given a Wrike Space Name, return the ID of the Wrike Space.

    :param space_title:         str, required           space name to retrieve metadata from
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    str                     ID of Wrike space
    """

    space_dict = get_space_metadata()
    space_id = next((item['id'] for item in space_dict if item['title'] == space_title), None)

    print(space_id) if verbose else None

    return space_id


def update_space(space_id, title=None, description=None, access_type=None, guest_role_id=None,
                 default_project_workflow_id=None, suggested_project_workflows_add=None,
                 suggested_project_workflows_remove=None, default_task_workflow_id=None,
                 suggested_task_workflows_add=None, suggested_task_workflows_remove=None, members_add=None,
                 members_remove=None, members_update=None, fields=None, verbose=False):
    """
    Updates an existing space in Wrike. The following parameters are optional:

        title, description, access_type, guest_role_id, default_project_workflow_id,
        suggested_project_workflows_add, suggested_project_workflows_remove,
        default_task_workflow_id, suggested_task_workflows_add, suggested_task_workflows_remove,
        members_add, members_remove, members_update, fields

    Constructs a PUT request to the 'spaces/{space_id}' endpoint, where space_id is the ID of the space to be updated.

    URL to pass to requests.put(), as follows:

        https://www.wrike.com/api/v4/spaces/{space_id}

    :param space_id:                            str, required           ID of the space to be updated
    :param title:                               str, optional           new title for the space
    :param description:                         str, optional           updated description of the space
    :param access_type:                         str, optional           access type (e.g., 'Public', 'Private')
    :param guest_role_id:                       str, optional           guest role ID (available for public spaces only)
    :param default_project_workflow_id:         str, optional           default project workflow ID
    :param suggested_project_workflows_add:     list, optional          project workflow IDs to add
    :param suggested_project_workflows_remove:  list, optional          project workflow IDs to remove
    :param default_task_workflow_id:            str, optional           default task workflow ID
    :param suggested_task_workflows_add:        list, optional          task workflow IDs to add
    :param suggested_task_workflows_remove:     list, optional          task workflow IDs to remove
    :param members_add:                         list, optional          members to add (list of dicts with 'id', 'accessRoleId', 'isManager')
    :param members_remove:                      list, optional          members to remove (list of member IDs)
    :param members_update:                      list, optional          members to update (list of dicts with 'id', 'accessRoleId', 'isManager')
    :param fields:                              list, optional          optional fields to include in the response model
    :param verbose:                             bool, optional          if True, print status to terminal
    :return:                                    JSON                    API response in JSON format
    """

    update_space_url = WRIKE_BASE_URL + WRIKE_SPACE_URL + f'{space_id}'
    print(update_space_url) if verbose else None

    payload = {}                                                            # construct the payload

    if title:                                                               # add optional fields if provided
        payload['title'] = title
    if description:
        payload['description'] = description
    if access_type:
        payload['accessType'] = access_type
    if guest_role_id:
        payload['guestRoleId'] = guest_role_id
    if default_project_workflow_id:
        payload['defaultProjectWorkflowId'] = default_project_workflow_id
    if suggested_project_workflows_add:
        payload['suggestedProjectWorkflowsAdd'] = suggested_project_workflows_add
    if suggested_project_workflows_remove:
        payload['suggestedProjectWorkflowsRemove'] = suggested_project_workflows_remove
    if default_task_workflow_id:
        payload['defaultTaskWorkflowId'] = default_task_workflow_id
    if suggested_task_workflows_add:
        payload['suggestedTaskWorkflowsAdd'] = suggested_task_workflows_add
    if suggested_task_workflows_remove:
        payload['suggestedTaskWorkflowsRemove'] = suggested_task_workflows_remove
    if members_add:
        payload['membersAdd'] = members_add
    if members_remove:
        payload['membersRemove'] = members_remove
    if members_update:
        payload['membersUpdate'] = members_update
    if fields:
        payload['fields'] = fields

    return wrike_put(url=update_space_url, payload=payload, verbose=verbose)
