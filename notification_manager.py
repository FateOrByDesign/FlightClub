import requests
from flight_data import FlightData

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self, flight_data: FlightData, telegram_key, chat_id):
        self.flight_data_object = flight_data
        self.telegram_key = telegram_key
        self.chat_id = chat_id

    def format_message(self):
        flight_price = self.flight_data_object.flights["price"]
        departure_airport = self.flight_data_object.flights["departure_airport"]["id"]
        arrival_airport = self.flight_data_object.flights["arrival_airport"]["id"]
        departure_date = self.flight_data_object.flight_outbound_date
        return_date = self.flight_data_object.flight_return_date
        flight_link = self.flight_data_object.google_flight_link
        message = (f"Low Price Alert!!!\n"
                   f"Only ${flight_price} to fly from {departure_airport} to {arrival_airport},"
                   f" on {departure_date} until {return_date}.\n"
                   f"Google flight Link: {flight_link}")
        return message

    def send_message_via_telegram(self):
        params = {
            "chat_id": self.chat_id,
            "text": self.format_message()
        }
        response = requests.post(url=f"https://api.telegram.org/bot{self.telegram_key}/sendMessage", params=params)
        response.raise_for_status()
        print("Message Sent Successfully.")
