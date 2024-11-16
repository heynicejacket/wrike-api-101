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
    WRIKE_TASK_URL
)

from wrike.core.toolkit import (
    get_all_ids,
)

from wrike.wrike.folder_project import (
    extract_folder_or_project_hierarchy,
    folder_level_map,
    get_folder_or_project_metadata,
)


def add_level_to_tasks(tasks, folder_level_mapping, folder_id=None, level=None, verbose=False):
    """
    Adds the 'level' key-value pair to each task in the list of tasks.

    Given a folder hierarchy in a Wrike space, like so:

        hierarchy                 folder  task
        ------------------------  ------  ----
        /wrike_space
            task                           0
            ../folder               0
                task                       1
                task                       1
            ../folder               0
                ../folder           1
                    task                   2
            ../folder_blah          0
                ../folder           1
                    ../folder       2
                        task               3

    When applying the folder hierarchy to tasks, etc., we must add 1 to differentiate from tasks at the space level;
    otherwise, tasks at the space level and tasks at the 0th folder level, will both appear to be at the space level.
    Thus, 1 is added in this function, here:

        task.update({'level': folder_level + 1})

    :param tasks:                   list, required      list of task dictionaries
    :param folder_level_mapping:    dict, required      dict mapping folder IDs to their levels
    :param folder_id:               str, optional       folder ID for which level needs to be added
    :param level:                   int, optional       level to set for space-level tasks
    :param verbose:                 bool, optional      if True, print status to terminal
    :return:                        list                updated list of tasks with 'level' key added
    """

    # for space-level tasks where a specific level is given
    if level is not None:
        [task.update({'level': level}) for task in tasks]

    # for folder-level tasks where level is determined by the folder ID
    elif folder_id:
        folder_level = folder_level_mapping.get(folder_id, 0)
        for task in tasks:
            task.update({'level': folder_level + 1})

    return tasks


def create_task(folder_id, task_title, description=None, status=None, importance=None, dates=None, shareds=None,
                responsibles=None, followers=None, super_tasks=None, custom_fields=None, metadata=None, follow=None,
                priority_before=None, priority_after=None, verbose=False):
    """
    Creates a new task in Wrike within a specified folder. The title and folder ID are required parameters. Other
    parameters are optional.

    Constructs a POST request to the '/folders/{folderId}/tasks' endpoint.

    Example usage:

        create_wrike_task(
            folder_id='DBCCBM5NACG3DEI5',
            task_title='New Task',
            description='A new task description.',
            ...
            verbose=True
        )

    Returns as follows:

        [
            {
                'id': 'DBCCBM5NACG3DEI5',
                'accountId': 'FJDSKSA',
                'title': 'Test new task',
                'description': 'Test task description.',
                ...
            }
        ]

    :param folder_id:           str, required           folder ID where task will be created
    :param task_title:          str, required           title of task to be created
    :param description:         str, optional           description of task
    :param status:              str, optional           status of task (e.g., 'Active', 'Completed')
    :param importance:          str, optional           importance of task (e.g., 'High', 'Normal', 'Low')
    :param dates:               dict, optional          task dates, including start, due, and duration
    :param shareds:             list, optional          list of user IDs with whom task is shared
    :param responsibles:        list, optional          list of user IDs who are responsible for task
    :param followers:           list, optional          list of user IDs who are followers of task
    :param super_tasks:         list, optional          list of task IDs that will act as super tasks (for subtasks)
    :param custom_fields:       list, optional          custom fields for task
    :param metadata:            list, optional          task metadata (key-value pairs)
    :param follow:              bool, optional          if True, follow task
    :param priority_before:     str, optional           ID of task before which new task should be placed
    :param priority_after:      str, optional           ID of task after which new task should be placed
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format
    """

    create_task_url = WRIKE_BASE_URL + WRIKE_FOLDER_URL + f'{folder_id}/' + WRIKE_TASK_URL
    print(create_task_url) if verbose else None

    payload = {
        'title': task_title
    }

    if description:
        payload['description'] = description
    if status:
        payload['status'] = status
    if importance:
        payload['importance'] = importance
    if dates:
        payload['dates'] = dates
    if shareds:
        payload['shareds'] = shareds
    if responsibles:
        payload['responsibles'] = responsibles
    if followers:
        payload['followers'] = followers
    if super_tasks:
        payload['superTasks'] = super_tasks
    if custom_fields:
        payload['customFields'] = custom_fields
    if metadata:
        payload['metadata'] = metadata
    if follow is not None:
        payload['follow'] = follow
    if priority_before:
        payload['priorityBefore'] = priority_before
    if priority_after:
        payload['priorityAfter'] = priority_after

    return wrike_post(url=create_task_url, payload=payload, verbose=verbose)


def delete_task(task_id, verbose=False):
    """
    Deletes an existing task in Wrike by moving it to the Recycle Bin.

    URL to pass to requests.delete(), as follows:

        https://www.wrike.com/api/v4/tasks/DBCCBM5NACG3DEI5

    Returned API response in JSON, as follows:

        [
            {
                'id': 'DBCCBM5NACG3DEI5',
                'accountId': 'FJDSKSA',
                'title': 'Test new task',
                'description': 'Test task description.',
                'briefDescription': 'Test task description.',
                'parentIds': ['DBCCBM5NACG3DEI5'],
                'superParentIds': [],
                'sharedIds': ['FJDSKSA', 'FJDSKSB', 'FJDSKSC'],
                'responsibleIds': [],
                'status': 'Active',
                'importance': 'Normal',
                'createdDate': '2023-02-12T11:24:48Z',
                updatedDate': '2023-02-12T11:26:07Z',
                'dates': {'type': 'Backlog'},
                'scope': 'RbTask',
                'authorIds': ['FJDSKSA'],
                'customStatusId': 'DBCCBM5NACG3DEI5',
                'hasAttachments': False,
                'attachmentCount': 0,
                'permalink': 'https://www.wrike.com/open.htm?id=12345',
                'priority': '4256d00080000005236',
                'followedByMe': True,
                'followerIds': ['FJDSKSA'],
                'superTaskIds': [],
                'subTaskIds': [],
                'dependencyIds': [],
                'metadata': [],
                'customFields': []
            }
        ]

    :param task_id:             str, required           ID of task to be deleted
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response, with details of deleted task
    """

    delete_task_url = WRIKE_BASE_URL + WRIKE_TASK_URL + f'{task_id}'
    print(delete_task_url) if verbose else None

    return wrike_delete(url=delete_task_url, verbose=verbose)


def get_task_metadata(space_id=None, folder_id=None, slim_metadata=False, verbose=False):
    """


    If requesting tasks in a folder, returns a list of dicts as follows:

        ...

    If requesting all tasks in a space, returns a list of dicts as follows:

        [
            {'id': 'DBCCBM5NACG3DEI5', 'accountId': 'FJDSKSA', 'title': 'task_foo', ..., 'level': 0},
            {'id': 'DBCCBM5NACG3DEI6', 'accountId': 'FJDSKSA', 'title': 'task_bar', ..., 'level': 0},
            ...
            {'id': 'DBCCBM5NACG3DEI9', 'accountId': 'FJDSKSA', 'title': 'task_baz', ..., 'level': 1}
        ]

    If slim_metadata = True, returns only the following fields:

        [
            {'id': 'DBCCBM5NACG3DEI5', 'title': 'task_foo', 'level': 0},
            {'id': 'DBCCBM5NACG3DEI6', 'title': 'task_bar', 'level': 0},
            ...
            {'id': 'DBCCBM5NACG3DEI9', 'title': 'task_baz', 'level': 1}
        ]

    If space_id and folder_id are both None, returns all tasks in account.

    :param space_id:            str, optional           Wrike space ID to retrieve metadata from; if '', return all spaces
    :param folder_id:           str, optional           Wrike folder ID to retrieve metadata from
    :param slim_metadata:       bool, optional          if True, returns a limited JSON dict
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    list                    tasks metadata as list of dicts
    """

    if space_id and folder_id:
        raise ValueError('Cannot specify both space_id and folder_id. Only one or neither can be provided.')

    elif space_id is not None:

        # return all tasks in a space; https://www.wrike.com/api/v4/spaces/
        tasks_url = WRIKE_BASE_URL + WRIKE_SPACE_URL + f'{space_id}/' + WRIKE_TASK_URL
        print(tasks_url) if verbose else None

        list_of_tasks = []

        # get tasks at space level and add hierarchy
        t_meta_space_level = wrike_get(url=tasks_url, get_projects=None, verbose=verbose)
        if slim_metadata:
            t_meta_space_level = extract_folder_or_project_hierarchy(data=t_meta_space_level, verbose=verbose)

        # add 'level': 0 for space-level tasks
        list_of_tasks.extend(add_level_to_tasks(t_meta_space_level, folder_level_mapping=None, level=0))

        # get folder metadata and make a list of folder ids
        folder_metadata = get_folder_or_project_metadata(space_id=space_id, get_projects=False, verbose=verbose)
        folder_id_list = get_all_ids(data=folder_metadata, verbose=verbose)

        # create folder-level mapping
        folder_level_mapping = folder_level_map(folder_metadata=folder_metadata, verbose=verbose)

        # for each folder, if tasks exist in folder, append to list_of_tasks
        for folder_id in folder_id_list:
            task_url = WRIKE_BASE_URL + WRIKE_FOLDER_URL + f'{folder_id}/' + WRIKE_TASK_URL
            folder_level_task = wrike_get(url=task_url, get_projects=None, verbose=verbose)

            if slim_metadata:
                folder_level_task = extract_folder_or_project_hierarchy(data=folder_level_task, verbose=verbose)

            # add 'level' from folder metadata to folder tasks
            if folder_level_task:
                list_of_tasks.extend(add_level_to_tasks(folder_level_task, folder_level_mapping=folder_level_mapping, folder_id=folder_id))

        return list_of_tasks

    elif folder_id is not None:
        # return all tasks in a folder; https://www.wrike.com/api/v4/folders/{folder_id}/tasks/
        tasks_url = WRIKE_BASE_URL + WRIKE_FOLDER_URL + f'{folder_id}/' + WRIKE_TASK_URL
        print(tasks_url) if verbose else None

    else:
        # return all tasks in an account; https://www.wrike.com/api/v4/tasks/
        tasks_url = WRIKE_BASE_URL + WRIKE_TASK_URL
        print(tasks_url) if verbose else None

    list_of_tasks = wrike_get(url=tasks_url, get_projects=None, verbose=verbose)

    return list_of_tasks


def update_task(task_id, task_title=None, description=None, status=None, importance=None, dates=None, add_parents=None,
                remove_parents=None, add_shareds=None, remove_shareds=None, add_responsibles=None,
                remove_responsibles=None, add_followers=None, remove_followers=None, custom_fields=None,
                add_super_tasks=None, remove_super_tasks=None, metadata=None, verbose=False):
    """
    Updates an existing task in Wrike. The following parameters are optional:

        title, description, status, importance, dates, add_parents, remove_parents,
        add_shareds, remove_shareds, add_responsibles, remove_responsibles, add_followers,
        remove_followers, custom_fields, add_super_tasks, remove_super_tasks, metadata

    Constructs a PUT request to the 'tasks/{task_id}' endpoint, where task_id is the ID of the task to be updated.

    URL to pass to requests.put(), as follows:

        https://www.wrike.com/api/v4/tasks/{task_id}

    :param task_id:                 str, required           ID of task to be updated
    :param task_title:              str, optional           new title for task
    :param description:             str, optional           updated description of task
    :param status:                  str, optional           updated status of task
    :param importance:              str, optional           task importance (e.g., 'Low', 'High')
    :param dates:                   dict, optional          task dates (start, due, duration)
    :param add_parents:             list, optional          folders to add task to (list of folder IDs)
    :param remove_parents:          list, optional          folders to remove task from (list of folder IDs)
    :param add_shareds:             list, optional          users to share task with (list of user IDs)
    :param remove_shareds:          list, optional          users to unshare task from (list of user IDs)
    :param add_responsibles:        list, optional          users to assign to task (list of user IDs)
    :param remove_responsibles:     list, optional          users to unassign from task (list of user IDs)
    :param add_followers:           list, optional          users to add as followers (list of user IDs)
    :param remove_followers:        list, optional          users to remove as followers (list of user IDs)
    :param custom_fields:           list, optional          custom fields to update (list of dicts with 'id' and 'value')
    :param add_super_tasks:         list, optional          tasks to add as super tasks (list of task IDs)
    :param remove_super_tasks:      list, optional          tasks to remove from super tasks (list of task IDs)
    :param metadata:                list, optional          metadata entries (list of dicts with 'key' and 'value')
    :param verbose:                 bool, optional          if True, print status to terminal
    :return:                        JSON                    API response in JSON format
    """

    update_task_url = WRIKE_BASE_URL + WRIKE_TASK_URL + f'{task_id}'
    print(update_task_url) if verbose else None

    payload = {}

    if task_title:
        payload['title'] = task_title
    if description:
        payload['description'] = description
    if status:
        payload['status'] = status
    if importance:
        payload['importance'] = importance
    if dates:
        payload['dates'] = dates
    if add_parents:
        payload['addParents'] = add_parents
    if remove_parents:
        payload['removeParents'] = remove_parents
    if add_shareds:
        payload['addShareds'] = add_shareds
    if remove_shareds:
        payload['removeShareds'] = remove_shareds
    if add_responsibles:
        payload['addResponsibles'] = add_responsibles
    if remove_responsibles:
        payload['removeResponsibles'] = remove_responsibles
    if add_followers:
        payload['addFollowers'] = add_followers
    if remove_followers:
        payload['removeFollowers'] = remove_followers
    if custom_fields:
        payload['customFields'] = custom_fields
    if add_super_tasks:
        payload['addSuperTasks'] = add_super_tasks
    if remove_super_tasks:
        payload['removeSuperTasks'] = remove_super_tasks
    if metadata:
        payload['metadata'] = metadata

    return wrike_put(url=update_task_url, payload=payload, verbose=verbose)
