# How its works?
The libray offers the possibility to continuously extend the SQL script by returning itself. 
With the execution this possibility is terminated. Example ends `get_sql()`, `execute()`, `fetchone()` or `fetchall()`. Endpoints are defined in the builders in the section endpoints. Repetable are defined in the section Repeatable.

### Example
```python
conn.table("myTable").select("name, age, email").where("age", 20).where("name", "Benjamin").where("email", "benjamin@mail.com").fetchone()
```

-----

# Results

## Fetch One

Fetch One returns a list with the data. The structure results from the pure sequence of the columns

### Example of the Data
```json
["Benjamin", 20, "benjamin@mail.com"]
```

## Fetch All
Fetch All returns a list with lists with the data. The structure results from the pure sequence of the columns.
Even if it contains only one result this structure is then used

### Example of the Data
```json
[
 ["Benjamin", 20, "benjamin@mail.com"],
 ["Heike", 24, "peike@mail.com"],
 ["Peter", 30, "peter@mail.com"]
]
```

-----

# Use the SQL Builder without connections
This is only a example <br> **Warning!** `execute` and `fetch` will throw errors. 

````python
from mariadb_sqlbuilder.builder import TableBuilder

table = TableBuilder(None, "myTable")  # no connection
# you can use it normal
sql: str = table.insert().set("id", 10).get_sql()

# example for run the sql in your own cursor
cursor.execute(sql)
````