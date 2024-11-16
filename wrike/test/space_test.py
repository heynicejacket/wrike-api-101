from wrike.wrike.space import (
    create_space,
    delete_space,
    get_space_id,
    get_space_metadata,
    get_space_name,
    update_space
)


# ===== example variables ============================================================================================
space_access_type = 'Public'
space_id = ''
space_description = 'Description of the space.'
space_description_update = 'Updated description of the space.'
space_title = 'Test Space'
space_title_new = 'Test Space Update'

verbose = True


# ===== example usage ================================================================================================

# get space metadata
get_space_metadata(
    space_id=space_id,
    verbose=verbose
)

# get space name from space id
get_space_name(
    space_id=space_id,
    verbose=verbose
)

# get space id from space name
get_space_id(
    space_title=space_title,
    verbose=verbose
)

# create new space
create_space(
    access_type=space_access_type,
    space_title=space_title,
    description=space_description
)

# update an existing space
update_space(
    space_id=space_id,
    space_title=space_title_new,
    description=space_description_update
)

# delete an existing space
delete_space(
    space_id=space_id,
    verbose=verbose
)
