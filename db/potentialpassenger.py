from abc import ABC, abstractmethod
from typing import List

from LatLong import LatLong
from MapLocation import MapLocation


class PotentialPassenger:
    def __init__(self, tele_user_id: int, location: MapLocation):
        self.telegram_user_id: int = tele_user_id
        self.location = location


class PotentialPassengerRepository(ABC):
    @abstractmethod
    def getListOfPassengersWithin(self, lat_long: LatLong) -> List[PotentialPassenger]:
        pass

    @abstractmethod
    def addPassenger(self, passenger: PotentialPassenger):
        pass
