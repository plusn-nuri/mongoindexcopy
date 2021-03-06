# MongoDB index copy

A utility to copy indexes from one database to another.

## Usage
Run the python utility and capture its output.

The utility generates a JavaScript script which can be run from the MongoDB shell `mongo`.

```bash
python mongoindexcopy.py > index_creation_script.js
```
The example above creates a file *index_creation_script.js* 

## Configuration
You can set the following:

| Setting   | Description   |
|---        |---            |
|`source_connection`| A full Mongo connection URL, including db name|
|`include_collections`| A set of collection names to include in the script|

### Source Connection
The connection string for the source database you want to copy from. Note that the database name is part of the URL. The script uses that database name and only lists collections in that database.

### Include Collections
A set of collection names to include. Using an asterisk `*` anywhere in the list will cause the script to include all collections in the database.

This is a white-list. Any collection not mentioned in this list will be skipped. Collection names are case sensitive (as are MongoDB's collection names).

_Example_: Script all collections in the database __db1__ on the server __myserver1__.

```python
source_connection = "mongodb://myserver1/db1"
include_collections = ("*")
```


