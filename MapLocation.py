import re
import requests
from LatLong import LatLong


class MapLocation:
    def __init__(self, google_map_url: str):
        self.url = google_map_url
        r = requests.get(google_map_url)
        raw_location_name = re.search("\/place\/([^\/]+)\/", r.url)
        if raw_location_name is None:
            raise ValueError("Location name not found in the URL")

        self.location_name = re.sub("\+", " ", raw_location_name.group(1).strip())

        pattern = r'@(-?\d+\.\d+),(-?\d+\.\d+)'
        lat_long_match = re.search(pattern, r.url)

        if lat_long_match is None:
            raise ValueError("Lat Long not found in URL")

        latitude = float(lat_long_match.group(1))
        longitude = float(lat_long_match.group(2))

        self.lat_long = LatLong(latitude, longitude)
