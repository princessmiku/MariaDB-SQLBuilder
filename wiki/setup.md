First Step install it -> [click me](https://github.com/princessmiku/MariaDB-SQLBuilder/wiki/Installation)

# Code
````python
import mariadb_sqlbuilder

connection = mariadb_sqlbuilder.Connect(
    host="HostIP/URL",
    user="User",
    password="Password",
    database="DatabaseToConnect",
    port=3306,  # not required
    pool_name='mypool',  # not required
    pool_size=3,  # not required
    pool_reset_connection=False # not required
    
)
````

## Infos about the connection pool
With `pool_size` you can set how many connections the library should make (default 3). 
Multiple connections allow multiple simultaneous queries. But more connections need more performance

## Infos about commit
The connection will always automatically run commit!