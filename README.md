# MariaDB SQL Builder

-----

[![License - GNU LPGL version 2.1](https://img.shields.io/badge/License-GNU_LPGL_version_2.1-green)](https://opensource.org/licenses/LGPL-2.1)
[![Python - ^3.7](https://img.shields.io/badge/Python-^3.7-blue)](https://www.python.org/)
[![Downloads](https://pepy.tech/badge/mariadb-sqlbuilder)](https://pepy.tech/project/mariadb-sqlbuilder)

## Warning! Update 1.0 change many functions and variable names to the pep8 standard

Too lazy to write SQL? Then use the SQL Builder to make your life easier!

MariaDB SQL Builder is a simple way to use SQL.
Use your own SQL or use the integrated SQL Builder tool.

# [Install](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Installation)
Install the package with pip
``pip install mariadb-sqlbuilder``

Installation with pip + github
``pip install git+https://github.com/princessmiku/MariaDB-SQLBuilder``

# [Setup](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Setup)
````python
import mariadb_sqlbuilder

connection = mariadb_sqlbuilder.Connect(
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


----------------------------------------------------------------

<br>
Not completely used but <br>
Translated with www.DeepL.com/Translator (free version)
