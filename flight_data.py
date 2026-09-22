class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, cheapest_flight_options, lowest_expected_price):
        self.flight_outbound_date = cheapest_flight_options["start_date"]
        self.flight_return_date = cheapest_flight_options["end_date"]
        self.google_flight_link = cheapest_flight_options["google_flights_link"]
        self.flights = cheapest_flight_options["flights"]
        self.price_to_compare = lowest_expected_price

    def get_the_cheapest_flight(self):
        """Get the cheapest option out of the returned list"""
        for flight in self.flights:
            if flight.get("cheapest_flight"):
                self.flights = flight
                return flight
        return None

    def compare_with_expected_price(self):
        """Compare with the expected price if it's lower then, returns true"""
        flight_details = self.get_the_cheapest_flight()
        if flight_details:
            return  flight_details["price"] <= self.price_to_compare