In mariadb_sqlbuilder.helpful.connection_dummy you can find a dummy connection, 
it does not need a connection to a database.


You can use it just like the normal one, except that it has no direct database functions.

The only available function is currently ``.table()`` what you need to use the library's purpose
