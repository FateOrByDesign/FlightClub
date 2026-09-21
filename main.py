import os
from dotenv import load_dotenv
import requests_cache

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

# Flight search data
flight_search_data = FlightSearch(SERP_API_KEY, SERP_API_ENDPOINT, session)
# Google sheet data
data = DataManager(SHEETY_ENDPOINT, SHEETY_TOKEN, session, flight_search_data)
# If data is missing in the sheet go and update those data
data.update_the_sheet_if_data_ismissing()
