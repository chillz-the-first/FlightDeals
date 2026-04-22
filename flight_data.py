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
    """Parse raw API response and return the cheapest FlightData object.
    Returns a FlightData with price='N/A' if no valid flights are found."""
    print("Finding cheapest flight...")
    if data is None or (not data.get("best_flights") and not data.get("other_flights")):
        print("Flight data not found.")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    total_flights = data.get("best_flights", []) + data.get("other_flights", [])

    cheapest_flight = None
    lowest_price = float("inf")

    for flight in total_flights:
        price = flight.get("price")
        if price is None:
            print("Skipping flight with no price.")
            continue

        if price < lowest_price:
            lowest_price = price
            nr_stops = len(flight["flights"]) - 1

            departure_airport = flight["flights"][0]["departure_airport"]["id"]
            destination_airport = flight["flights"][-1]["arrival_airport"]["id"]
            departure_date = (flight["flights"][0]["departure_airport"]["time"]).split(" ")[0]

            cheapest_flight = FlightData(lowest_price, departure_airport, destination_airport, departure_date,
                                         return_date, nr_stops)

            print(f"New lowest price found: R{lowest_price} to {destination_airport}")

    return cheapest_flight if cheapest_flight else FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

