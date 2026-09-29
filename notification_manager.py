import requests
from flight_data import FlightData

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self, telegram_key, chat_id, sender_email, departure):
        self.telegram_key = telegram_key
        self.chat_id = chat_id
        self.departure = departure
        self.senders_email = sender_email

    def _format_message(self, flight_data_object,destination_city):
        flight_price = flight_data_object.flight["price"]
        stops = flight_data_object.stops
        num_of_stops_per_flight = "Direct" if  stops == 0 else ("1 stop" if stops == 1 else f"{stops} stops")
        arrival_airport = flight_data_object.flight["arrival_airport"]["id"]
        departure_date = flight_data_object.flight_outbound_date
        return_date = flight_data_object.flight_return_date
        flight_link = flight_data_object.google_flight_link
        message = (f"Low Price Alert!\n\n"
                   f"{self.departure} -> {destination_city} ({arrival_airport})\n"
                   f"${flight_price} | {num_of_stops_per_flight}\n"
                   f"Outbound: {departure_date}\n"
                   f"Return: {return_date}\n\n"
                   f"Google flight Link: {flight_link}")
        return message

    def send_message_via_telegram(self, flight_data: FlightData, destination_city):
        params = {
            "chat_id": self.chat_id,
            "text": self._format_message(flight_data, destination_city)
        }
        response = requests.post(url=f"https://api.telegram.org/bot{self.telegram_key}/sendMessage", params=params)
        response.raise_for_status()
        print("Message Sent Successfully.\n\n")


    def send_email(self,connection, flight_data: FlightData, departure_city, destination_city, email_address):
        connection.sendmail(
                from_addr=self.senders_email,
                to_addrs=email_address,
                msg=f"Subject:Flight deal: {departure_city} to {destination_city} for ${flight_data.flight["price"]}\n\n"
                    f"Hi,\n"
                    f"{self._format_message(flight_data,destination_city)}\n"
                    f"Happy travels,\nFlight Club"
            )