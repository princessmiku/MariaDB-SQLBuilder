# Welcome to the MariaDB-SQLBuilder wiki!

### What is the MariaDB-SQLBuilder?
This library should make it easier to use SQL with Maria DB.
With the MariaDB SQLBuilder you don't have to write SQL yourself anymore. Build the script over a class and run it afterwards.

### Pre Info
The wiki is mostly translated by [DeepL](https://www.deepl.com/translator), otherwise by myself which might not always be correct.


### Importand notice
Keep in mind that as long as a script is executed, one connection is occupied. 
So always consider how many connections you need at startup, changing them later 
is not possible. Connections are only used during an execute/fetch and then released 
again, this process usually does not take long. Other execute/fetch will wait.

More about Cursor *coming soon*

