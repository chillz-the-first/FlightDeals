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

# Cache all API responses for 1 hour, but never cache Sheety (sheet data must always be fresh)
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
sheet_data = data_manager.get_sheet_data()

for destination in sheet_data:
    city = destination["city"]
    iata = destination["iataCode"]
    lowest_price = destination["lowestPrice"]
    row_id = destination["id"]

    print(f"Checking prices for {city}({iata})")

    # First try direct flights
    flight_results = search.check_flights(ORIGIN_CITY_CODE, iata, DEPARTURE_DATE, RETURN_DATE)
    cheapest_flight = flight_data.find_cheapest_flight(flight_results, RETURN_DATE)

    # If no direct flight found, fall back to flights with stopovers
    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {city}({iata}). Looking for indirect flights...")
        stopover = search.check_flights(ORIGIN_CITY_CODE, iata, DEPARTURE_DATE, RETURN_DATE, False)
        cheapest_flight = flight_data.find_cheapest_flight(stopover, RETURN_DATE)

    if cheapest_flight.price != "N/A" and cheapest_flight.price < lowest_price:
        pprint(f"🎉 Deal found! R{cheapest_flight.price} to {city} (sheet lowest: R{lowest_price})")
        data_manager.update_lowest_price(row_id, cheapest_flight.price)
        message.send_notification(cheapest_flight)
        message.send_emails(cheapest_flight, users)
    else:
        print(f"No deal found. Cheapest: R{cheapest_flight.price} | Sheet lowest: R{lowest_price}")
