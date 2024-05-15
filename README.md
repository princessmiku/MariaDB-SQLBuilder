# MariaDB SQL Builder

-----

[![License - GNU LPGL version 2.1](https://img.shields.io/badge/License-GNU_LPGL_version_2.1-green)](https://opensource.org/licenses/LGPL-2.1)
[![Python - ^3.7](https://img.shields.io/badge/Python-^3.7-blue)](https://www.python.org/)
[![Downloads](https://pepy.tech/badge/mariadb-sqlbuilder)](https://pepy.tech/project/mariadb-sqlbuilder)

## Security fix 1.1

If you are interested, the content is below

### MariaDB license

This library uses MariaDB Connector/Python, which is released under the terms of the GPLv2 license. For more 
information, please see the [license file in the repository](https://github.com/mariadb-corporation/mariadb-connector-python/blob/1.1/LICENSE).


# [Install](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Installation)
Install the package with pip
``pip install mariadb-sqlbuilder``

Installation with pip + github
``pip install git+https://github.com/princessmiku/MariaDB-SQLBuilder``

# [Setup](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Setup)

````python
import mariadb_sqlbuilder

connection = mariadb_sqlbuilder.Connector(
    host="HostIP/URL",
    user="User",
    password="Password",
    database="DatabaseToConnect"
)
````

# Example Functions
### Select
```python
result = connection.table("myTable").select("name, age, email").where("age", 25).fetchall()
```

### Insert
```python
connection.table("myTable").insert().set("id", 10).set("age", 25).set("Name", "Helgo").execute()
```

# [Wiki](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki)
For all Details and how to use

## Functions

- **[Select](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Select)**
- **[Insert](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Insert)**
- **[Update](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Update)**
- **[Upsert](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Upsert)**
- **[Delete](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Builder---Delete)**
- **[CustomSQL](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Custom-SQL)**


## Content of the fix

I have found a security problem. Variables should be given directly
to the cursor instead of writing them to the SQL. This prevents SQL injections.

By changing the avoidance of sql injection, the function “get_sql()” now returns “?”
at the points where variables were before.

To get the variables back, there is now “values_for_execute”, which contains the variables in the correct order.
The variables are returned in the type as they are stored. 
String as string, integer as integer, datetime as datetime...

**Example**

- ``conn.table().update().values_for_execute``
- ``conn.table().select().values_for_execute``

The variables are used in the statements where I suspect the possibility of SQL injection.

- Setting variables
- Where to query (conditions)

Setting keys or table names, for example, is normally not something a user should do, 
so they are written to SQL as normal.

I learned a lot while working on other projects. 
This has given me some knowledge about security. 
So I thought it was right to apply this to old projects as well.

----------------------------------------------------------------

<br>
Not completely used but <br>
Translated with www.DeepL.com/Translator (free version)
