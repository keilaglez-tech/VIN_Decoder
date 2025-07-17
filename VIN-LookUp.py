from nicegui import ui
import requests

API_KEY = "ZrQEPSkKa2VpMDkxNy5rQGdtYWlsLmNvbQ=="

def fetch_vehicle_info(vin):
    url = f"https://auto.dev/api/vin/{vin}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        return {"error": f"HTTP error: {err.response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def display_vehicle_info(data):
    # Top-level info
    make = data.get('make', {}).get('name', 'N/A')
    model = data.get('model', {}).get('name', 'N/A')
    year = data.get('years', [{}])[0].get('year', 'N/A')
    trim = data.get('years', [{}])[0].get('styles', [{}])[0].get('trim', 'N/A')
    body = data.get('categories', {}).get('primaryBodyType', 'N/A')
    driven_wheels = data.get('drivenWheels', 'N/A')
    num_doors = data.get('numOfDoors', 'N/A')
    mpg = data.get('mpg', {})
    price = data.get('price', {}).get('baseMsrp', 'N/A')

    ui.label(f"🚗 {year} {make} {model} {trim}").style("font-size: 1.2em; font-weight: bold; margin-bottom: 8px;")
    ui.label(f"Body: {body} | Driven Wheels: {driven_wheels} | Doors: {num_doors}")
    ui.label(f"MPG: City {mpg.get('city', 'N/A')}, Highway {mpg.get('highway', 'N/A')}")
    ui.label(f"Base MSRP: ${price}")

    # Engine details
    engine = data.get('engine', {})
    if engine:
        ui.label("Engine:").style("font-weight: bold; margin-top: 8px;")
        ui.label(f"  {engine.get('cylinder', 'N/A')}-cyl {engine.get('size', 'N/A')}L {engine.get('fuelType', '')} {engine.get('configuration', '')}")
        ui.label(f"  Horsepower: {engine.get('horsepower', 'N/A')} hp @ {engine.get('rpm', {}).get('horsepower', 'N/A')} rpm")
        ui.label(f"  Torque: {engine.get('torque', 'N/A')} lb-ft @ {engine.get('rpm', {}).get('torque', 'N/A')} rpm")

    # Transmission details
    transmission = data.get('transmission', {})
    if transmission:
        ui.label("Transmission:").style("font-weight: bold; margin-top: 8px;")
        ui.label(f"  {transmission.get('numberOfSpeeds', 'N/A')}-speed {transmission.get('automaticType', transmission.get('transmissionType', 'N/A'))}")

    # Options (show only first 5 for brevity)
    options = data.get('options', [])
    if options:
        ui.label("Options:").style("font-weight: bold; margin-top: 8px;")
        for category in options:
            ui.label(f"  {category.get('category', 'Other')}:").style("font-style: italic;")
            for opt in category.get('options', [])[:5]:
                ui.label(f"    - {opt.get('name', '')}")

    # Colors (show only first 3 for brevity)
    colors = data.get('colors', [])
    if colors:
        ui.label("Colors:").style("font-weight: bold; margin-top: 8px;")
        for color_cat in colors:
            ui.label(f"  {color_cat.get('category', 'Other')}:").style("font-style: italic;")
            for color in color_cat.get('options', [])[:3]:
                ui.label(f"    - {color.get('name', '')}")

ui.label("🚘 VIN Decoder").style("font-size: 1.5em; font-weight: bold; margin-bottom: 10px;")
vin_input = ui.input(label="Enter VIN").style("width: 100%")
result_area = ui.column()

def on_lookup_click():
    result_area.clear()
    vin = vin_input.value.strip()

    with result_area:
        if not vin or len(vin) != 17 or not vin.isalnum():
            ui.label("❌ Please enter a valid 17-character VIN.").style("color: red")
            return
        vehicle_data = fetch_vehicle_info(vin)
        ui.label("🔍 VIN Lookup Results").style("font-weight: bold; margin-top: 10px")

        if "error" in vehicle_data:
            ui.label(f"❌ Error: {vehicle_data['error']}").style("color: red")
        elif not vehicle_data:
            ui.label("No data found for this VIN.").style("color: orange")
        else:
            display_vehicle_info(vehicle_data)

ui.button("Search VIN", on_click=on_lookup_click)

ui.run()

