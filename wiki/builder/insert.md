Insert data into the database

# First
## Example
```python
conn.table("myTable").insert()
```

# Repeatable

- `set(column: str, value: Union[str, int, None])` - set the data of a specific column
- `ignore()` - insiert or ignore
- `tableSet(self, table: str, column: str, value: Union[str, int, None])` - set data in another table
- `addJoinTable(self, table: str)` - only requierd if you use set json and want to set it in a other table.
- `set_json(self, json: Dict[str, any], pop: List[str] = None)` - set data with a json

# Endpoints

- `execute()`
- `get_sql()`

# Example Code
```python
# normal insert
connection.table("myTable").insert().set("id", 10).set("age", 25).set("Name", "Helgo").execute()
# insert ignore
connection.table("myTable").insert().set("id", 10).ignore().execute()
```