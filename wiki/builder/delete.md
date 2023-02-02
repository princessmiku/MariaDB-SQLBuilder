Delete data from the database

# First
## Example
```python
conn.table("myTable").delete()
```

# Repeatable
- [all of conditions builder](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Conditions)
- imSureImNotUseConditions(True) - security so that you do not unknowingly delete everything, default is the `True` `False` therefore you must specify this extra

# Endpoints
- `execute()`
- `get_sql()`

# Example Code
```python
# delete with where
connection.table("myTable").delete().where("id", 10).execute()

# delete without where is not possible on this way, it wil throws an error
connection.table("myTable").delete().execute()
# if you really want to delete all data in a table use this way
# the true is important, otherwise it will also throw an error
connection.table("myTable").delete().imSureImNotUseWhere(True).execute()
# but you can still get the sql this way
connection.table("myTable").delete().get_sql()
```