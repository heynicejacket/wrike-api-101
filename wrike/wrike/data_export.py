import io
import pandas as pd

from wrike.core.api import (
    wrike_get
)

from wrike.core.constants import (
    WRIKE_BASE_URL,
    WRIKE_DATA_URL
)


def data_export_to_csv(data_export_dict, output_dir, tbl_prefix='', verbose=False):
    """
    Given a Wrike data export CSV URL dictionary, this function downloads data from Wrike API URLs provided in
    data_export_dict and saves data as CSV files.

    Wrike dict should appear as follows:

        {
            'attachment_file': 'https://storage.www.wrike.com/data_export/resource/123456789?accountId=12345',
            'audit_log': 'https://storage.www.wrike.com/data_export/resource/123456789?accountId=12345',
            ...
        }

    For each dataset in data_export_dict, this function sends a request to the corresponding URL, reads the data into
    a pandas DataFrame, and saves it as a CSV file. The CSV file name is derived from the keys in data_export_dict
    and can have an optional prefix.

    For export, given the following parameters:

        output_dir=f'C:/localtemp/'
        tbl_prefix='wrike'

    Export string is as follows:

        'C:/localtemp/wrike_attachment_file.csv'
        'C:/localtemp/wrike_audit_log.csv'
        ...

    Note: Wrike takes some time to return the full tables.

    :param data_export_dict:    dict, required          dict containing resource names as keys and URLs as values
    :param output_dir:          str, required           path where CSV files will be saved
    :param tbl_prefix:          str, optional           if provided, prefix for CSV file names
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    None
    """

    for name, url in data_export_dict.items():
        response = wrike_get(url=url)
        df = pd.read_csv(io.BytesIO(response.content))

        csv_file_path = f'{output_dir}{tbl_prefix}{name}.csv'

        df.to_csv(csv_file_path, index=False)
        print(f'Success: data saved to {csv_file_path}') if verbose else None


def data_export_to_sql(data_export_dict, engine, if_exists, tbl_prefix='', verbose=False):
    """
    Given a Wrike data export CSV URL dictionary and SQLAlchemy connection engine, sends data from Wrike API URLs
    provided in data_export_dict to a SQL database.

    Wrike dict should appear as follows:

        {
            'attachment_file': 'https://storage.www.wrike.com/data_export/resource/123456789?accountId=12345',
            'audit_log': 'https://storage.www.wrike.com/data_export/resource/123456789?accountId=12345',
            ...
        }

    For each dataset in data_export_dict, this function sends a request to the corresponding URL, reads the data into
    a pandas DataFrame, and writes data to the SQL database using the specified engine.

    Connection failures and retries are handled to limit likelihood of failed push to SQL. The table name is derived
    from keys in data_export_dict and can have an optional prefix.

    Note: Wrike takes some time to return the full tables.

    :param data_export_dict:    dict, required          dict containing dataset name and data URL
    :param engine:              object, required        sqlalchemy.engine.Engine
    :param if_exists:           str, required           pd.to_sql() handling for existing table; ‘fail’, ‘replace’, ‘append’
    :param tbl_prefix:          str, optional           if provided, prefix for sql table
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    None
    """

    for name, url in data_export_dict.items():
        response = wrike_get(url=url, verbose=verbose)
        df = pd.read_csv(io.BytesIO(response.content))

        tbl_name = f'{tbl_prefix}{name}'

        fail = True
        while fail:
            try:
                conn = engine.connect()
                df.to_sql(name=tbl_name, con=engine, index=False, if_exists=if_exists, chunksize=10000)
                print('Success: df.to_sql() successfully sent data to {}'.format(tbl_name)) if verbose else None
                fail = False
                conn.close()

            except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError) as e:
                print('{}. Trying again to connect.'.format(e)) if verbose else None
                continue


def get_data_export_urls(filtered_list=None, verbose=False):
    """
    Retrieves URLs for data exports from Wrike's API, which include resources like tasks, folders, comments, and other
    entities. This function retrieves all available data export URLs and optionally filters them based on a provided
    list.

    The request is sent to the data export endpoint, and a dict is constructed with the resource names as keys and
    their corresponding URLs as values. If no 'filtered_list' provided, the entire dictionary of resources and  URLs
    is returned. If 'filtered_list' provided, only the resources whose names match the entries in the list will be
    returned.

    Optional parameters to pass into this function as follows:

        filtered_list=['user', 'work_item']
        verbose=True

    Returned API response in dictionary format:

        {
            'attachment_file': 'https://storage.www.wrike.com/data_export/resource/123456789?accountId=12345',
            'audit_log': 'https://storage.www.wrike.com/data_export/resource/123456789?accountId=12345',
            ...
        }

    :param filtered_list:       list, optional          list of resource names to filter returned export URLs
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    dict                    resource names dict and corresponding export URLs
    """

    data_export_url = WRIKE_BASE_URL + WRIKE_DATA_URL
    data_export_resources = wrike_get(url=data_export_url, return_all=False, verbose=verbose)[0]['resources']
    data_export_dict = {resource['name']: resource['url'] for resource in data_export_resources}

    if filtered_list is None:
        return data_export_dict
    else:
        return {key: value for key, value in data_export_dict.items() if key in filtered_list}
