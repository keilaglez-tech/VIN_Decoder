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

file_path = "CopartCars.csv"
data = pd.read_csv(file_path, encoding="utf-8-sig")
data.columns = data.columns.str.strip()

makes = {
    "Hyundai": data[data['Make'] == 'Hyundai'],
    "Nissan": data[data['Make'] == 'Nissan'],
    "Chevrolet": data[data['Make'] == 'Chevrolet'],
    "Mercedes": data[data['Make'] == 'Mercedes'],
    "Toyota": data[data['Make'] == 'Toyota'],
}

ADMIN_FIELDS = [
    'Make', 'Model', 'Year', 'Trim', 'Miles', 'Color', 'Engine', 'Transmission', 'Title', 'Gas', 'Doors', 'Price'
]

# --- Header without Tabs ---
def render_header():
    with ui.header().classes('bg-blue-900 text-white p-4'):
        ui.label("VehicleMax").classes("text-3xl font-bold")
        with ui.row().classes('ml-8'):
            ui.button("Home", on_click=lambda: ui.navigate.to('/')).props('flat color=white')
            ui.button("Admin", on_click=lambda: ui.navigate.to('/admin')).props('flat color=white')

@ui.page('/')
def main_page():
    render_header()
    ui.label("Car Information Viewer").classes("text-2xl font-bold mt-4")
    for make_name in makes.keys():
        ui.button(
            f"{make_name} Vehicles",
            on_click=lambda make=make_name: ui.navigate.to(f"/vehicles/{make}")
        ).classes("text-xl mt-4")

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

# --- Vehicles list page for each make ---
def create_vehicles_page(make_name, make_data):
    @ui.page(f"/vehicles/{make_name}")
    def vehicles_page():
        render_header()
        ui.label(f"{make_name} Vehicles").classes("text-xl font-bold")
        vehicles = list(make_data.iterrows())
        for i in range(0, len(vehicles), 5):
            with ui.row().classes('items-center'):
                for _, row in vehicles[i:i+5]:
                    vehicle_label = f"{row['Year']} {row['Make']} {row['Model']} {row['Trim']}"
                    with ui.column().classes('items-center flex-1 min-w-0'):
                        ui.button(
                            vehicle_label,
                            on_click=lambda r=row: ui.navigate.to(f"/vehicle/{r['Make']}/{r['Model']}/{r['Trim']}")
                        )
                    create_vehicle_details_page(row)
        ui.button("Back to Main Menu", on_click=lambda: ui.navigate.to("/"))

# --- Vehicle details page ---
def create_vehicle_details_page(vehicle_row):
    @ui.page(f"/vehicle/{vehicle_row['Make']}/{vehicle_row['Model']}/{vehicle_row['Trim']}")
    def vehicle_details():
        render_header()
        ui.label("Vehicle Details").classes("text-xl font-bold")
        for col, value in vehicle_row.items():
            ui.label(f"{col}: {value}")
        ui.button("Back to Vehicles", on_click=lambda: ui.navigate.to(f"/vehicles/{vehicle_row['Make']}"))

# Register all pages
for make_name, make_data in makes.items():
    create_vehicles_page(make_name, make_data)

ui.run(title="Car Information Viewer", storage_secret="P4ssword!")

