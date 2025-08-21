This web app is a vehicle information lookup tool built with NiceGUI. It provides two main features:

VIN Lookup: Users can enter a Vehicle Identification Number (VIN) to retrieve detailed information about a specific vehicle using the API Ninjas VIN lookup service. Results are displayed in a table, and the last three VIN searches are shown for quick reference.

Car Search: Users can search for vehicles by make, model, and year using the API Ninjas Cars API. Matching vehicles are displayed in a table, and the last three search queries are listed for convenience.

The app includes error handling, search history, and a user-friendly interface with navigation between the two main pages. API keys are loaded securely from environment variables, and errors are logged to a file.