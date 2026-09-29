import requests

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self, api_key, api_endpoint, departure_airport_iata_code):
        self.serpApi_key = api_key
        self.serpApi_endpoint = api_endpoint
        self.departure_airport_iata_code = departure_airport_iata_code

    def get_iata_codes(self, city):
        """Get the IATA code from flight search api given the city as the query"""
        query_params = {
            "engine": "google_flights_autocomplete",
            "api_key": self.serpApi_key,
            "q": city,
            "exclude_regions" : True
        }
        response = requests.get(url=self.serpApi_endpoint, params=query_params)
        response.raise_for_status()
        data = response.json()
        if data.get("suggestions"):
            return data
        return None

    def get_flights_within_next_six_months(self, airport_iata, is_direct = True)-> dict|None:
        """Returns the flight details of the cheapest flight found for the given parameters"""
        if is_direct:
            num_of_stops = 1
        else:
            num_of_stops = 3

        query_params = {
            "engine": "google_travel_explore",
            "api_key": self.serpApi_key,
            "departure_id": self.departure_airport_iata_code,
            "arrival_id": airport_iata,
            "travel_mode": 1,
            "currency": "USD",
            "stops": num_of_stops
        }
        response = requests.get(url=self.serpApi_endpoint, params=query_params)
        response.raise_for_status()
        flight_search_data = response.json()

        if not flight_search_data.get("flights"):
            return None
        return flight_search_data


