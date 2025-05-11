import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read credentials from environment variables
hostname = os.getenv("vehiclemax-1.c1yiowcm4goo.us-east-2.rds.amazonaws.com")
database = os.getenv("postgres")
username = os.getenv("DVehicleMax")
pwd = os.getenv("Keilacodingspace0033?")
port_id = int(os.getenv("DB_PORT", 5432))  # default to 5432 if not set

conn = None

try:
    print("Trying connection...")
    conn = psycopg2.connect(
        host='vehiclemax-1.c1yiowcm4goo.us-east-2.rds.amazonaws.com',
        dbname='postgres',
        user='VehicleMax',
        password='Keilacodingspace0033?',
        port=5432
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
