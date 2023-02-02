Update data in the Database

# First
## Example
```python
connection.table("myTable").update()
```

# Repeatable
- [all of conditions builder](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Conditions)
- [all of base join extention](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Base-Join-Extention)
- `set(column: str, value: Union[str, int, None])` - set the data of a specific column
- `joinSet(joinTable: str, joinColumn: str, value: [Union[str, int, None]])` - set the data of a specific column of a join table, but you have to specify the table of the join from which you want to set the column.
- `imSureImNotUseConditions(True)` - security so that you do not unknowingly overwrite everything, default is the `True` `False` therefore you must specify this extra
- `set_json(self, json: Dict[str, any], pop: List[str] = None)` - set data with a valid json, witch you can example get it with a select. Sub dict will default insert as a join, so do not forget when it is time to set a join builder. `Pop`- pop keys from the json, if you have joins in select that not should insert in a table.

# Endpoints

- `execute()`
- `get_sql()`

# Example Code
```python
# update all
connection.table("myTable").update().set("age", 25).execute()
# update multiple
connection.table("myTable").update().set("age", 25).set("name", "Helgo").execute()

# update with where statements
connection.table("myTable").update().set("age", 25).where("id", 10).execute()

# update with join

connection.table("myTable").update().set("age", 26).join(InnerJoinBuilder("otherTable").condition("id", "otherId")).joinSet("otherTable", "note", "Birthday today").execute()

```