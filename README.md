# Phonebook
Simple python Elasticsearch phonebook

## Setup
A couple steps have to be performed to prepare the Elasticsearch database locally:
* Run: `curl -fsSL https://elastic.co/start-local | sh`
* Copy the API key printed to the screen and paste it into the `Elasticsearch` `api_key` field

## Running the code
To run the code simply run: `python3 main.py` and then follow instructions on the screen

## Cleanup
* Once you are done running the code, cleanup the elastic local instance with `cd elastic-start-local && ./uninstall.sh`

# Limitations
* **Case sensitivity:** Names have to be unique but are case sensitive - i.e. "Alice Smith" and "Alice smith" are considered 2 different unique names. Similarly searching names is also case sensitive - searching for "alic" won't return "Alice"
* **Python version:** Code requires python3.9 or newer to work