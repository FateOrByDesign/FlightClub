class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self, api_key, api_endpoint):
        self.serpApi_key = api_key
        self.serpApi_endpoint = api_endpoint

    def get_iata_codes(self,session, city):
        query_params = {
            "engine": "google_flights_autocomplete",
            "api_key": self.serpApi_key,
            "q": city
        }

        response = session.get(url=self.serpApi_endpoint, params=query_params)
        return response.json()
