from nicegui import ui
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# VIN Lookup API URL and API Key
VIN_LOOKUP_URL = "https://api.api-ninjas.com/v1/vinlookup"
API_KEY = os.getenv("API_KEY") # Load API key from .env file

def fetch_vehicle_details(vin):
    try:
        headers = {"X-Api-Key": API_KEY}
        params = {"vin": vin}
        response = requests.get(VIN_LOOKUP_URL, headers=headers, params=params)
        if response.status_code == 200:
            vehicle_data = response.json()
            if vehicle_data:
                details = (
                    f"Make: {vehicle_data.get('make', 'N/A')}\n"
                    f"Model: {vehicle_data.get('model', 'N/A')}\n"
                    f"Year: {vehicle_data.get('year', 'N/A')}\n"
                    f"Country: {vehicle_data.get('country', 'N/A')}\n"
                    f"Region: {vehicle_data.get('region', 'N/A')}\n"
                    f"Class: {vehicle_data.get('class', 'N/A')}\n"
                )
                result_label.text = f"Vehicle Details:\n{details}"
            else:
                result_label.text = "No vehicle details found."
        else:
            result_label.text = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        result_label.text = f"Error: {str(e)}"

# UI Layout
ui.label("VIN Lookup App").classes("text-2xl font-bold")
vin_input = ui.input("Enter VIN").props("type=text")
ui.button("Fetch Vehicle Details", on_click=lambda: fetch_vehicle_details(vin_input.value))
result_label = ui.label().classes("text-lg text-green-500")

ui.run(title="VIN Lookup App")