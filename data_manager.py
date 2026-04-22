import requests
import os
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.GET_URL = "https://api.sheety.co/836e7029d2380b3f3c6e9ca0eb7f38b8/flightDeals/prices/"
        self.PUT_URL = "https://api.sheety.co/836e7029d2380b3f3c6e9ca0eb7f38b8/flightDeals/prices/"
        self.SHEETY_KEY = os.getenv("SHEETY_BEARER")
        self.HEADERS = {"Authorization": f"Bearer {self.SHEETY_KEY}"}
        self.destination_data = {}

    def get_sheet_data(self):
        print("Getting sheet data.")
        response = requests.get(url=self.GET_URL, headers=self.HEADERS)

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
        requests.put(url=f"{self.PUT_URL}/{row_id}",json=new_data,headers=self.HEADERS)
