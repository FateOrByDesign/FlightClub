import os
from dotenv import load_dotenv
import requests_cache

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

load_dotenv()
session = requests_cache.CachedSession("flight_price.cache", expire_after=360 * 10)

SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
SHEETY_TOKEN = os.getenv("SHEETY_AUTHORIZATION")
SERP_API_ENDPOINT = os.getenv("SERP_API_ENDPOINT")
SERP_API_KEY = os.getenv("SERP_API_KEY")
TELEGRAM_KEY = os.getenv("TELEGRAM_BOT_API")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")
if not SHEETY_ENDPOINT: raise ValueError("Error: There was an issue loading the SHEETY_ENDPOINT.")
if not SHEETY_TOKEN: raise ValueError("Error: There was an issue loading the SHEETY_TOKEN.")
if not SERP_API_ENDPOINT: raise ValueError("Error: There was an issue loading the SERP_API_ENDPOINT.")
if not SERP_API_KEY : raise ValueError("Error: There was an issue loading the SERP_API_KEY.")
if not TELEGRAM_KEY: raise ValueError("Error: There was an issue loading the TELEGRAM_KEY.")
if not TELEGRAM_CHAT_ID: raise ValueError("Error: There was an issue loading the TELEGRAM_CHAT_ID.")

DEPARTURE_AIRPORT_IATA_CODE = "CMB"

# Flight search data class
flight_search_data = FlightSearch(SERP_API_KEY, SERP_API_ENDPOINT, session, DEPARTURE_AIRPORT_IATA_CODE)

# Google sheet data class
data = DataManager(SHEETY_ENDPOINT, SHEETY_TOKEN, session, flight_search_data)
# If data is missing in the sheet go and update those data
data.update_the_sheet_if_data_ismissing()

# Returns completed sheet results
sheet_data = data.return_completed_sheet_data()

for destination in sheet_data:
    destination_iata_code = destination[1]
    lowest_expected_price = destination[2]

    # get the cheepest flight options for given iata_code within a six-month window
    cheepest_flight_options = flight_search_data.get_flights_within_next_six_months(destination_iata_code)

    # Flight data class
    flight_data = FlightData(cheepest_flight_options, lowest_expected_price)


    # check if cheap flight available for the expected price
    if flight_data.get_the_cheapest_flight_and_compare_value():
        # notifications manger
        notifications = NotificationManager(flight_data, TELEGRAM_KEY, TELEGRAM_CHAT_ID)
        notifications.send_message_via_telegram()



