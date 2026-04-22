from datetime import datetime, timedelta
import requests
import os
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.KEY = os.getenv("SERP_KEY")
        self.endpoint = os.getenv("SERP_ENDPOINT")

    def check_flights(self, origin_city_code, destination_city_code, departure_date, return_date, is_direct=True):
        """
        Search for flights and return raw JSON, or None on failure.
        is_direct=True adds stops=1 (direct only) to the query.
        """
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
        if is_direct:
            params["stops"] = "1"

        print(f"  Searching {'direct' if is_direct else 'indirect'} flights: {origin_city_code} → {destination_city_code}")

        try:
            response = requests.get(url=self.endpoint, params=params)
            response.raise_for_status()     # Raises HTTPError for 4xx/5xx responses
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

        data = response.json()
        if "error" in data:
            print(f"API error: {data['error']}")
            return None
        return data
