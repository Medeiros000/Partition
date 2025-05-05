# Partition Project

This project provides tools and scripts for managing database partitions, extracting table definitions, and executing regression analyses on data files.

## Features

- **Database Connection and Management**:  
  Utilities for connecting to and managing databases, located in the database folder.

- **Partition Script Generation**:  
  Automatically generates SQL scripts for creating partitions, with outputs saved in the files directory.

- **Table Definition Extraction**:  
  Extracts table definitions using SQL scripts found in the sql folder.

- **Regression Analysis**:  
  Performs simple and complete regression analyses on datasets, with results saved as CSV files in the files directory.

- **Utility Functions**:  
  Helper modules for printing and note-taking, available in the utils folder.

## Usage

1. Configure your database connection in the `.env` file.
2. Run the main script (`main.py`) to execute the desired operations.
3. Generated files and results will be saved in the files directory.
4. 
The default configuration is `PostgreSQL` but you should change it to use with another database

## Requirements

- Python 3.11 or higher
- Run sql file `sql\pg_get_tabledef.sql`
- Required packages (see your `requirements.txt` if available)

## Folder Structure

- database - Database connection and management scripts
- files - Generated SQL, CSV, and text files
- sql - SQL scripts for table definition extraction
- utils - Utility modules for printing and notes

## License

This project is licensed under the MIT License


## Third-Party Content

The SQL script `sql/pg_get_tabledef.sql` was sourced from [[MichaelDBA](https://github.com/MichaelDBA/pg_get_tabledef)].  
Please refer to the original license included in that repository.  

---
