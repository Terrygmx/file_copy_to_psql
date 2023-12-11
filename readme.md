# description
This application is to copy file into corresponding postgres table daily and update the date index table(some file might need extra operation, like add a new "date_of_file" column). The date index table tells you what date is the latest date for a table, so the data loading application shall access the corresponding data of the table.
Because the copy action and the update action must be done in one row, they are implemented with transaction.

## usage
call the file_handler.py by giving a table configuration file and where the data files are located
```python
    python3 py/file_handler.py conf/table_mappings.csv /data/CP2/ftp/af/
```

# file list

## conf/logger_config.json
configuration of the logger

## conf/table_mappings.csv
details of the table mapping configuration, like which file refers to which table, and what the file definition is, etc.

## py/logger.py
used to create log generator, specially a function for decorator is added.

## py/file_handler.py
the entrance of the application, which calls other python functions. It will do: initialize the logger, parse the configuration, manipulate the data file and copy files into the database tables.

## py/file_name_parser.py
parse the table_mappings.csv file

## py/cycle_date_addup.py
to add a new "date_of_file" column into data files(if configured in the table_mappings)

## py/psql_copy.py
copy the data file into postgres and update the date index table, using transaction to keep consistency.
