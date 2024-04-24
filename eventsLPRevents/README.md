# Eagle Eye Networks - License Plate Recognition - Events Endpoint README

## Description
This Python script utilizes the Eagle Eye Networks API to retrieve events associated with license plate recognition (LPR) from a specified range of dates. It fetches details like the unique plates detected, the direction of the vehicle movement (entry/exit), and logs all data to an output file.

## Requirements
- Python 3.x
- `requests` library
- `json` library
- `logging` library

## Setup
To run the script, you will need to provide:
- `access_token`: Bearer token for authentication with the API.
- `base_url`: The base URL of the API (excluding https://).

These values must be inserted into the script before execution.

## Configuration
The script is configured to log its operations to `debug.log`. It outputs the results into `output.log`. It logs each API request URL along with parameters.

### Logging Configuration
Logging is set up with the following line:
    +++logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')+++

### API Request Details
API requests are made to `base_url` which is constructed within the script as follows:
    +++base_url = f"https://{base_url}/api/v3.0/lprEvents"+++

The parameters for the API request are set up in the `params` dictionary to filter the events by timestamps and include specific related data.

### Headers
The API requests include headers for JSON acceptance and authorization using the provided `access_token`.

## Usage
Execute the script in a Python environment. The script will:
- Make paginated requests to the Eagle Eye Networks API.
- Fetch events within the specified date range.
- Write each API response to `output.log` in a readable JSON format.
- Extract and count unique license plates and direction-specific events.

Upon completion, the script will output:
- Total number of events fetched.
- Total number of unique license plates detected.
- Count of entry and exit events.

## Output
The script prints real-time progress of the number of events fetched and finally outputs the totals to the console. The complete data fetched from the API is written to `output.log` in a structured format.

## Closure
Ensure all resources are properly closed, as seen with the `output_file` object.

## Conclusion
This script is useful for monitoring and analyzing vehicle movements using LPR technology via the Eagle Eye Networks API, with easy configuration and extensive logging for debugging and verification purposes.
