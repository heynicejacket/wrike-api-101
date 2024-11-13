![wrike-api-101](https://github.com/heynicejacket/wrike-api-101/blob/master/wrike-api-101-banner-transparent.png)

## The 101

My company onboarded Wrike in 2022, but the rollout was primarily left up to individual teams. As such, there was no uniform structure to the organization of spaces.

This had its own advantages - teams weren't forced into structures that didn't "flow" the way their clients and processes worked - but it caused complications when my department was asked to retrieve this data off the back end.

GitHub had no repos. We started, and ended, with a very basic data export, dumping the entire Wrike database into a series of tables, day after day, handling a series of byzantine, infinitely recursive crosswalks on the SQL side.

This was not acceptable - but all hours are billable, so I created my own account and built out this repo to help others like me who need to work with the Wrike API.

This, hopefully, should provide the necessary tools for both the experienced data engineer, and the novice just trying to get by, with the necessary functions to be dangerous. If I'm missing anything, please let me know by filing an issue.

## Basic implementation

Test sets TBD, in `wrike.test`

## Additional helper functions

#### wrike.core.sql.create_engine()

A one-stop shop for creating a SQLAlchemy engine for MSSQL, postgreSQL, or MySQL.

Many users will have their own constructions of this, or will simply use the basic SQLAlchemy functions to do this, but this is a helpful tool for doing the connection formatting work for you.

```
# create SQLAlchemy connection engine
engine = create_engine(
    db=db,                          # name of database
    dialect=dialect,                # 'postgres', 'mysql', or 'mssql'
    user=user,
    password=password,
    endpoint=endpoint,
    verbose=True                    # if True, prints status to terminal; for dev and debug
)
```

#### chronumbo.core.sql.db_to_df()

While many users will have their own construction of this, this is a variant on `pd.read_sql()` with built-in error handling. Given a SQLAlchemy engine and a SQL query, returns the query as a DataFrame.

```
query = """
    SELECT * FROM project_audit_trail
"""

df = db_to_df(
    query=query,
    engine=engine,
    verbose=True
)
```

#### wrike.core.sql.df_to_db()

This function utilises `df.to_sql()` to push a DataFrame to SQL, with the optional functionality of handling dtypes between DataFrames and SQL to ensure successful upload.

```
df_to_db(
    engine=engine,
    df=df,
    tbl='event_log_with_time',      # name of SQL table to upload data to
    if_tbl_exists='replace',        # as with df.to_sql()
    retrieve_dtype_from_db=True,    # if True, recasts DataFrame with SQL field types
    dtype_override=None,            # dictionary of column names and dtypes
    chunksize=10000,
    verbose=True
)
```

#### chronumbo.core.sql.get_sql_col_types()

Helper function to retrieve column types from SQL tables.

🚨 _See [Chronumbo, Issue #5](https://github.com/heynicejacket/chronumbo/issues/5); This function currently only supports postgreSQL._

```
get_sql_col_types(
    engine=engine,
    tbl=tbl,
    verbose=True
)
```
