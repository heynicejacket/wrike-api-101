from wrike.core.sql import (
    create_engine
)

from wrike.wrike.data_export import (
    get_data_export_urls,
    data_export_to_csv,
    data_export_to_sql
)


# ===== example variables ============================================================================================
reporting_tables = [
    'user', 'work_workflow_stage_history', 'workflow_stage', 'work_assignee',
    'work_item', 'work_custom_field', 'work_graph'
]
verbose = True


# ===== example objects ==============================================================================================
engine = create_engine(
    db='',
    dialect='',
    user='',
    password='',
    endpoint='',
    verbose=verbose
)


# ===== example usage ================================================================================================

# return a dictionary of table names and CSV URLs for data extraction
get_data_export_urls(
    filtered_list=None,                                                         # default option, returns all tables
    # filtered_list=reporting_tables,                                             # returns only tables named in list
    verbose=verbose
)

# given a dict of Wrike data tables and URLs, save as CSV files
data_export = get_data_export_urls(filtered_list=reporting_tables, verbose=verbose)
data_export_to_csv(
    data_export_dict=data_export,
    output_dir=f'C:/localtemp/',
    tbl_prefix='wrike_',
    verbose=verbose
)

# given a dict of Wrike data tables and URLs, save as SQL tables
data_export = get_data_export_urls(filtered_list=reporting_tables, verbose=verbose)
data_export_to_sql(
    data_export_dict=data_export,
    engine=engine,
    if_exists='replace',
    tbl_prefix='wrike_',
    verbose=False
)
