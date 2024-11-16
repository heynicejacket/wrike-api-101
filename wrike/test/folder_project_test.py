from wrike.wrike.folder_project import (
    create_folder,
    create_project,
    delete_folder_or_project,
    get_folder_or_project_id,
    get_folder_or_project_metadata,
    get_folder_or_project_name,
    update_folder,
    update_project
)


# ===== example variables ============================================================================================
folder_id = ''
folder_title = 'Test Folder'
folder_title_new = 'Test Folder Update'

project_id = ''
project_description = 'Description of the project.'
project_description_new = 'Updated description of the project.'
project_title = 'Test Project'
project_title_new = 'Test Project Update'

space_id = ''

verbose = True


# ===== example usage: get_folder_or_project_metadata() ==============================================================

# get all projects and folders in a space
get_folder_or_project_metadata(
    space_id=space_id,
    get_projects=None,                                                          # get all projects and folders
    # get_projects=True,                                                        # get all projects
    # get_projects=False,                                                       # get all folders
    verbose=verbose
)


# ===== example usage: folders =======================================================================================

# get folder name from folder id
get_folder_or_project_name(
    space_id=space_id,
    folder_id=folder_id,
    verbose=verbose
)

# get folder id from folder name
get_folder_or_project_id(
    space_id=space_id,
    folder_title=folder_title,
    verbose=verbose
)

# create new folder
create_folder(
    space_or_folder_id=space_id,
    space_title=folder_title_new,
    verbose=verbose
)

# update an existing folder
folder_id = get_folder_or_project_id(space_id=space_id, folder_title=folder_title, verbose=verbose)
update_folder(
    folder_id=folder_id,
    space_title=folder_title_new,
    verbose=verbose
)

# delete an existing folder
folder_id = get_folder_or_project_id(space_id=space_id, folder_title=folder_title, verbose=verbose)
delete_folder_or_project(
    folder_or_project_id=folder_id,
    verbose=verbose
)


# ===== example usage: projects ======================================================================================

# get project name from project id
get_folder_or_project_name(
    space_id=space_id,
    project_id=project_id,
    verbose=verbose
)

# get project id from project name
get_folder_or_project_id(
    space_id=space_id,
    project_title=project_title,
    verbose=verbose
)

# create a new project
create_project(
    space_or_folder_id=folder_id,
    project_title=project_title,
    description=project_description,
    verbose=verbose
)

# update an existing project
project_id = get_folder_or_project_id(space_id=space_id, project_title=project_title, verbose=verbose)
update_project(
    project_id=project_id,
    space_title=project_title_new,
    description=project_description_new,
    verbose=verbose
)

# delete an existing project
project_id = get_folder_or_project_id(space_id=space_id, project_title=project_title_new, verbose=verbose)
delete_folder_or_project(
    folder_or_project_id=project_id,
    verbose=verbose
)
