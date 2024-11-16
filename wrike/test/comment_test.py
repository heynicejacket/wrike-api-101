from wrike.wrike.comment import (
    create_comment,
    delete_comment,
    get_comments,
    update_comment
)


# ===== example variables ============================================================================================
comment_id = ''
comment_text = 'New comment.'

folder_id = ''
task_id = ''

verbose = True


# ===== example usage ================================================================================================

# return a JSON of all comments in an account
get_comments(verbose=verbose)

# return a JSON of all comments in a folder or task
get_comments(
    folder_id=folder_id,                                                        # get all comments in folder
    # task_id=task_id,                                                          # get all comments in task
    verbose=verbose
)

# create a comment in a folder or task
create_comment(
    text=comment_text,
    folder_id=folder_id,                                                        # create comment in folder
    # task_id=task_id,                                                          # create comment in task
    verbose=verbose
)

# update an existing comment
update_comment(
    comment_id=comment_id,
    text=comment_text,
    verbose=verbose
)

# delete an existing comment
delete_comment(
    comment_id=comment_id,
    verbose=verbose
)
