from wrike.wrike.user import (
    get_user,
    get_users_all,
    get_user_types,
    update_user
)

# ===== example variables ============================================================================================
account_id = ''

user_id = ''
user_role = 'Collaborator'

verbose = True


# ===== example usage ================================================================================================

# get user types
get_user_types(verbose=verbose)

# get all users (contacts)
get_users_all(
    deleted=False,
    return_all=False,
    verbose=verbose
)

# get an existing user
get_user(
    user_id=user_id,
    verbose=verbose
)

# modify an existing user
update_user(
    user_id=user_id,
    account_id=account_id,
    role=user_role,
    verbose=verbose
)
