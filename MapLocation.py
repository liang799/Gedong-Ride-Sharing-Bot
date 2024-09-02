from LatLong import LatLong


class MapLocation:
    def __init__(self, url: str, location_name: str, lat_long: LatLong):
        self.url = url
        self.location_name = location_name
        self.lat_long = lat_long
