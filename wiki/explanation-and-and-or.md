# General
The default condition for the query is `AND`, `OR` is possible
Normally the default condition is inserted when using the builder, for a better understanding examples are available

If you use `AND` `OR` several times in a row without another condition in between, the last one will always be used.

## Example
Normaly
```python
conn.table("myTable").select("name, age, email").where("age", 20).where("name", "Benjamin").where("email", "benjamin@mail.com").fetchone()
```
What it really looks like
```python
conn.table("myTable").select("name, age, email").where("age", 20).AND().where("name", "Benjamin").AND().where("email", "benjamin@mail.com").fetchone()
```
It saves you the step of repeating `AND`.
If you set the condition default to `or` you will see everywhere instead of `AND`, `OR`

```python
conn.table("myTable").select("name, age, email").default_or().where("age", 20).where("name", "Benjamin").where("email", "benjamin@mail.com").fetchone()
```
What it really looks like
```python
conn.table("myTable").select("name, age, email").default_or().where("age", 20).OR().where("name", "Benjamin").OR().where("email", "benjamin@mail.com").fetchone()
```
## Change the AND/OR condition
You can not only do everything with `and` `or`, but you can also address them separately to mix them.
### Example
```python
conn.table("myTable").select("name, age, email").where("age", 20).OR().where("age", 25).fetchone()
```
Remember, the default condition has not been changed, so normally `AND` would be used, but we override it with `OR` at this point. This is also possible the other way around if you have set `OR` by default.

## Change default AND/OR Condition
It is possible to set also between the default, this affects only new conditions

### To AND

- `default_and()`

### To OR

- `default_or()`