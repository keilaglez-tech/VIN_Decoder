# This code creates a web application using NiceGUI to display vehicle information from a CSV file.
# It allows users to navigate through different makes and view detailed information about each vehicle.
# The application is structured with a main page that lists vehicle makes, and each make has its own page
# displaying the vehicles available for that make.
# The vehicle details page shows specific information about each vehicle when clicked.
# The code uses pandas to read the CSV file and filter data based on vehicle makes.
# The application is designed to be user-friendly and provides a clear navigation structure for users to explore vehicle information.
# The CSV file used in this code contains detailed specifications for various vehicle makes and models.
# The application is built using NiceGUI, a Python library for creating web applications with a simple and intuitive API.
# The code is structured to create a clean and organized user interface, making it easy for users to find and view vehicle information.
# FullCarInfo3.py

from nicegui import ui, app
import pandas as pd
import csv
import os
import requests
from dotenv import load_dotenv

file_path = "CopartCars.csv"
data = pd.read_csv(file_path, encoding="utf-8-sig")
data.columns = data.columns.str.strip()

ADMIN_FIELDS = [
    'Make', 'Model', 'Year', 'Trim', 'Miles', 'Color', 'Engine', 'Transmission', 'Title', 'Gas', 'Doors', 'Price'
]

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

def render_header():
    with ui.header().classes('bg-blue-900 text-white p-4'):
        ui.label("VehicleMax").classes("text-3xl font-bold")
        with ui.row().classes('ml-8'):
            ui.button("Home", on_click=lambda: ui.navigate.to('/')).props('flat color=white')
            ui.button("Admin", on_click=lambda: ui.navigate.to('/admin')).props('flat color=white')
            ui.button("VIN Lookup", on_click=lambda: ui.navigate.to('/vin-lookup')).props('flat color=white')

@ui.page('/')
def main_page():
    render_header()
    ui.label("Car Information Viewer").classes("text-2xl font-bold mt-4")
    with ui.row().classes("flex-wrap"):
        for _, row in data.iterrows():
            with ui.card().classes("w-80 m-4 shadow-lg"):
                ui.label(f"{row['Year']} {row['Make']} {row['Model']} {row['Trim']}").classes("text-lg font-bold mb-2")
                for col, value in row.items():
                    if col not in ['Year', 'Make', 'Model', 'Trim']:
                        ui.label(f"{col}: {value}").classes("text-sm")

@ui.page('/admin')
def admin_page():
    render_header()
    ui.label('Admin: Add New Vehicle').classes('text-2xl font-bold mb-4')
    inputs = {field: ui.input(label=field).classes('mb-2') for field in ADMIN_FIELDS}

    def add_vehicle():
        new_row = [inputs[field].value for field in ADMIN_FIELDS]
        with open(file_path, 'a', newline='', encoding='latin1') as f:
            writer = csv.writer(f)
            writer.writerow(new_row)
        ui.notify('Vehicle added! Please reload the app to see the new vehicle.')

    ui.button('Add Vehicle', on_click=add_vehicle).classes('mt-4')

@ui.page('/vin-lookup')
def vin_lookup_page():
    render_header()
    ui.label("VIN Lookup").classes("text-2xl font-bold mt-4")
    vin_input = ui.input("Enter VIN").classes("mb-4")
    result_label = ui.label("").classes("mt-2")

    def lookup():
        vin = vin_input.value.strip()
        if not vin:
            result_label.text = "Please enter a VIN."
            return
        try:
            response = requests.get(
                "https://api.api-ninjas.com/v1/vinlookup",
                params={"vin": vin},
                headers={"X-Api-Key": API_KEY}
            )
            if response.status_code == 200:
                data = response.json()
                if data:
                    details = "\n".join(f"{k}: {v}" for k, v in data.items())
                    result_label.text = details
                else:
                    result_label.text = "No details found for this VIN."
            else:
                result_label.text = f"API error: {response.status_code}"
        except Exception as e:
            result_label.text = f"Error: {e}"

    ui.button("Lookup", on_click=lookup).classes("mt-2")

ui.run(title="Car Information Viewer", storage_secret="P4ssword!")

