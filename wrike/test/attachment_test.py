from wrike.wrike.attachment import (
    delete_attachment,
    download_attachment,
    get_attachments,
    get_attachments_in_space,
    update_attachment,
    upload_attachment
)


# ===== example variables ============================================================================================
attachment_id = ''
folder_id = ''
space_id = ''
task_id = ''

created_date_start = '2023-01-01T00:00:00Z'
created_date_end = '2023-12-31T23:59:59Z'

verbose = True
versions = True
with_urls = True

# sample value returned from get_attachments_in_space(space_id=space_id, slim_metadata=True)
test_json = [
    {'id': 'DBCCBM5NACG3DEI5', 'name': 'foo.txt', 'in_type': 'folder', 'in_type_title': 'folder_foo'},
    {'id': 'DBCCBM5NACG3DEI6', 'name': 'bar.jpg', 'in_type': 'folder', 'in_type_title': 'folder_bar'},
    {'id': 'DBCCBM5NACG3DEI7', 'name': 'baz.xlsx', 'in_type': 'folder', 'in_type_title': 'folder_baz'}
]


# ===== example usage of attachment functions ========================================================================

# return a JSON of all attachments in account
get_attachments(
    versions=versions,
    created_date_start=created_date_start,
    created_date_end=created_date_end,
    with_urls=with_urls,
    verbose=verbose
)

# return a JSON of all attachments in a folder or task
get_attachments(
    folder_id=folder_id,                                                        # get all attachments in folder
    # task_id=task_id,                                                          # get all attachments in task
    versions=versions,
    created_date_start=created_date_start,
    created_date_end=created_date_end,
    with_urls=with_urls,
    verbose=verbose
)

# return a JSON of all attachments in a space; todo: see https://github.com/heynicejacket/wrike-api-101/issues/1
get_attachments_in_space(
    space_id=space_id,
    slim_metadata=False,                                                        # to return full JSON
    # slim_metadata=True,                                                       # to return limited JSON
    verbose=verbose
)

# download single attachment using a single attachment ID string
download_attachment(
    attachment_id=attachment_id,
    filepath=f'C:/path/to/save/',
    verbose=verbose
)

# download multiple attachments using a list of attachment ID strings
download_attachment(
    attachment_id=['', '', ''],
    filepath=f'C:/path/to/save/',
    verbose=verbose
)

# download multiple attachments from list of dicts returned from get_wrike_attachments_in_space(space_id=SPACE_ID)
download_attachment(
    attachment_id=test_json,
    filepath=f'C:/path/to/save/',
    verbose=verbose
)

# upload attachment to a task
upload_attachment(
    filepath=f'C:/path/to/foo.jpg',
    task_id=task_id,
    verbose=verbose
)

# upload attachment to a folder
upload_attachment(
    filepath=f'C:/path/to/bar.jpg',
    folder_id=folder_id,
    verbose=verbose
)

# update an existing attachment
update_attachment(
    attachment_id=attachment_id,
    filepath=f'C:/path/to/baz.jpg',
    filename='baz.jpg',
    verbose=verbose
)

# delete an attachment
delete_attachment(attachment_id=attachment_id, verbose=verbose)
