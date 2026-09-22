class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self, api_key, api_endpoint, session):
        self.serpApi_key = api_key
        self.serpApi_endpoint = api_endpoint
        self.session = session
        self.departure_airport_iata_code = "CMB"

    def get_iata_codes(self, city):
        """Get the IATA code from flight search api given the city as the query"""
        query_params = {
            "engine": "google_flights_autocomplete",
            "api_key": self.serpApi_key,
            "q": city
        }
        response = self.session.get(url=self.serpApi_endpoint, params=query_params)
        return response.json()

    def get_flights_within_next_six_months(self, airport_iata):
        """Returns the flight details of the cheapest flight found for the given parameters"""
        query_params = {
            "engine": "google_travel_explore",
            "api_key": self.serpApi_key,
            "departure_id": self.departure_airport_iata_code,
            "arrival_id": airport_iata,
            "travel_mode": 1
        }
        response = self.session.get(url=self.serpApi_endpoint, params=query_params)
        return response.json()

