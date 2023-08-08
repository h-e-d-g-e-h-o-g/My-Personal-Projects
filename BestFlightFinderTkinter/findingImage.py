import requests
from pprint import pprint
class CityImage:
    def __init__(self, destination_city):
        self.city = destination_city
        self.api_endpoint = "https://api.unsplash.com/search/photos"
        self.header = {
            "Authorization": "Client-ID d5BSTQEp21XfRRq10WyHQlWLXheZ_RjU8OcV_WepfV4"
        }

    def make_request(self):
        params_city = {
            "query": self.city,
            "fit": "crop",
            "w": 520,
            "h": 320,
            "page": 1,
            "per_page": 1,
            "order_by": "popular"
        }
        response = requests.get(url=self.api_endpoint, params=params_city, headers=self.header)
        data = response.json()
        image_url = data["results"][0]["urls"]["regular"]
        return image_url

    def get_tourist_images(self):
        params_tourist = {
            "query": self.city,
            "page": 1,
            "per_page": 8,
            "order_by": "popular"
        }
        response_tourist = requests.get(url=self.api_endpoint, params=params_tourist, headers=self.header)
        data_tourism = response_tourist.json()
        image_urls = []
        for result in data_tourism["results"]:
            image_urls.append(result["urls"]["thumb"])

        return image_urls