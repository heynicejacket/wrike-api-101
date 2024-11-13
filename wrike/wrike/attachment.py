import os
import requests

from wrike.core.api import (
    wrike_delete,
    wrike_get,
    wrike_post_upload,
    wrike_put_upload
)

from wrike.core.constants import (
    WRIKE_BASE_URL,
    WRIKE_FOLDER_URL,
    WRIKE_ATTACHMENTS_URL,
    WRIKE_TASK_URL,
    WRIKE_DOWNLOAD_URL
)

from wrike.wrike.folder_project import (
    extract_folder_or_project_hierarchy,
    get_folder_or_project_dict
)

from wrike.wrike.task import (
    get_task_metadata
)

from wrike.core.toolkit import (
    get_all_ids
)


def delete_attachment(attachment_id, verbose=False):
    """
    Given an attachment ID, deletes attachment.

    :param attachment_id:       str, required           ID of attachment to be deleted
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response
    """

    delete_url = WRIKE_BASE_URL + WRIKE_ATTACHMENTS_URL + f'{attachment_id}'
    print(delete_url) if verbose else None

    try:
        response = wrike_delete(delete_url, return_all=True, verbose=verbose)
        print(f'Attachment {attachment_id} deleted successfully.') if verbose else None
        return response

    except requests.exceptions.RequestException as err:
        print(f'Error deleting attachment {attachment_id}: {err}') if verbose else None


def download_attachment(attachment_id, filepath, verbose=False):
    """
    Download attachments from Wrike and save to specified filepath.

    :param attachment_id:       str or list, required   str or list of attachment IDs, or list of dicts containing metadata
    :param filepath:            str, required           directory where files should be saved
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    list                    download URLs if verbose, else None
    """

    if isinstance(attachment_id, str):
        attachment_ids = [attachment_id]

    elif isinstance(attachment_id, list) and all(isinstance(item, dict) for item in attachment_id):
        attachment_ids = get_all_ids(data=attachment_id, verbose=verbose)

    elif isinstance(attachment_id, list):
        attachment_ids = attachment_id

    else:
        raise TypeError('attachment_id must be a string, a list, or a list of dicts.')

    download_url = WRIKE_BASE_URL + WRIKE_ATTACHMENTS_URL + '{0}/' + WRIKE_DOWNLOAD_URL
    print(download_url) if verbose else None

    list_of_download_urls = [
        wrike_get(url=download_url.format(a), return_all=True, verbose=verbose) for a in attachment_ids
    ]

    for download_info in list_of_download_urls:
        url = download_info['data'][0]['url']                                   # extract URL str from list of dicts
        filename = url.split('/')[-1]                                           # extract filename from URL
        full_filepath = os.path.join(filepath, filename)

        try:
            response = wrike_get(url, return_response=True, verbose=verbose)

            with open(full_filepath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f'File downloaded successfully to {full_filepath}')

        except requests.exceptions.RequestException as e:
            print(f'Error downloading {url}: {e}')

    return list_of_download_urls if verbose else None


def get_attachments(folder_id=None, task_id=None, versions=None, created_date_start=None, created_date_end=None, with_urls=None, verbose=False):
    """
    Fetches all attachments from Wrike with optional filters for versions, created date, and attachment URLs.

    :param folder_id:           str, optional           if provided, only return attachments in specified folder or project
    :param task_id:             str, optional           if provided, only return attachments in specified task
    :param versions:            bool, optional          if True, includes previous versions of attachments
    :param created_date_start:  str, optional           start of created date range (format: yyyy-MM-dd'T'HH:mm:ss'Z')
    :param created_date_end:    str, optional           end of created date range (format: yyyy-MM-dd'T'HH:mm:ss'Z')
    :param with_urls:           bool, optional          if True, includes URLs for attachments
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response containing attachments data
    """

    try:
        if folder_id and task_id:
            raise ValueError('Cannot specify both folder_id and task_id. Only one can be provided.')
        elif folder_id is not None:
            attachments_url = WRIKE_BASE_URL + WRIKE_FOLDER_URL + f'{folder_id}/' + WRIKE_ATTACHMENTS_URL
        elif task_id is not None:
            attachments_url = WRIKE_BASE_URL + WRIKE_TASK_URL + f'{task_id}/' + WRIKE_ATTACHMENTS_URL
        else:
            attachments_url = WRIKE_BASE_URL + WRIKE_ATTACHMENTS_URL
        print(attachments_url) if verbose else None

        params = {}                                                             # construct required payload

        if versions is not None:
            params['versions'] = str(versions).lower()

        if created_date_start or created_date_end:                              # add optional date fields if provided
            date_filter = {}
            if created_date_start:
                date_filter['start'] = created_date_start
            if created_date_end:
                date_filter['end'] = created_date_end
            params['createdDate'] = date_filter

        if with_urls is not None:                                               # add optional url field if provided
            params['withUrls'] = str(with_urls).lower()

        return wrike_get(url=attachments_url, return_all=False, verbose=verbose)

    except ValueError as e:
        print(f'Error: {e}')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')


def get_attachments_in_space(space_id, slim_metadata=False, verbose=False):
    """

    Given a Wrike space ID, returns a list of dicts containing metadata of all attachments in a given space.

    By default, returns as follows:

        [
            {'id': 'IEBCC46DTD4A4P', 'name': 'foo.txt', ..., 'in_type': 'folder', ..., 'in_type_title': 'folder_b'},
            {'id': 'IEBCC46DTD4A45', 'name': 'bar.jpg', ..., 'in_type': 'folder', ..., 'in_type_title': 'folder_b'},
            ...
        ]

    If slim_metadata = True, returns a limited set, as follows:

        [
            {'id': 'IEBCC46DTD4A4P', 'name': 'foo.txt', 'in_type': 'folder', 'in_type_title': 'folder_b'},
            {'id': 'IEBCC46DTD4A45', 'name': 'bar.jpg', 'in_type': 'folder', 'in_type_title': 'folder_b'},
            ...
        ]

    :param space_id:            str, required           ID of space to retrieve attachments from
    :param slim_metadata:       bool, optional          if True, returns a limited JSON dict
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response of attachment data
    """

    folder_and_project_dict = get_folder_or_project_dict(
        space_id=space_id, additional_keys=['title', 'level'], verbose=verbose
    )

    attachment_list = []

    for folder_or_project in folder_and_project_dict:
        attachments = get_attachments(folder_id=folder_or_project['id'], verbose=verbose)
        if attachments:                                                             # append if attachments is not None, empty
            attachment_list.extend(attachments)

    # get all attachments in tasks
    for folder_or_project in folder_and_project_dict:
        task_metadata = get_task_metadata(space_id=None, folder_id=folder_or_project['id'], verbose=verbose)

        if task_metadata:
            task_id_list = get_all_ids(data=task_metadata, verbose=verbose)

            for task_id in task_id_list:
                attachments = get_attachments(task_id=task_id, verbose=verbose)

                if attachments:
                    for attachment in attachments:                                  # add key-value pairs to attachment
                        attachment['in_type'] = folder_or_project['type']
                        attachment['in_type_title'] = folder_or_project['title']

                    attachment_list.extend(attachments)                             # append updated attachments to list

    if slim_metadata:
        attachment_list = extract_folder_or_project_hierarchy(
            data=attachment_list,
            additional_keys=['name', 'in_type', 'in_type_title'],
            verbose=verbose
        )

    return attachment_list


def update_attachment(attachment_id, filepath, filename, verbose=False):
    """
    Given the ID of an existing attachment and filepath and name of new attachment, replaces existing attachment.

    Updating an attachment changes its attachment_id; retrieve new attachment ID from JSON dict for new attachment ID.

    :param attachment_id:       str, required           ID of attachment to update
    :param filepath:            str, required           local filepath of file to be updated (e.g. 'C:\...\file.xlsx')
    :param filename:            str, required           name of file to be updated
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format
    """

    update_url = WRIKE_BASE_URL + WRIKE_ATTACHMENTS_URL + f'{attachment_id}'
    print(update_url) if verbose else None

    return wrike_put_upload(url=update_url, filepath=filepath, filename=filename, verbose=verbose)


def upload_attachment(filepath, task_id=None, folder_id=None, verbose=False):
    """
    Uploads a file to a Wrike task or folder.

    :param filepath:            str, required           path to local file to be uploaded
    :param task_id:             str, optional           task ID if uploading to task
    :param folder_id:           str, optional           folder ID if uploading to folder
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format
    """

    if not task_id and not folder_id:
        raise ValueError('Either task_id or folder_id must be provided.')

    if task_id and folder_id:
        raise ValueError('Only one of task_id or folder_id can be provided.')

    if task_id:
        upload_url = WRIKE_BASE_URL + WRIKE_TASK_URL + f'{task_id}' + WRIKE_ATTACHMENTS_URL
    else:
        upload_url = WRIKE_BASE_URL + WRIKE_FOLDER_URL + f'{task_id}' + WRIKE_ATTACHMENTS_URL
    print(upload_url) if verbose else None

    filename = os.path.basename(filepath)                                       # extract filename from filepath

    return wrike_post_upload(url=upload_url, filepath=filepath, filename=filename, verbose=verbose)
