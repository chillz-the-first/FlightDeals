#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests_cache
from dotenv import load_dotenv
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta
import flight_data
from pprint import pprint

load_dotenv()   # Load environment variables from the .env file (if present)

requests_cache.install_cache(
    'flight_cache',              # The name of the local file it creates
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    }
)
ORIGIN_CITY_CODE = "CPT"
DEPARTURE_DATE = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
RETURN_DATE  = (datetime.today() + timedelta(weeks=24)).strftime("%Y-%m-%d")


data_manager = DataManager()
search = FlightSearch()
message = NotificationManager()
users = data_manager.get_customer_emails()
# pprint(users)

sheet_data = data_manager.get_sheet_data()
for i in sheet_data:
    print(f"Checking prices for {i["city"]}({i["iataCode"]})")
    destination_city_code = i["iataCode"]
    flight = search.check_flights(ORIGIN_CITY_CODE, destination_city_code, DEPARTURE_DATE, RETURN_DATE)
    # print(f"Getting flights from {origin_city_code} to {destination_city_code}")
    cheapest_flight = flight_data.find_cheapest_flight(flight, RETURN_DATE)
    # pprint(f"{sheet_data[0]['city']}: R {cheapest_flight.price}")

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {i["city"]}({i["iataCode"]}). Looking for indirect flights...")
        stopover = search.check_flights(ORIGIN_CITY_CODE, destination_city_code, DEPARTURE_DATE, RETURN_DATE, False)

        cheapest_flight = flight_data.find_cheapest_flight(stopover, RETURN_DATE)

    if cheapest_flight.price != "N/A" and cheapest_flight.price < sheet_data[0]["lowestPrice"]:
        pprint(f"Lower price flight found to {sheet_data[0]['city']}!")
        data_manager.update_lowest_price(sheet_data[0]["id"], cheapest_flight.price)
        message.send_notification(cheapest_flight)
        message.send_emails(cheapest_flight, users)
