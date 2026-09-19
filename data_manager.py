class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self, endpoint, token):
        self.sheety_endpoint = endpoint
        self.sheety_headers = {"Authorization": token}

    def get_city_from_missing_IATA_records(self, session):
        """Goes through the google sheet then returns the (row_id, city) of the missing IATA codes"""
        response = session.get(url=self.sheety_endpoint, headers=self.sheety_headers)
        data = response.json()["prices"]

        rows_to_be_edited = []
        for row_index in data:
            if row_index["iataCode"] == '':
                rows_to_be_edited.append([row_index["id"], row_index["city"]])

        return rows_to_be_edited

    def set_the_missing_IATA_codes(self, session, row_id, iata_code):
        response = session.put(url=f"{self.sheety_endpoint}/{row_id}", headers=self.sheety_headers, json={"price": {"iataCode": iata_code}})
        print(response.text)
