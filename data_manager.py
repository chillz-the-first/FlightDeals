import requests
import os
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.FLIGHTS_URL = os.environ.get("SHEETY_FLIGHTS_ENDPOINT")
        self.USERS_URL = os.environ.get("SHEETY_USERS_ENDPOINT")
        self.SHEETY_KEY = os.getenv("SHEETY_BEARER")
        self.HEADERS = {"Authorization": f"Bearer {self.SHEETY_KEY}"}
        self.destination_data = {}

    def get_sheet_data(self):
        print("Getting sheet data.")
        response = requests.get(url=self.FLIGHTS_URL, headers=self.HEADERS)

        if response.status_code == 200:
            data = response.json()
            self.destination_data = data["prices"]
            return self.destination_data
        else:
            print(f"Error: {response.status_code}")
            return None

    def update_lowest_price(self, row_id, new_price):
        print(f"Updating lowest price to R{new_price}")
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        requests.put(url=f"{self.FLIGHTS_URL}/{row_id}",json=new_data,headers=self.HEADERS)

    def get_customer_emails(self):
        print("Getting customer emails.")
        response = requests.get(url=self.USERS_URL, headers=self.HEADERS)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None

        data = response.json()
        self.destination_data = data["users"]
        return self.destination_data

