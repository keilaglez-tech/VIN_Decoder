from nicegui import ui
import pandas as pd

# Load the CSV file
file_path = "Year-Make-Model-Trim-Full-Specs-by-Teoalida-SAMPLE.csv"
data = pd.read_csv(file_path)

# Display all columns in the output
pd.set_option('display.max_columns', None)

# Convert the DataFrame to a list of dictionaries for NiceGUI
table_data = data.to_dict(orient="records")
columns = [{"name": col, "label": col, "field": col, "sortable": True} for col in data.columns]

# NiceGUI UI
ui.label("Car Information Table").classes("text-2xl font-bold")
ui.table(columns=columns, rows=table_data).classes("max-h-96 overflow-auto")

ui.run(title="Car Information Viewer")