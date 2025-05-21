from nicegui import ui
import pandas as pd

# Load the CSV file with a specified encoding
file_path = "Year-Make-Model-Trim-Full-Specs-by-Teoalida-SAMPLE.csv"
data = pd.read_csv(file_path, encoding="latin1")  # Use 'latin1' encoding for compatibility

# Display all columns in the output
pd.set_option('display.max_columns', None)

# Filter data for each make
bmw_data = data[data['Make'] == 'BMW']
ford_data = data[data['Make'] == 'Ford']
toyota_data = data[data['Make'] == 'Toyota']

# Convert the filtered DataFrames to lists of dictionaries for NiceGUI
bmw_table_data = bmw_data.to_dict(orient="records")
ford_table_data = ford_data.to_dict(orient="records")
toyota_table_data = toyota_data.to_dict(orient="records")

# Create column definitions for NiceGUI tables
columns = [{"name": col, "label": col, "field": col, "sortable": True} for col in data.columns]

# NiceGUI UI
ui.label("Car Information Tables").classes("text-2xl font-bold")

ui.label("BMW Vehicles").classes("text-xl font-bold mt-4")
ui.table(columns=columns, rows=bmw_table_data).classes("max-h-96 overflow-auto")

ui.label("Ford Vehicles").classes("text-xl font-bold mt-4")
ui.table(columns=columns, rows=ford_table_data).classes("max-h-96 overflow-auto")

ui.label("Toyota Vehicles").classes("text-xl font-bold mt-4")
ui.table(columns=columns, rows=toyota_table_data).classes("max-h-96 overflow-auto")

ui.run(title="Car Information Viewer")