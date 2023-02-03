Select your data in your database

# First
To select certain columns list them in a string and separate them with a comma, to select all of them use `*` _not usable in connection with json_. <br>
This is normal SQL

## Example "All"
```python
conn.table("myTable").select("*")
```
## Example "Spefic"
```python
conn.table("myTable").select("name, age, email")
```

# Repeatable

- [all of conditions builder](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Conditions)
- [all of base join extention](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Base-Join-Extention)

- `join_select(join_table: str, column: str)` - Works like in step ["first"](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Select#first), it is only added to the existing column, but you have to specify the table of the join from which you want to select the column.
- `column_select(column: str):` - Works like in step ["first"](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Select#first), it is only added to the existing column

# Endpoints

- `fetchone()`
- `fetchall()`
- `get_sql()`

_after update 0.5.0_

- `fetchone_json()`
- `fetchall_json()`

# Example Code
```python
# fetch one
result = connection.table("myTable").select("*").fetchone()
# fetch all
result = connection.table("myTable").select("*").fetchall()

# Select specific column/s
result = connection.table("myTable").select("id").fetchall()
result = connection.table("myTable").select("id, name, age, email").fetchall()

# Select something with where
result = connection.table("myTable").select("name, age, email").where("age", 25).fetchall()
# Multiple where
result = connection.table("myTable").select("name, age, email").where("age", 25).where("name", "Helgo").fetchall()

# Use join (example)
result = connection.table("myTable").select("name").join(InnerJoinBuilder("otherTable").condition("id", "otherId")).join_select("otherTable", "note").fetchall()
```