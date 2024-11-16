from wrike.core.api import (
    wrike_delete,
    wrike_get,
    wrike_post,
    wrike_put
)

from wrike.core.constants import (
    WRIKE_BASE_URL,
    WRIKE_COMMENTS_URL,
    WRIKE_FOLDER_URL,
    WRIKE_TASK_URL
)


def create_comment(text, task_id=None, folder_id=None, plain_text=True, verbose=False):
    """
    Creates a comment in a specified task or folder in Wrike. If both task_id and folder_id are provided, an error
    is raised.

    :param text:                str, required           comment text
    :param task_id:             str, optional           Wrike task ID for which to create comment
    :param folder_id:           str, optional           Wrike folder ID for which to create comment
    :param plain_text:          bool, optional          if True, treat comment text as plain text
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response with comment details
    """

    if task_id and folder_id:
        raise ValueError('Either \'task_id\' or \'folder_id\' must be provided, not both.')

    if not task_id and not folder_id:
        raise ValueError('Either \'task_id\' or \'folder_id\' must be provided.')

    if task_id:
        create_comment_url = WRIKE_BASE_URL + WRIKE_TASK_URL + f'{task_id}/' + WRIKE_COMMENTS_URL
    elif folder_id:
        create_comment_url = WRIKE_BASE_URL + WRIKE_FOLDER_URL + f'{folder_id}/' + WRIKE_COMMENTS_URL
    print(create_comment_url) if verbose else None

    payload = {
        'text': text,
        'plainText': plain_text
    }

    response = wrike_post(url=create_comment_url, payload=payload, verbose=verbose)

    return response if response else {}


def delete_comment(comment_id, verbose=False):
    """
    Deletes a comment in Wrike, given the comment ID.

    :param comment_id:          str, required           ID of comment to delete
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format or None if an error occurred
    """

    delete_comment_url = WRIKE_BASE_URL + f'/comments/{comment_id}'
    print(delete_comment_url) if verbose else None

    response = wrike_delete(url=delete_comment_url, verbose=verbose)

    return response if response else {}


def get_comments(task_id=None, folder_id=None, limit=None, verbose=False):
    """
    Retrieves comments in Wrike based on the provided task_id or folder_id. If neither is provided, returns all
    comments in the current account.

    Comment JSON returned as follows:

        [
            {
                'id': 'DBCCBM5NACG3DEI5',
                'authorId': 'FJDSKSA',
                'text': 'comment on task',
                'updatedDate': '2023-05-15T10:15:59Z',
                'createdDate': '2023-05-15T10:15:59Z',
                'taskId': 'DBCCBM5NACG3DEI5'
            },
            ...
        ]

    :param task_id:             str, optional           Wrike task ID to retrieve task-specific comments
    :param folder_id:           str, optional           Wrike folder ID to retrieve folder-specific comments
    :param limit:               int, optional           limit number of comments returned
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response of comments based on provided parameters
    """

    if task_id and folder_id:
        raise ValueError('Either \'task_id\' or \'folder_id\' must be provided, not both.')

    if limit is not None:
        limit_url = '?limit={limit}'
    else:
        limit_url = ''

    # todo: simplify with const and verify
    if task_id:
        comments_url = WRIKE_BASE_URL + WRIKE_TASK_URL + f'{task_id}/comments' + limit_url
    elif folder_id:
        comments_url = WRIKE_BASE_URL + WRIKE_FOLDER_URL + f'{folder_id}/comments' + limit_url
    else:
        comments_url = WRIKE_BASE_URL + f'comments' + limit_url
    print(comments_url) if verbose else None

    comments = wrike_get(url=comments_url, verbose=verbose)

    return comments if comments else []


def update_comment(comment_id, text, plain_text=True, external_requester=None, verbose=False):
    """
    Updates a comment in a Wrike task or folder. You can also pass an external requester for email comments.

    external_requester must include 'id', 'firstName', 'email'; optionally 'lastName'.

    :param comment_id:          str, required           ID of comment to update
    :param text:                str, required           updated comment text
    :param plain_text:          bool, optional          if True, treat comment text as plain text
    :param external_requester:  dict, optional          external requester information in case of email comments
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response with comment details
    """

    update_comment_url = WRIKE_BASE_URL + WRIKE_COMMENTS_URL + f'{comment_id}'
    print(update_comment_url) if verbose else None

    payload = {
        'text': text,
        'plainText': plain_text
    }

    if external_requester:
        payload['externalRequester'] = external_requester

    response = wrike_put(url=update_comment_url, payload=payload, verbose=verbose)

    return response if response else {}
