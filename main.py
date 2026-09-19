import os
from dotenv import load_dotenv
import requests_cache
from platformdirs import api

from data_manager import DataManager
from flight_search import FlightSearch

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


# Google sheet data
data = DataManager(SHEETY_ENDPOINT, SHEETY_TOKEN)
# Flight search data
flight_search_data = FlightSearch(SERP_API_KEY, SERP_API_ENDPOINT)


# get the missing city and the row id from the row that are missing the IATA codes
sheet_data = data.get_city_from_missing_IATA_records(session)
print(sheet_data)

# go through the missing city data and get the IATA codes from the serp_api flight autocomplete engine
for item in sheet_data:
    airport_name = item[1]
    flight_search_results = flight_search_data.get_iata_codes(session,airport_name)
    airport_iata_code = flight_search_results["suggestions"][0]["airports"][0]["id"]
    item.append(airport_iata_code)
    data.set_the_missing_IATA_codes(session, str(item[0]), airport_iata_code)

print(sheet_data)
