import xml.etree.ElementTree as ET  # For parsing XML
from nicegui import ui
import requests

# Example API endpoint
url = "https://api.example.com/vehicles/GetVehicleVariableList?format=xml"

# Function to fetch and display vehicle variables
def fetch_vehicle_variables():
    try:
        # Make a GET request to the API
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the XML response
            root = ET.fromstring(response.content)
            variables = []
            for variable in root.findall(".//Variable"):
                name = variable.find("Name").text if variable.find("Name") is not None else "N/A"
                description = variable.find("Description").text if variable.find("Description") is not None else "N/A"
                variables.append((name, description))
            
            # Clear and update the table
            variable_table.rows.clear()
            for name, description in variables:
                variable_table.add_row(name, description)
            response_label.text = "Vehicle variables fetched successfully!"
        else:
            response_label.text = f"Error: Unable to fetch data (Status Code: {response.status_code})"
    except Exception as error:
        response_label.text = f"Error: {error}"

# UI layout
ui.label('Vehicle Management System').classes('text-2xl font-bold')
ui.button('Fetch Vehicle Variables', on_click=fetch_vehicle_variables)

# Table to display vehicle variables
variable_table = ui.table(columns=['Variable Name', 'Description'], rows=[])

# Label to display responses
response_label = ui.label().classes('text-lg text-green-500')

ui.run()