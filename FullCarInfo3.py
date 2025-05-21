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

from nicegui import ui
import pandas as pd

# Load the CSV file with a specified encoding
file_path = "Year-Make-Model-Trim-Full-Specs-by-Teoalida-SAMPLE.csv"
data = pd.read_csv(file_path, encoding="latin1")  # Use 'latin1' encoding for compatibility

# Filter data for each make
makes = {
    "BMW": data[data['Make'] == 'BMW'],
    "Ford": data[data['Make'] == 'Ford'],
    "Toyota": data[data['Make'] == 'Toyota']
}

# Function to create a page for vehicle details
def create_vehicle_details_page(vehicle_row):
    @ui.page(f"/vehicle/{vehicle_row['Make']}/{vehicle_row['Model']}/{vehicle_row['Trim']}")
    def vehicle_details():
        ui.label("Vehicle Details").classes("text-xl font-bold")
        for col, value in vehicle_row.items():
            ui.label(f"{col}: {value}")
        ui.button("Back to Vehicles", on_click=lambda: ui.navigate.to(f"/vehicles/{vehicle_row['Make']}"))

# Function to create a page for vehicles of a specific make
def create_vehicles_page(make_name, make_data):
    @ui.page(f"/vehicles/{make_name}")
    def vehicles_page():
        ui.label(f"{make_name} Vehicles").classes("text-xl font-bold")
        for _, row in make_data.iterrows():
            vehicle_label = f"{row['Year']} {row['Make']} {row['Model']} {row['Trim']}"
            ui.button(vehicle_label, on_click=lambda r=row: ui.navigate.to(f"/vehicle/{row['Make']}/{row['Model']}/{row['Trim']}"))
            create_vehicle_details_page(row)
        ui.button("Back to Main Menu", on_click=lambda: ui.navigate.to("/"))

# Main page
@ui.page("/")
def main_page():
    ui.label("Car Information Viewer").classes("text-2xl font-bold")
    for make_name in makes.keys():
        # Correct usage of ui.navigate
        ui.button(f"{make_name} Vehicles", on_click=lambda make=make_name: ui.navigate.to(f"/vehicles/{make}")).classes("text-xl mt-4")

# Create pages for each make
for make_name, make_data in makes.items():
    create_vehicles_page(make_name, make_data)

# Run the NiceGUI app
ui.run(title="Car Information Viewer")


