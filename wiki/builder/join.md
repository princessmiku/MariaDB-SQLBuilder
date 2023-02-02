All general information about what the joins do can be found on the [official site](https://mariadb.com/kb/en/joining-tables-with-join-clauses/)

# Conditionless Join Builder
## CrossJoinBuilder
### Example
```python
from mariadb_sqlbuilder.builder.joinBuilder import CrossJoinBuilder
conn.table("myTable").select("*").join(CrossJoinBuilder("otherTable")).joinSelect("otherTable", "*").fetchall()
```

# Condition Join Builder
Currently is only AND possible for multiplie conditions.

In the condition you first specify a column from the main table, then a column from the join table 
### Example
`.condition("val1", "otherVal1")`


## InnerJoinBuilder
### Example
```python
from mariadb_sqlbuilder.builder.joinBuilder import InnerJoinBuilder
conn.table("myTable").select("*").join(InnerJoinBuilder("otherTable").condition("my", "other")).joinSelect("otherTable", "*").fetchall()
```
## LeftJoinBuilder
### Example
```python
from mariadb_sqlbuilder.builder.joinBuilder import LeftJoinBuilder
conn.table("myTable").select("*").join(LeftJoinBuilder("otherTable").condition("my", "other")).joinSelect("otherTable", "*").fetchall()
```
## RightJoinBuilder
### Example
```python
from mariadb_sqlbuilder.builder.joinBuilder import RightJoinBuilder
conn.table("myTable").select("*").join(RightJoinBuilder("otherTable").condition("my", "other")).joinSelect("otherTable", "*").fetchall()
```
