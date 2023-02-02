### You can use JSON and you can get data as Json

It is recommended if you request data from the database and want to insert it again in a modified form.

**Note that when you insert a JSON into the database, all columns must be present. Otherwise there will be an error.**

Note that with joins you have to specify the joins again with an insert. Otherwise it will try to write the data into a column in the table with the data.