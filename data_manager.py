from flight_search import FlightSearch

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self, endpoint, token, session, flight_search : FlightSearch):
        self.sheety_endpoint = endpoint
        self.sheety_headers = {"Authorization": token}
        self.session = session
        self.flight_search_data = flight_search

    def update_the_sheet_if_data_ismissing(self):
        """If there are missing data in the google sheet specifally IATA codes then update it using flight_search class"""
        # get the missing city and the row id from the row that are missing the IATA codes
        sheet_data = self.get_city_from_missing_IATA_records()
        # go through the missing city data and get the IATA codes from the serp_api flight autocomplete engine
        for item in sheet_data:
            airport_name = item[1]
            flight_search_results = self.flight_search_data.get_iata_codes(airport_name)
            airport_iata_code = flight_search_results["suggestions"][0]["airports"][0]["id"]
            item.append(airport_iata_code)
            self.set_the_missing_IATA_codes(str(item[0]), airport_iata_code)


    def get_city_from_missing_IATA_records(self):
        """Goes through the google sheet then returns the (row_id, city) of the missing IATA codes"""
        response = self.session.get(url=self.sheety_endpoint, headers=self.sheety_headers)
        data = response.json()["prices"]

        rows_to_be_edited = []
        for row_index in data:
            if row_index["iataCode"] == '':
                rows_to_be_edited.append([row_index["id"], row_index["city"]])

        return rows_to_be_edited

    def set_the_missing_IATA_codes(self, row_id, iata_code):
        """Updating the sheet with the missing IATA codes"""
        response = self.session.put(url=f"{self.sheety_endpoint}/{row_id}", headers=self.sheety_headers, json={"price": {"iataCode": iata_code}})
        print(response.text)


    def return_completed_sheet_data(self):
        """Return all the sheet data fromated by city, iatacode and price"""
        response = self.session.get(url=self.sheety_endpoint, headers=self.sheety_headers)
        data = response.json()["prices"]
        sheet_data = []
        for item in data:
            sheet_data.append([item['city'], item['iataCode'], item['lowestPrice']])
        return sheet_data
