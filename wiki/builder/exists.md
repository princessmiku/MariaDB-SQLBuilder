Check if a table, a column or specific rows exists


# Repeatable

- [all of conditions builder](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Conditions)
- ```column(column: str)``` - name of a column
- ```columns(columns: str)``` - column names seperated with a comma

# Table Check

A table check can't combine with conditions 

```result = conn.table("user").exists().check_exists()```

# Column

Check if a column or more columns exists

```result = conn.table("user").exists().column("id").check_exists()```

```result = conn.table("user").exists().columns("id, username").check_exists()```

# Row

Check if a row exists or more

```result = conn.table("user").exitsts().where("id", 1).check_exitsts()```

```result = conn.table("user").exitsts().where("id", 1).OR().where("username", "Bob").check_exitsts()```

# Endpoints

- `get_sql()`
- ``check_exists()`` - return a bool only
