Select your data in your database

# First

In the example we will only look at the simplest method of 
expressions and that is the column in a string. 
For understanding the deeper possibilities of sql we 
recommend you to read its documentation.

- [Arithmetic Documentation](https://mariadb.com/kb/en/arithmetic-operators/)

### Available Expressions
- Column
- Arithmetic


## Possible handover of variables
All listed transfer options are also available in the join column. 
It is only to note that the table comes first

### In a string
This is the example and the simplest, here we only work with column, 
for deeper sql functions it needs the intigrated sqlbuilder functions

````python
.select("name, age, email")
````

### With a list
All expressions listed above are available here

````python
.select(["name", "age", "email"])
````
````python
.select(["name", Arithmetic(...)])
````

### With args
All expressions listed above are available here
````python
.select("name", "age", Arithmetic(...))
````

### Combine Str/List with args
It is also possible to combine a str or a list with the args
````python
.select("name, age", Arithmetic(...))
````
````python
.select(["name", "age"], Arithmetic(...))
````


## Example "All" select
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

- `join_select(join_table: str, expression)` - Works like in step ["first"](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Select#first), it is only added to the existing column, but you have to specify the table of the join from which you want to select the column.
- `column_select(expression):` - Works like in step ["first"](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Select#first), it is only added to the existing column

# Endpoints

- `fetchone()`
- `fetchall()`
- `get_sql()`
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