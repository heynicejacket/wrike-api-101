from wrike.wrike.comment import (
    create_comment,
    delete_comment,
    get_comments,
    update_comment
)


# ===== example variables ============================================================================================
verbose = True


# ===== example usage ================================================================================================
# return a JSON of all comments in an account
get_comments(verbose=verbose)

# return a JSON of all comments in a folder
get_comments(
    folder_id='',
    verbose=verbose
)

# return a JSON of all comments in a task
get_comments(
    task_id='',
    verbose=verbose
)

# create a comment in a folder
create_comment(
    text='new folder comment',
    folder_id='',
    verbose=verbose
)

# create a comment in a task
create_comment(
    text='new task comment',
    task_id='',
    verbose=verbose
)

# update an existing comment in a folder
update_comment(
    comment_id='',
    text='update to new folder comment',
    verbose=verbose
)

# update an existing comment in a task
update_comment(
    comment_id='',
    text='update to new task comment',
    verbose=verbose
)

# delete an existing comment
delete_comment(
    comment_id='',
    verbose=verbose
)
