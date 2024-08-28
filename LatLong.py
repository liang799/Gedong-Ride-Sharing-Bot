from geopy import distance


class LatLong:
    def __init__(self, lat: float, long: float):
        self.lat = lat
        self.long = long

    def compare_distance_km(self, other_lat_long: 'LatLong'):
        coords_1 = (self.lat, self.long)
        coords_2 = (other_lat_long.lat, other_lat_long.long)
        return distance.geodesic(coords_1, coords_2).km
