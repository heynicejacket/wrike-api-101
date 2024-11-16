from wrike.wrike.workflow import (
    create_workflow,
    get_workflow_id,
    get_workflow_metadata,
    get_workflow_name,
    get_custom_statuses_by_id,
    update_workflow
)

# ===== example variables ============================================================================================
custom_status = [{'name': 'Test Workflow Status', 'color': 'Green', 'group': 'Active'}]

verbose = True

workflow_id = ''
workflow_name = 'Test Workflow'
workflow_name_new = 'Test Workflow Update'



# ===== example usage ================================================================================================

# get workflow metadata for all workflows available to user
get_workflow_metadata(verbose=verbose)

# get workflow name from workflow id
get_workflow_name(
    workflow_id=workflow_id,
    verbose=verbose
)

# get workflow id from workflow name
get_workflow_id(
    workflow_name=workflow_name,
    verbose=verbose)


# get custom statuses from workflow id
get_custom_statuses_by_id(
    workflow_id=workflow_id,
    verbose=verbose
)

# create new workflow
create_workflow(
    workflow_name=workflow_name,
    verbose=verbose
)

# update an existing workflow
update_workflow(
    workflow_id=workflow_id,
    workflow_name=workflow_name_new,
    custom_status=custom_status,
    verbose=verbose
)

# note: there is no API function to delete workflow
