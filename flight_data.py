class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

def find_cheapest_flight(data, return_date):
    print("Finding cheapest flight...")
    if data is None or (not data.get("best_flights") and not data.get("other_flights")):
        print("Flight data not found.")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    total_flights = data.get("best_flights", []) + data.get("other_flights", [])

    # total_flights.sort(key=lambda x: x["price"])

    flight = total_flights[0]
    lowest_price = flight["price"]
    departure_airport = flight["flights"][0]["departure_airport"]["id"]
    departure_date = (flight["flights"][-1]["departure_airport"]["time"]).split(" ")[0]
    destination_airport = flight["flights"][0]["arrival_airport"]["id"]
    nr_stops = len(flight["flights"]) - 1

    cheapest_flight = FlightData(lowest_price, departure_airport, destination_airport, departure_date, return_date, nr_stops)

    for fly in total_flights:
        try:
            price = fly["price"]
        except KeyError:
            print("--- No price available for flight. ---")
            continue
        if price < lowest_price:
            lowest_price = price
            departure_airport = fly["flights"][0]["departure_airport"]["id"]
            departure_date = (fly["flights"][0]["departure_airport"]["time"]).split(" ")[0]
            destination_airport = fly["flights"][-1]["arrival_airport"]["id"]
            cheapest_flight = FlightData(lowest_price, departure_airport, destination_airport, departure_date,
                                         return_date, nr_stops)
            nr_stops = len(fly["flights"]) - 1
            print(f"Lowest price to {destination_airport} is R{lowest_price}")

    return cheapest_flight

