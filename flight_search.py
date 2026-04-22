from datetime import datetime, timedelta
import requests
import os
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.KEY = os.getenv("SERP_KEY")
        self.endpoint = "https://serpapi.com/search?engine=google_flights"

    def check_flights(self, origin_city_code, destination_city_code, departure_date, return_date):
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
            "api_key": self.KEY,
        }
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