import requests
import os
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.FLIGHTS_URL = os.environ.get("SHEETY_FLIGHTS_ENDPOINT")
        self.USERS_URL = os.environ.get("SHEETY_USERS_ENDPOINT")
        self.HEADERS = {"Authorization": f"Bearer {os.getenv("SHEETY_BEARER")}"}
        self.destination_data = {}

    def get_sheet_data(self):
        print("Fetching destination data from sheet...")
        response = requests.get(url=self.FLIGHTS_URL, headers=self.HEADERS)

        if response.status_code != 200:
            response.raise_for_status()
            return None

        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_lowest_price(self, row_id, new_price):
        print(f"Updating lowest price to R{new_price}")
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        response = requests.put(url=f"{self.FLIGHTS_URL}/{row_id}",json=new_data,headers=self.HEADERS)
        response.raise_for_status()

    def get_customer_emails(self):
        print("Getting customer emails.")
        response = requests.get(url=self.USERS_URL, headers=self.HEADERS)

        if response.status_code != 200:
            response.raise_for_status()
            return None

        self.destination_data = response.json()["prices"]
        return self.destination_data

