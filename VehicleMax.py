# --------------------------------------------------------------------------------------------------- #
# IMPORT PSYCOPG2 TO CONNECT TO DB USING SCRIPT

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()           
hostname= 'vehiclemax-1.c1yiowcm4goo.us-east-2.rds.amazonaws.com'
database= 'postgres'
username= 'VehicleMax'
pwd = 'Keilacodingspace0033?'
port_id = 5432
conn= None

# --------------------------------------------------------------------------------------------------- #
# TRY CONNECTION AND CURSOR TO NAVIGATE DATABASE
try:
    print("Trying connection...")
    conn = psycopg2.connect(
        host='vehiclemax-1.c1yiowcm4goo.us-east-2.rds.amazonaws.com',
        dbname= 'postgres',
        user= 'VehicleMax',
        password= 'Keilacodingspace0033?',
        port= 5432
    )
    print("Connection successful")

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print("Cursor created")

    cur.execute('DROP TABLE IF EXISTS employees')
    print("Table dropped")

    create_employees_script = '''CREATE TABLE IF NOT EXISTS employees(
                                    employees_id int PRIMARY KEY,
                                    employees_name varchar,
                                    favorite_color varchar
                                )'''
    cur.execute(create_employees_script)
    print("Table created")

    insert_employees_script = '''INSERT INTO employees(
                                        employees_id,
                                        employees_name,
                                        favorite_color)
                                        VALUES (%s, %s, %s)'''
    insert_employees_value = (1, "Christopher Niles", "blue")
    cur.execute(insert_employees_script, insert_employees_value)
    print("Insert complete")

    conn.commit()
    cur.close()
except Exception as error:
    print("ERROR:", error)
finally:
    if conn:
        conn.close()
# This code connects to a PostgreSQL database using the psycopg2 library and prints the version of the database.
# It uses the dotenv library to load environment variables from a .env file, which contains the database connection details.
# Make sure to create a .env file with the following content:
# DB_HOST=your_host
# DB_PORT=your_port
# DB_NAME=your_database_name
# DB_USER=your_username
# DB_PASSWORD=your_password
# This code is useful for testing the connection to the database and ensuring that the psycopg2 library is working correctly.
# It is a good practice to use environment variables for sensitive information like database credentials.
# This code is useful for testing the connection to the database and ensuring that the psycopg2 library is working correctly.
# It is a good practice to use environment variables for sensitive information like database credentials.
# Make sure to install the required libraries using pip:
# pip install psycopg2-binary python-dotenv
# This code connects to a PostgreSQL database using the psycopg2 library and prints the version of the database.
# It uses the dotenv library to load environment variables from a .env file, which contains the database connection details.
# Make sure to create a .env file with the following content:
# DB_HOST=your_host
# DB_PORT=your_port
# DB_NAME=your_database_name
# DB_USER=your_username
# DB_PASSWORD=your_password

#python main.py
# This code connects to a PostgreSQL database using the psycopg2 library and prints the version of the database.
# It uses the dotenv library to load environment variables from a .env file, which contains the database connection details.
