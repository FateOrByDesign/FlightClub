import os
from smtplib import SMTP, SMTPException
from dotenv import load_dotenv
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

load_dotenv()

SHEETY_ENDPOINT_PRICES = os.getenv("SHEETY_ENDPOINT_PRICES")
SHEETY_ENDPOINT_USERS = os.getenv("SHEETY_ENDPOINT_USERS")
SHEETY_TOKEN = os.getenv("SHEETY_AUTHORIZATION")
SERP_API_ENDPOINT = os.getenv("SERP_API_ENDPOINT")
SERP_API_KEY = os.getenv("SERP_API_KEY")
TELEGRAM_KEY = os.getenv("TELEGRAM_BOT_API")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")
SENDER_EMAIL = os.getenv("SENDERS_EMAIL")
SMTP_PASSWORD = os.getenv("GOOGLE_SMTP_APP_PASSWORD")
if not SHEETY_ENDPOINT_PRICES: raise ValueError("Error: There was an issue loading the SHEETY_ENDPOINT_PRICES.")
if not SHEETY_ENDPOINT_USERS: raise ValueError("Error: There was an issue loading the SHEETY_ENDPOINT_USERS.")
if not SHEETY_TOKEN: raise ValueError("Error: There was an issue loading the SHEETY_TOKEN.")
if not SERP_API_ENDPOINT: raise ValueError("Error: There was an issue loading the SERP_API_ENDPOINT.")
if not SERP_API_KEY : raise ValueError("Error: There was an issue loading the SERP_API_KEY.")
if not TELEGRAM_KEY: raise ValueError("Error: There was an issue loading the TELEGRAM_KEY.")
if not TELEGRAM_CHAT_ID: raise ValueError("Error: There was an issue loading the TELEGRAM_CHAT_ID.")
if not SENDER_EMAIL: raise ValueError("Error: There was an issue loading the SENDERS_EMAIL.")
if not SMTP_PASSWORD: raise ValueError("Error: There was an issue loading the SMTP_PASSWORD.")

DEPARTURE_AIRPORT_IATA_CODE = "CMB"
DEPARTURE_CITY = "Colombo"

# Flight search data class
flight_search_data = FlightSearch(SERP_API_KEY, SERP_API_ENDPOINT, DEPARTURE_AIRPORT_IATA_CODE)

# Google sheet data class
data = DataManager(SHEETY_ENDPOINT_PRICES, SHEETY_ENDPOINT_USERS, SHEETY_TOKEN, flight_search_data)

# If data is missing in the sheet go and update those data
data.update_the_sheet_if_data_ismissing()

# Returns completed sheet results
sheet_data = data.return_completed_sheet_data()

# User data (emails)
emails_to_send = data.get_user_info()

# setup smtp connection
connection = SMTP("smtp.gmail.com", port=587)
connection.starttls()
connection.login(user=SENDER_EMAIL, password=SMTP_PASSWORD)

# Notifications Manager
notifications = NotificationManager(TELEGRAM_KEY, TELEGRAM_CHAT_ID,SENDER_EMAIL, departure=f"{DEPARTURE_CITY}({DEPARTURE_AIRPORT_IATA_CODE})")

for destination in sheet_data:
    destination_city = destination[0]
    destination_iata_code = destination[1]
    lowest_expected_price = destination[2]

    # get the cheepest flight options for given iata_code within a six-month window
    print(f"Getting direct flights for {destination_city}...")
    cheapest_flight_options = flight_search_data.get_flights_within_next_six_months(destination_iata_code)
    if cheapest_flight_options is not None:
        print(f"Direct flight to {destination_city} found.\n")
    else:
        print(f"No direct flight to {destination_city}. Looking for indirect flights...")
        cheapest_flight_options = flight_search_data.get_flights_within_next_six_months(destination_iata_code, is_direct=False)
        if cheapest_flight_options is not None:
            print(f"Indirect flight to {destination_city} found.\n")
        else:
            print(f"No flights found to {destination_city}. Skipping.")
            continue

    # Flight data class
    flight_data = FlightData(cheapest_flight_options, lowest_expected_price)


    # check if cheap flight available for the expected price
    if flight_data.get_the_cheapest_flight_and_compare_value():
        # send the notification via telegram
        notifications.send_message_via_telegram(flight_data, destination_city)
        # send notifications to email
        try:
            for email in emails_to_send:
                notifications.send_email(connection,flight_data,DEPARTURE_CITY, destination_city, email)
            print("All emails sent successfully.")
        except SMTPException:
            print("Error occurred with with sending the emails.")

connection.close()




