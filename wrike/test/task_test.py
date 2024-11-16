from wrike.wrike.task import (
    create_task,
    delete_task,
    get_task_metadata,
    update_task
)


# ===== example variables ============================================================================================
folder_id = ''

task_description = 'Description of the task.'
task_description_new = 'Updated description of the task.'
task_title = 'Test Task'
task_title_new = 'Test Task Update'

space_id = ''

verbose = True


# ===== example usage ================================================================================================

# get all tasks in spaces available to user
get_task_metadata(
    space_id=None,
    folder_id=None,
    verbose=verbose
)

# get all tasks in a specific space
get_task_metadata(
    space_id=space_id,
    folder_id=None,
    slim_metadata=True,                                                         # get limited JSON metadata
    # slim_metadata=False,                                                      # get full JSON metadata
    verbose=verbose
)

# get all tasks in a specific folder
get_task_metadata(
    space_id=None,
    folder_id=folder_id,
    slim_metadata=True,                                                         # get limited JSON metadata
    # slim_metadata=False,                                                      # get full JSON metadata
    verbose=verbose
)

# create a new task and return the task_id
create_task(folder_id=folder_id, task_title=task_title, description=task_description, verbose=verbose)
task_id = create_task(folder_id=folder_id, task_title=task_title, description=task_description, verbose=verbose)[0]['id']

# update an existing task
update_task(
    task_id=task_id,
    task_title=task_title_new,
    description=task_description_new,
    verbose=verbose
)

# delete an existing task
delete_task(
    task_id=task_id,
    verbose=verbose
)
