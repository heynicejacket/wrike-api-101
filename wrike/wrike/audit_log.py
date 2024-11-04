import json
import pandas as pd

from wrike.core.api import (
    wrike_get
)

from wrike.core.constants import (
    WRIKE_AUDIT_URL,
    WRIKE_BASE_URL
)

from wrike.core.toolkit import (
    get_ordinal_suffix,
    the_time_keeper
)


def get_audit_log(event_start=None, event_end=None, operations=None, page_size=None, next_page_token=None, verbose=False):
    """
    Returns audit log reports from Wrike API.

    This function retrieves audit trail of actions performed in Wrike. This function can only be successfully called by
    an API token created by Enterprise Admins with the 'Create user activity reports' right. If user has insufficient
    permissions, _wrike_get() will return a 403 error.

    The parameter 'operations' defines which events are called from the Wrike audit log. The full list of operations
    can be found here: https://developers.wrike.com/api/v4/audit-log/

    Can be executed as follows:

        get_wrike_audit_log(
            event_start='2023-02-01T07:51:44Z',
            operations=['TaskCreated', 'InvitationSend'],
            page_size=2
        )

    Returns as follows:

        {
            'kind': 'auditLog',
            'nextPageToken': 'AACTACY3YYQAAAXEM3ZC',
            'responseSize': 100000,
            'data': [
                {
                    'id': 'IEBCC46DA4E55',
                    'operation': 'TaskCreated',
                    'userId': 'UDWKFOAG',
                    'userEmail': 'matthew@nicejacket.cc',
                    'eventDate': '2023-10-17T22:55:51Z',
                    'ipAddress': '44.255.128.242',
                    'objectType': 'Task',
                    'objectName': 'Order released',
                    'objectId': 'IEBCC46DA4E55',
                    'details': {
                        'Now Shared With Users': '',
                        'Now Shared With Teams': '',
                        'Parent Folders': 'https://www.wrike.com/open.htm?id=1337275616',
                        'Work Item Link': 'https://www.wrike.com/open.htm?id=1368492816',
                        'Work Item Type': 'Task'
                    }
                },
                ...
            ]
        }

    :param event_start:         str, optional           event filter start date (e.g. yyyy-MM-dd'T'HH:mm:ss'Z')
    :param event_end:           str, optional           event filter end date (e.g. yyyy-MM-dd'T'HH:mm:ss'Z')
    :param operations:          list, optional          list of operations to filter log (e.g. ['Oauth2AccessGranted', 'InvitationSend'])
    :param page_size:           int, optional           number of records per page to fetch
    :param next_page_token:     str, optional           token to fetch the next page of results, if paginated
    :param verbose:             bool, optional          if True, print status to terminal
    :return:
    """

    audit_log_url = WRIKE_BASE_URL + WRIKE_AUDIT_URL

    params = {}

    if event_start or event_end:
        params['eventDate'] = {}
        if event_start:
            params['eventDate']['start'] = event_start
        if event_end:
            params['eventDate']['end'] = event_end
    if operations:
        params['operations'] = operations
    if page_size:
        params['pageSize'] = page_size
    if next_page_token:
        params['nextPageToken'] = next_page_token

    return wrike_get(url=audit_log_url, return_all=False, verbose=verbose)


def get_audit_log_subset(next_page_token=None, event_date=None, operations=None, page_size=100, verbose=False):
    """
    Pulls a subset of Wrike audit log based on nextPageToken.

    :param next_page_token:
    :param event_date:
    :param operations:
    :param page_size:
    :param verbose:             bool, optional          if True, print status to terminal
    :return:
    """
    url = WRIKE_BASE_URL + WRIKE_AUDIT_URL
    print(url) if verbose else None

    params = {
        "pageSize": page_size,
    }

    if next_page_token:
        params['nextPageToken'] = next_page_token
    else:
        if event_date:
            event_date_json = json.dumps(event_date)                            # Wrike requires URL-encoded event_date
            params['eventDate'] = event_date_json
        if operations:
            params['operations'] = operations

    response = wrike_get(url=url, return_response=True, params=params, verbose=verbose)

    if response.status_code == 401:
        print('Authentication failed: Invalid API token.')
        return None, None

    if response.status_code == 400:
        print(f'Bad request: {response.json()}')
        return None, None

    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        return None, None

    data = response.json().get('data', [])
    next_token = response.json().get('nextPageToken', None)

    df = pd.DataFrame(data)

    return df, next_token


def get_complete_audit_log(event_date=None, operations=None, page_size=100, max_iterations=None, reframe=False,
                           verbose=False):
    """
    Fetches entire audit log by repeatedly calling _get_audit_log_subset() function and concatenating results as a
    pandas DataFrame.

    By default, returns a DataFrame with the following fields:

        ['id', 'operation', 'userId', 'userEmail', 'eventDate', 'ipAddress', 'objectType', 'objectName', 'objectId', 'details']

    The field 'details' is by default a dict, which appears as follows:

        {'Prev Status': 'New', 'New Status': 'Completed', 'Work Item Link': 'https://www.wrike.com/open.htm?id=5992019'}

    If reframe_audit_log=True,

    :param event_date:          dict, optional          dict with 'start' and 'end' for date range (semi-open interval)
    :param operations:          list, optional          list of operations to filter
    :param page_size:           int, optional           number of results to retrieve per page (default 100)
    :param max_iterations:      int, optional           maximum number of iterations (pages) to retrieve
    :param reframe:             bool, optional
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    df                      full audit log as a DataFrame
    """

    complete_audit_log = pd.DataFrame()
    next_page_token = None

    duration = the_time_keeper()
    i = 0

    while True:
        subset, next_page_token = get_audit_log_subset(next_page_token, event_date, operations, page_size, verbose)
        print(f'Retrieved {len(subset)} row(s) in {i}{get_ordinal_suffix(i)} subset of audit log.') if verbose else None

        if subset is None:
            print('Error encountered. Stopping the log retrieval.') if verbose else None
            break

        complete_audit_log = pd.concat(objs=[complete_audit_log, subset], ignore_index=True)

        if not next_page_token:
            break                                                               # exit loop when no more pages

        i += 1

        if max_iterations is not None and i >= max_iterations:
            print(f"Reached maximum iteration limit: {max_iterations}. Stopping retrieval.") if verbose else None
            break                                                               # exit loop at max_iterations

    if reframe:
        complete_audit_log = reframe_audit_log(audit_df=complete_audit_log, verbose=verbose)

    the_time_keeper(duration)

    return complete_audit_log


def reframe_audit_log(audit_df, details_col='details', event_col='event', description_col='description', verbose=False):
    """
    Transforms a dataframe by exploding a dictionary column into multiple rows.

    For each key-value pair in the specified 'details' column, this function creates a new row with the key placed in
    'event' column, and the value in the 'description' column. Other columns remain the same for each expanded row.

    :param audit_df:            df, required            DataFrame with a column containing dicts
    :param details_col:         str, optional           column name containing dict to explode
    :param event_col:           str, optional           name of new column for dict keys
    :param description_col:     str, optional           name of new column for dict values
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                                            transformed dataframe with exploded dictionary values
    """

    df = audit_df[audit_df[details_col].apply(lambda x: isinstance(x, dict))]   # ensure 'details' col contains dicts

    exploded_df = df.apply(                                                     # explode dict into separate rows
        lambda row: pd.DataFrame(
            {
                **{col: row[col] for col in df.columns if col != details_col},
                event_col: row[details_col].keys(),
                description_col: row[details_col].values()
            }
        ),
        axis=1
    ).reset_index(drop=True)

    return pd.concat(exploded_df.tolist(), ignore_index=True)                   # concat all exploded rows into one df
