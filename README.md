# SAP Hana Connector

## Commands

All commands require passing in the SAP Hana connection string:

```
database_connection_str: str
```

Which is passed directly to `hdbcli.dbapi`. eg: `user=SYSTEM password=password address=localhost port=30015`

All commands except for `DoSQL` require `table_name: str` as well.

### InsertValues

Additional parameters:

```
schema: Dict[str, Any]
```

Inserts values into a table with the provided column names and their values. Multiple records can be inserted per call.

The schema parameter expects:

| Key | Value |
|-----|-------|
| `columns` | A list of column names |
| `values` | A list of lists of the values to insert. Order must match column order. |

As an example, to insert the following data:

```
dev=# select * from states;
 country |  state   | abbrev | somenum 
---------+----------+--------+---------
 USA     | Georgia  | GA     |      33
 USA     | Virginia | VA     |      55
(2 rows)

```

The schema passed to the connector would be:

```
{
  "columns": [
    "country",
    "state",
    "abbrev",
    "somenum"
  ], 
  "values": [
    ["USA", "Georgia", "GA", 33], 
    ["USA", "Virginia", "VA", 55]
  ]
}
```
### SelectValues

Additional parameters:

```
schema: Dict[str, Any]
```

Selects values from a table with the provided column names and optional where clause.

The schema parameter expects:

| Key | Value |
|-----|-------|
| `columns` | A list of column names |
| `where` | (optional) A list of lists of the column names, operator and values to filter the select. |

Operators supported for where clauses are: `=, !=, <, >`

As an example, to mimic the following select:

```
dev=# select * from states;
 country |  state   | abbrev | somenum 
---------+----------+--------+---------
 USA     | Georgia  | GA     |      33
 USA     | Virginia | VA     |      55
(2 rows)

```

The schema passed to the connector would be:

```
{
  "columns": [
    "country",
    "state",
    "abbrev",
    "somenum"
  ]
}
```

To mimic the following select:

```
dev=# select * from states where somenum = 33;
 country |  state   | abbrev | somenum 
---------+----------+--------+---------
 USA     | Georgia  | GA     |      33
(2 rows)

```

The schema passed to the connector would be:

```
{
  "columns": [
    "country",
    "state",
    "abbrev",
    "somenum"
  ],
  "where": [
    ["somenum", "=", 33]
  ]
}
```

### UpdateValues

Additional parameters:

```
schema: Dict[str, Any]
```

Updates columns a table with the provided value and optional where clause. The where clause is specified, and works, the same as described in `SelectValues`.

The schema expcets a `set` key with a value that is a dictionary. The keys in this dictionary are the column names and the values are the new value to set. 

For example:

```
{
  "set": {
    "abbrev": "ZZ"
  }, 
  "where": [
    ["abbrev", "=", "VA"]
  ]
}
```

### DoSQL

Additional parameters:

```
schema: Dict[str, Any]
```

Performs a SQL statement of your chosing.

The schema parameter expects:

| Key | Value |
|-----|-------|
| `sql` | The SQL to `do`. Uses `%s` for variable bindings. |
| `values` | (optional) A list of values to bind. |
| `fetch_results` | (options) Bool to indicate if a list of results should be returned. |

