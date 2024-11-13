ACCESS_TOKEN_WRIKE = 'your api key'                         # Wrike api key

API_HEADER_UPLOAD_WRIKE = {                                 # header for attachment upload requests
    'Authorization': 'bearer ' + ACCESS_TOKEN_WRIKE
}

API_HEADER_WRIKE = {                                        # header for general requests
    'Authorization': 'bearer ' + ACCESS_TOKEN_WRIKE,
    'Content-Type': 'application/json',
    'cache-control': 'no-cache',
}

API_PREFIX_URL_WRIKE = 'https://www.wrike.com/api/v4/'      # base Wrike api URL for requests

DTYPE_MAPPING = {
    # integer types
    'integer': 'int64',
    'bigint': 'int64',
    'smallint': 'int64',
    'tinyint': 'int8',
    'mediumint': 'int32',

    # unsigned integer types, treated as signed in pandas
    'unsigned big int': 'uint64',
    'unsigned int': 'uint32',
    'unsigned smallint': 'uint16',
    'unsigned tinyint': 'uint8',

    # floating-point types
    'decimal': 'float64',
    'numeric': 'float64',
    'real': 'float64',
    'float': 'float64',
    'double precision': 'float64',

    # date and time types
    'date': 'datetime64[ns]',
    'datetime': 'datetime64[ns]',
    'timestamp': 'datetime64[ns]',
    'time': 'datetime64[ns]',                               # pandas lacks time-only dtype; can be stored as datetime
    'year': 'datetime64[ns]',                               # pandas lacks year dtype; can be stored as datetime

    # char types
    'char': 'object',
    'varchar': 'object',
    'text': 'object',
    'mediumtext': 'object',
    'longtext': 'object',
    'tinytext': 'object',

    # binary data types
    'binary': 'object',                                     # pandas lacks binary natively; can be stored as object
    'varbinary': 'object',
    'blob': 'object',
    'mediumblob': 'object',
    'longblob': 'object',
    'tinyblob': 'object',

    # boolean types
    'boolean': 'bool',
    'bool': 'bool',

    # JSON data types
    'json': 'object',
    'jsonb': 'object',                                      # postgreSQL JSON binary

    # geospatial types
    'geometry': 'object',
    'geography': 'object',
    'point': 'object',
    'linestring': 'object',
    'polygon': 'object',

    # enumerated types
    'enum': 'object',

    # UUID types
    'uuid': 'object',

    # array types
    'array': 'object',

    # interval types
    'interval': 'timedelta64[ns]',

    # specialized types
    'money': 'float64',                                     # money can be treated as float or custom object
    'serial': 'int64',                                      # auto-incrementing integer
    'bigserial': 'int64',

    # bit types
    'bit': 'object',
    'bit varying': 'object',
}

WRIKE_BASE_URL = 'https://www.wrike.com/api/v4/'

WRIKE_ACCESS_ROLES_URL = 'access_roles/'
WRIKE_ATTACHMENTS_URL = 'attachments/'
WRIKE_AUDIT_URL = 'audit_log/'
WRIKE_COMMENTS_URL = 'comments/'
WRIKE_CONTACTS_URL = 'contacts/'
WRIKE_CREATE_FOLDER_URL = 'folders/{0}/folders/'
WRIKE_CUSTOM_STATUS_URL = 'customstatuses/'
WRIKE_DATA_URL = 'data_export/'
WRIKE_DOWNLOAD_URL = 'url/'
WRIKE_FOLDER_URL = 'folders/'
WRIKE_SPACE_URL = 'spaces/'
WRIKE_TASK_URL = 'tasks/'
WRIKE_UPDATE_OR_DELETE_FOLDER_URL = 'folders/{0}'
WRIKE_USER_TYPES_URL = 'user_types/'
WRIKE_USER_URL = 'users/'
WRIKE_WORKFLOWS_URL = 'workflows/'
