from nicegui import ui
import csv
import os

# Path to the CSV file
CSV_FILE = "VINData (1).csv"

def fetch_vehicle_details_from_csv(vin):
    try:
        # Open and read the CSV file
        with open(CSV_FILE, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if the VIN matches (if VIN is part of the data)
                if row.get("valueid") == vin:
                    details = (
                        f"Make: {row.get('Make', 'N/A')}\n"
                        f"Model: {row.get('Model', 'N/A')}\n"
                        f"Year: {row.get('Model Year', 'N/A')}\n"
                        f"Country: {row.get('Plant Country', 'N/A')}\n"
                        f"Class: {row.get('Body Class', 'N/A')}\n"
                    )
                    result_label.text = f"Vehicle Details:\n{details}"
                    return
            result_label.text = "No details found for the given VIN."
    except Exception as e:
        result_label.text = f"Error: {str(e)}"

# UI Layout
ui.label("VIN Lookup App (CSV)").classes("text-2xl font-bold")
vin_input = ui.input("Enter VIN").props("type=text")
ui.button("Fetch Vehicle Details", on_click=lambda: fetch_vehicle_details_from_csv(vin_input.value))
result_label = ui.label().classes("text-lg text-green-500")

ui.run(title="VIN Lookup App VIN Data (CSV)")