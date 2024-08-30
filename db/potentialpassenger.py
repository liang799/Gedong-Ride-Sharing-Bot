from abc import ABC, abstractmethod
from typing import List

from LatLong import LatLong


class PotentialPassenger:
    def __init__(self, tele_user_id: int, lat_long: LatLong):
        self.telegram_user_id: int = tele_user_id
        self.lat_long: LatLong = lat_long


class PotentialPassengerRepository(ABC):
    @abstractmethod
    def getListOfPassengersWithin(self, lat_long: LatLong) -> List[PotentialPassenger]:
        pass

    @abstractmethod
    def addPassenger(self, passenger: PotentialPassenger):
        pass
