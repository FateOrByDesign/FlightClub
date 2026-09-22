import requests
from flight_data import FlightData

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self, telegram_key, chat_id):
        self.telegram_key = telegram_key
        self.chat_id = chat_id

    def format_message(self, flight_data_object):
        flight_price = flight_data_object.flight["price"]
        departure_airport = flight_data_object.flight["departure_airport"]["id"]
        arrival_airport = flight_data_object.flight["arrival_airport"]["id"]
        departure_date = flight_data_object.flight_outbound_date
        return_date = flight_data_object.flight_return_date
        flight_link = flight_data_object.google_flight_link
        message = (f"Low Price Alert!!!\n"
                   f"Only ${flight_price} to fly from {departure_airport} to {arrival_airport},"
                   f" on {departure_date} until {return_date}.\n"
                   f"Google flight Link: {flight_link}")
        return message

    def send_message_via_telegram(self, flight_data: FlightData):
        params = {
            "chat_id": self.chat_id,
            "text": self.format_message(flight_data)
        }
        response = requests.post(url=f"https://api.telegram.org/bot{self.telegram_key}/sendMessage", params=params)
        response.raise_for_status()
        print("Message Sent Successfully.")
