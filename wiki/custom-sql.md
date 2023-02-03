# Example
````python
from mariadb_sqlbuilder import Connect

connection: Connect = Connect(...)

# execute your own SQL, without receiving
result = connection.execute("YourSQL")

# execute your own SQL, with receiving
result = connection.execute_fetchone("YourSQL") # return with fetchOne
result = connection.execute_fetchall("YourSQL") # return with fetchMany

# execute more than one SQL Statement
result = connection.execute_script("YourSQLScript")
````