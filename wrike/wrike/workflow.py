from wrike.core.api import (
    wrike_get,
    wrike_post,
    wrike_put
)

from wrike.core.constants import (
    WRIKE_BASE_URL,
    WRIKE_WORKFLOWS_URL
)


def create_workflow(workflow_name, verbose=False):
    """
    Given a workflow name, creates a new workflow in Wrike.

    Wrike workflows must be created before they are modified or populated with additional fields, as the workflow ID
    is required for this process.

    :param workflow_name:       str, required           name of Wrike workflow to create
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response containing workflow metadata
    """

    workflow_url = WRIKE_BASE_URL + WRIKE_WORKFLOWS_URL                     # 'https://www.wrike.com/api/v4/workflows'
    print(workflow_url) if verbose else None

    payload = {'name': workflow_name, }                                     # construct required payload

    return wrike_post(url=workflow_url, payload=payload, verbose=False)


def get_custom_statuses_by_id(workflow_id, verbose=False):
    """
    Retrieve the customStatuses list of dicts for a given workflow ID.

    Custom status list appears as follows:

        [
            {
                'id': 'IEAABD3EK3XOKC4U',
                'name': 'Workspace',
                'standard': False,
                'hidden': False,
                'customStatuses': [
                    {
                        'id': 'IEAAB3DEJMCXOK4U',
                        'name': 'New Invoice',
                        'standardName': False,
                        'color': 'Blue',
                        'standard': False,
                        'group': 'Active',
                        'hidden': False
                    },
                    ...
                ]
            },
            ...
        ]

    List returned is as follows:

        'customStatuses': [
            {
                'id': 'IEAAB3DEJMCXOK4U',
                'name': 'New Invoice',
                'standardName': False,
                'color': 'Blue',
                'standard': False,
                'group': 'Active',
                'hidden': False
            },
            ...
        ]

    :param workflow_id:         str, required           workflow ID to return custom statuses
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    list                    customStatuses list of dicts
    """

    workflows = get_workflow_metadata(verbose=verbose)

    for workflow in workflows:
        if workflow.get('id') == workflow_id:
            return workflow.get('customStatuses', [])

    return []


def get_workflow_id(workflow_name, verbose=False):
    """
    Retrieve the ID of a Wrike workflow based on its name.

    :param workflow_name:       str, required           workflow name to retrieve ID for
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    str                     workflow ID
    """

    workflow_dict = get_workflow_metadata()
    workflow_id = next((item['id'] for item in workflow_dict if item['name'] == workflow_name), None)

    print(workflow_id) if verbose else None

    return workflow_id


def get_workflow_metadata(return_all=False, verbose=False):
    """
    Retrieves all workflows from Wrike for the entire account. Wrike does not support limiting workflows to a single
    space, so this function retrieves all custom workflows available across the account.

    :param return_all:          bool, optional          if True, only return data dict; else, entire json dict
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response containing workflow metadata
    """

    workspace_url = WRIKE_BASE_URL + WRIKE_WORKFLOWS_URL
    print(workspace_url) if verbose else None

    return wrike_get(url=workspace_url, return_all=return_all, verbose=verbose)


def get_workflow_name(workflow_id, verbose=False):
    """
    Retrieve the name of a Wrike workflow based on its ID.

    :param workflow_id:         str, required           workflow ID to retrieve name for
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    str                     name of Wrike workflow
    """

    workflow_dict = get_workflow_metadata()
    workflow_name = next((item['name'] for item in workflow_dict if item['id'] == workflow_id), None)

    print(workflow_name) if verbose else None

    return workflow_name


def update_workflow(workflow_id, name=None, hidden=None, custom_status=None, verbose=False):
    """
    Updates a Wrike workflow with new attributes such as name, visibility, and custom statuses.

    This function sends a PUT request to the Wrike API to modify the properties of an existing workflow.
    It allows optional updates to the workflow's name, visibility (hidden), and custom status list.

    custom_status list of dicts specifies custom statuses to update within the workflow. Each dictionary should define
    a custom status with necessary details like 'id', 'name', or other attributes as required by the Wrike API.

    :param workflow_id:         str, required           ID of workflow to update
    :param name:                str, optional           new name for workflow; if not provided, name remains unchanged
    :param hidden:              bool, optional          if True, sets workflow to hidden; if False, sets to visible
    :param custom_status:       JSON, optional          custom statuses to update within workflow
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response containing updated workflow details
    """

    update_workflow_url = WRIKE_BASE_URL + WRIKE_WORKFLOWS_URL + f'{workflow_id}'
    print(update_workflow_url) if verbose else None

    payload = {}

    if name is not None:
        payload['name'] = name
    if hidden is not None:
        payload['hidden'] = hidden
    if custom_status is not None:
        payload['customStatus'] = custom_status

    print(payload) if verbose else None

    return wrike_put(url=update_workflow_url, payload=payload, verbose=verbose)
