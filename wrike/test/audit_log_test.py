from wrike.wrike.audit_log import (
    get_audit_log,
    get_complete_audit_log,
    reframe_audit_log
)


# ===== example variables ============================================================================================
verbose = True

operations = ['TaskCreated']
event_date = {
    'start': '2023-02-01T07:51:44Z',
    'end': '2023-02-28T07:51:44Z'
}

audit_reformat_data = {'id': ['DBCCBM5NACG3DEI9'],
        'operation': ['TaskStatusChanged'],
        'userId': ['FJDSKSA'],
        'userEmail': ['matthew@nicejacket.cc'],
        'eventDate': ['2023-02-01T09:46:16Z'],
        'ipAddress': ['55.200.450.210'],
        'objectType': ['Task'],
        'objectName': ['Order confirmed'],
        'objectId': ['DBCCBM5NACG3DEI9'],
        'details': [
            {
                'Prev Status': 'Order Pending',
                'New Status': 'Order Confirmed',
                'Assignees': 'matthew@nicejacket.cc',
                'Work Item Link': 'https://www.wrike.com/open.htm?id=12345'}]
        }


# ===== example usage ================================================================================================

# return a JSON subset of the wrike audit log
get_audit_log(
    page_size=2,
    verbose=verbose
)

# return a DataFrame of the entire audit log
get_complete_audit_log(
    event_date=event_date,
    verbose=verbose
)

# return a DataFrame with JSON-clustered columns broken up into unique columns
audit_df = get_complete_audit_log(event_date=event_date)
reframe_audit_log(
    audit_df=audit_df,                                                          # df from get_complete_audit_log()
    details_col='details',                                                      # default value
    event_col='event',                                                          # default value
    description_col='description',                                              # default value
    verbose=verbose
)
