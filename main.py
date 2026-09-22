import os
from dotenv import load_dotenv
import requests_cache

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

load_dotenv()
session = requests_cache.CachedSession("flight_price.cache", expire_after=360 * 10)

SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
SHEETY_TOKEN = os.getenv("SHEETY_AUTHORIZATION")
SERP_API_ENDPOINT = os.getenv("SERP_API_ENDPOINT")
SERP_API_KEY = os.getenv("SERP_API_KEY")
if not SHEETY_ENDPOINT: raise ValueError("Error: There was an issue loading the SHEETY_ENDPOINT.")
if not SHEETY_TOKEN: raise ValueError("Error: There was an issue loading the SHEETY_TOKEN.")
if not SERP_API_ENDPOINT: raise ValueError("Error: There was an issue loading the SERP_API_ENDPOINT.")
if not SERP_API_KEY : raise ValueError("Error: There was an issue loading the SERP_API_KEY.")

# Flight search data
flight_search_data = FlightSearch(SERP_API_KEY, SERP_API_ENDPOINT, session)
# Google sheet data
data = DataManager(SHEETY_ENDPOINT, SHEETY_TOKEN, session, flight_search_data)
# If data is missing in the sheet go and update those data
data.update_the_sheet_if_data_ismissing()

# Returns completed sheet results
sheet_data = data.return_completed_sheet_data()

destination_iata_code = sheet_data[0][1]
lowest_expected_price = sheet_data[0][2]

# get the cheepest flight options for given iata_code within a six-month window
cheepest_flight_options = flight_search_data.get_flights_within_next_six_months(destination_iata_code)
# format the flight data
flight_data = FlightData(cheepest_flight_options, lowest_expected_price)

# check if cheap flight available for the expected price
if flight_data.compare_with_expected_price():
    flight_departure_date = flight_data.flight_outbound_date
    flight_return_date = flight_data.flight_return_date
    flight_details = flight_data.flights
    google_flight_link = flight_data.google_flight_link
    print(flight_departure_date,flight_return_date, flight_details,google_flight_link)



