Delete data from the database

# First
## Example
```python
conn.table("myTable").delete()
```

# Repeatable
- [all of conditions builder](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Conditions)
- im_sure_im_not_use_conditions() - security so that you do not unknowingly delete everything
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
connection.table("myTable").delete().im_sure_im_not_use_conditions().execute()
# but you can still get the sql this way
connection.table("myTable").delete().get_sql()
```