What is Upsert? Upsert is an Insert with Update when a key is duplicated

# First

### Excepted Types in set
- String
- Integer
- Arithmetic


## Example
```python
connection.table("myTable").upsert()
```

# Repeatable

- [all of conditions builder](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Conditions)
- `set(column: str, value)` - set the data of a specific column
- `table_set(self, table: str, column: str, value)` - set data in another table
- `add_join_table(self, table: str)` - only requierd if you use set json and want to set it in a other table.
- `set_json(self, json: Dict[str, any], pop: List[str] = None)` - set data with a json

# Endpoints

- `execute()`
- `get_sql()`

# Example Code
```python
# upsert
connection.table("myTable").upsert().set("id", 10).set("name", "Helgo").execute()
# this will update the row before
connection.table("myTable").upsert().set("id", 10).set("name", "Helgo the Hero").execute()
```