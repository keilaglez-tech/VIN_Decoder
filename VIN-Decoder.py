# This code is a complete NiceGUI application that allows users to look up vehicle information by VIN.
# It includes error handling and displays results in a table format.

from operator import gt
from nicegui import ui  # Import NiceGUI for building the web interface
import requests          # Import requests for making HTTP requests to the API
import os                # Import os for environment variable access
from dotenv import load_dotenv  # Import dotenv to load environment variables from .env file
import logging           # Import logging for error logging


@ui.page('/')
def index():
    ui.markdown('### Share this link:')
    for url in app.urls:        # app.urls contains both localhost and your on-air URL
        ui.link(text=url, url=url, target=url)


# Load API key from .env
load_dotenv()            # Loads environment variables from a .env file into the environment
API_KEY = os.getenv("API_KEY")  # Retrieves the API key from environment variables

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR)  # Logs errors to error.log file

def render_header():
    # Creates a header section for the web page
    with ui.header().classes('background-color: #4682B4; text-white p-4'):
        ui.label("VIN Decoder").classes("text-3xl font-bold")  # Title label
        with ui.row().classes('ml-8'):
            ui.button("VIN Lookup", on_click=lambda: ui.navigate.to('/')).props('flat color=white')  # Home button
            ui.button("Search Vehicles", on_click=lambda: ui.navigate.to('/car-api-search')).props('flat color=white')  # Search page button


@ui.page('/')
def vin_decoder_page():
    # Main page for VIN lookup
    render_header()
    with ui.column().classes('fit items-center justify-center').style('height: 70vh;'):
        with ui.card().classes('q-pa-md').style('width: 600px; max-width: 95vw; background-color: #4682B4; color: white;'):

            ui.label("Enter a VIN number to lookup").classes("text-2xl font-bold mt-2")
            vin_input = ui.input("Enter VIN").classes("mb-4")
            result_label = ui.label("").classes("mt-2")
            table_container = ui.element("div")
            # Store last 3 VIN searches
            vin_search_history = []

            def lookup():
                vin = vin_input.value.strip()
                table_container.clear()
                if not vin or len(vin) != 17 or not vin.isalnum():
                    result_label.text = "Please enter a valid 17-character VIN."
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
                            result_label.text = ""

                            with table_container:
                                ui.label(f"VIN Details for {vin}").classes("text-xl font-bold mb-2")
                                ui.table(
                                    columns=[{"name": "key", "label": "Field", "field": "key"},
                                            {"name": "value", "label": "Value", "field": "value"}],
                                    rows=[{"key": k, "value": v} for k, v in data.items()],
                                    row_key="key"
                                ).classes("w-full")

                            # Add VIN to history, keep only last 3
                            vin_search_history.insert(0, vin)
                            if len(vin_search_history) > 3:
                                vin_search_history.pop()
                            history_container.clear()
                            with history_container:
                                ui.label("Last 3 VIN Searches:").classes("text-lg font-bold mt-4")
                                for v in vin_search_history:
                                    ui.label(v).classes("text-base")
                        else:
                            result_label.text = "No details found for this VIN."
                    else:
                        result_label.text = "There was a problem with the VIN lookup service. Please try again later."
                        logging.error(f"API error: {response.status_code} - {response.text}")
                except Exception as e:
                    result_label.text = "An unexpected error occurred. Please try again later."
                    logging.error(f"Exception during VIN lookup: {e}")

            def clear_vin():
                vin_input.value = ""
                result_label.text = ""
                table_container.clear()

            with ui.row():
                ui.button("Lookup", on_click=lookup).classes("mt-2")
                ui.button("Clear", on_click=clear_vin).classes("mt-2")

            # Section for search history
            history_container = ui.element("div")

@ui.page('/car-api-search')
def car_api_search_page():
    render_header()
    with ui.column().classes('fit items-center justify-center').style('height: 70vh;'):
        with ui.card().classes('q-pa-md').style('width: 600px; max-width: 95vw; background-color: #4682B4; color: white;'):
            ui.label("Search Vehicles").classes("text-2xl font-bold mt-4")

            make_input = ui.input("Make (e.g. toyota)").classes("mb-2")
            model_input = ui.input("Model (e.g. camry)").classes("mb-2")
            year_input = ui.input("Year (e.g. 2018)").classes("mb-2")

            result_label = ui.label("").classes("mt-2")
            table_container = ui.element("div")
            # Store last 3 car searches
            car_search_history = []

            def search():
                table_container.clear()
                params = {}
                if make_input.value: params["make"] = make_input.value.strip()
                if model_input.value: params["model"] = model_input.value.strip()
                if year_input.value: params["year"] = year_input.value.strip()

                try:
                    response = requests.get(
                        "https://api.api-ninjas.com/v1/cars",
                        params=params,
                        headers={"X-Api-Key": API_KEY}
                    )
                    if response.status_code == 200:
                        cars = response.json()
                        if cars:
                            result_label.text = ""

                            with table_container:
                                ui.label("Search Results").classes("text-xl font-bold mb-2")
                                for car in cars:
                                    ui.label(f"{car.get('make', '').title()} {car.get('model', '').title()}").classes(
                                        "text-lg font-bold mt-4"
                                    )
                                    ui.table(
                                        columns=[
                                            {"name": "key", "label": "Field", "field": "key"},
                                            {"name": "value", "label": "Value", "field": "value"},
                                        ],
                                        rows=[{"key": k.replace("_", " ").title(), "value": v} for k, v in car.items()],
                                        row_key="key",
                                    ).classes("w-full mb-4")

                            # Add search to history, keep only last 3
                            search_record = f"{make_input.value} {model_input.value} {year_input.value}".strip()
                            car_search_history.insert(0, search_record)
                            if len(car_search_history) > 3:
                                car_search_history.pop()
                            car_history_container.clear()
                            with car_history_container:
                                ui.label("Last 3 Vehicle Searches:").classes("text-lg font-bold mt-4")
                                for s in car_search_history:
                                    ui.label(s).classes("text-base")
                        else:
                            result_label.text = "No cars found for the given parameters."
                    else:
                        result_label.text = "There was a problem with the Cars API service. Please try again later."
                        logging.error(f"Cars API error: {response.status_code} - {response.text}")
                except Exception as e:
                    result_label.text = "An unexpected error occurred. Please try again later."
                    logging.error(f"Exception during Cars API search: {e}")

            def clear_search():
                make_input.value = ""
                model_input.value = ""
                year_input.value = ""
                result_label.text = ""
                table_container.clear()

            with ui.row():
                ui.button("Search", on_click=search).classes("mt-2")
                ui.button("Clear", on_click=clear_search).classes("mt-2")

            # Section for search history
            car_history_container = ui.element("div")


#ui.run( on_air=True,  # Run the application on the server
 #   title="VIN Decoder",
   # port=8081,
 #   reload=True
#)

ui.run(host='127.0.0.1', port=8081, reload=True)