from datetime import datetime, timedelta
import requests
import os
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.KEY = os.getenv("SERP_KEY")
        self.endpoint = "https://serpapi.com/search?engine=google_flights"

    def check_flights(self, origin_city_code, destination_city_code, departure_date, return_date, is_direct=True):
        print("Checking flights...")
        params = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": departure_date,
            "return_date": return_date,
            "type": "1",
            "adults": "1",
            "currency": "ZAR",
            "stops" : "1",
            "api_key": self.KEY,
        }
        response = requests.get(url=self.endpoint, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None


        if response.json():
            print(f"Getting flights from {origin_city_code} to {destination_city_code}")
            data = response.json()
            if "error" in data:
                print(f"API error: {data['error']}")
                return None
            return data
        else:
            print(f"No direct flights from {origin_city_code} to {destination_city_code}. Looking for indirect flights...")
            is_direct = False
            params["stops"] = "0"
            response = requests.get(url=self.endpoint, params=params)
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                print(response.text)
                return None

            data = response.json()
            if "error" in data:
                print(f"API error: {data['error']}")
                return None
            return data
