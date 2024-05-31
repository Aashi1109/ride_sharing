from typing import Optional


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class RideInfo:
    def __init__(self, id: str, rider_id: str, is_completed: bool, source: Point, driver_id: str,
                 time_taken: Optional[float] = None, destination: Optional[Point] = None):
        self.id = id
        self.rider_id = rider_id
        self.is_completed = is_completed
        self.source = source
        self.driver_id = driver_id
        self.time_taken = time_taken
        self.destination = destination


class User:
    def __init__(self, id: str, location: Point):
        self.id = id
        self.location = location


class Driver(User):
    def __init__(self, id: str, location: Point, is_available: bool):
        super().__init__(id, location)
        self.is_available = is_available


class Rider(User):
    def __init__(self, id: str, location: Point):
        super().__init__(id, location)
