With the module you can easily write conditions in advance and then use them in different builders.

The module works only in all modules where there are conditions too


## Setup

``ConditionsSaver(table_name)``

# Repeatable Functions

- [all of conditions builder](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Conditions)


## Using
You simply specify this class when selecting the action, see in example usage.

It is important that you pass it with ``condition=``.

## Example Usage

### Select
````python
saver = ConditionsSaver("user")
saver.where("id", 19)
conn.table(user).select("*", condition=saver).fetch_one()
````

### Delete
````python
saver = ConditionsSaver("user")
saver.where("id", 25)
conn.table(user).delete(condition=saver).execute()
````


