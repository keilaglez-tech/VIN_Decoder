import pandas as pd

# Load the CSV file
file_path = "carapi-opendatafeed-sample.csv"
data = pd.read_csv(file_path)

# Function to filter cars by make and model
def filter_cars(make=None, model=None):
    filtered_data = data
    if make:
        filtered_data = filtered_data[filtered_data['Make Name'].str.contains(make, case=False, na=False)]
    if model:
        filtered_data = filtered_data[filtered_data['Model Name'].str.contains(model, case=False, na=False)]
    return filtered_data

# Example usage
make_input = input("Enter car make (e.g., Acura): ")
model_input = input("Enter car model (e.g., MDX): ")

# Filter the data
filtered_cars = filter_cars(make=make_input, model=model_input)

# Display the results
if not filtered_cars.empty:
    print(f"Cars matching Make: {make_input}, Model: {model_input}")
    print(filtered_cars[['Make Name', 'Model Name', 'Trim Year', 'Trim Name', 'Trim Msrp', 'Engine Fuel Type']])
else:
    print("No cars found matching the criteria.")