import datetime

import requests

# tequila.kiwi.com
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
TEQUILA_API_KEY = ""  # Type your api key
CURRENCY = "GBP"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self, flay_from: str, flay_to: str):
        self.tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        self.TOMORROW_DATE = self.tomorrow.strftime("%d/%m/%Y")
        self.NEXT_6_MONTH_DATE = (self.tomorrow + datetime.timedelta(180)).strftime("%d/%m/%Y")
        self.FLAY_FROM = flay_from
        self.FLAY_TO = flay_to
        self.parameters = None
        self.headers = None
        self.stop_overs = 0
        self.via_city = ""
        self.data = self.get_data()
        self.departure_airport_IATA = self.data["flyFrom"]
        self.destination_airport_IATA = self.data["flyTo"]
        self.date_flight_departure = self.data['utc_departure'].split("T")[0]

    def get_data(self):
        self.parameters = {
            "fly_from": self.FLAY_FROM,
            "fly_to": self.FLAY_TO,
            "dateFrom": self.TOMORROW_DATE,
            "dateTo": self.NEXT_6_MONTH_DATE,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": CURRENCY,
        }
        self.headers = {
            "apikey": TEQUILA_API_KEY,
            "Content-Encoding": "gzip",
            "Content-Type": "application/json",
        }
        response = requests.get(url=TEQUILA_ENDPOINT, params=self.parameters, headers=self.headers)
        try:
            data = response.json()["data"][0]
            return data
        except IndexError:
            print(f"No flight Found to {self.FLAY_TO}")
            self.parameters = {
                "fly_from": self.FLAY_FROM,
                "fly_to": self.FLAY_TO,
                "dateFrom": self.TOMORROW_DATE,
                "dateTo": self.NEXT_6_MONTH_DATE,
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "flight_type": "round",
                "one_for_city": 1,
                "max_stopovers": 2,
                "curr": CURRENCY,
            }
            response = requests.get(url=TEQUILA_ENDPOINT, params=self.parameters, headers=self.headers)
            data = response.json()["data"]
            if data:
                self.stop_overs = 1
                self.via_city = data[0]['route'][0]['cityTo']
                return data[0]

    def get_price(self):
        price = self.data["conversion"]["GBP"]
        return price
