from nicegui import ui
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Read credentials from environment variables
hostname = os.getenv("vehiclemax-1.c1yiowcm4goo.us-east-2.rds.amazonaws.com")
database = os.getenv("postgres")
username = os.getenv("DVehicleMax")
pwd = os.getenv("Keilacodingspace0033?")
port_id = int(os.getenv("DB_PORT", 5432))  # default to 5432 if not set

create_table_query = '''
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id SERIAL PRIMARY KEY,       -- Auto-incrementing ID for each vehicle
    vehicle_name VARCHAR(255) NOT NULL,  -- Name of the vehicle
    vehicle_color VARCHAR(255) NOT NULL  -- Color of the vehicle
);
'''

# Add a header to the page using ui.header
ui.header('Vehicle Max').classes('text-4xl font-bold text-center mt-4')

def execute_query(query, values=None):
    try:
        conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if values:
            cur.execute(query, values)
        else:
            cur.execute(query)
        conn.commit()
        result = cur.fetchall() if cur.description else None
        cur.close()
        return result
    except Exception as error:
        print("ERROR:", error)
        return None
    finally:
        if conn:
            conn.close()

# NiceGUI front end
def add_vehicle(vehicle_id, vehicle_name, vehicle_color):
    query = '''INSERT INTO vehicles (vehicle_id, vehicle_name, vehicle_color)
               VALUES (%s, %s, %s)'''
    execute_query(query, (vehicle_id, vehicle_name, vehicle_color))
    ui.notify(f'Vehicle {vehicle_name} added successfully!')

def fetch_vehicles():
    query = 'SELECT * FROM vehicles'
    vehicles = execute_query(query)
    table.rows.clear()
    if vehicles:
        for vehicle in vehicles:
            table.add_row(vehicle['vehicle_id'], vehicle['vehicle_name'], vehicle['vehicle_color'])

# UI layout
ui.label('Vehicle Management System').classes('text-2xl font-bold')
with ui.row():
    vehicle_id = ui.input('Vehicle ID').props('type=number')
    vehicle_name = ui.input('Vehicle Name')
    vehicle_color = ui.input('Vehicle Color')
    ui.button('Add Vehicle', on_click=lambda: add_vehicle(
        int(vehicle_id.value), vehicle_name.value, vehicle_color.value))

ui.button('Fetch Vehicles', on_click=fetch_vehicles)
table = ui.table(columns=['ID', 'Name', 'Color'], rows=[])

ui.run(title='VehicleMax', port=8080)
