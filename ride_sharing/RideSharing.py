from typing import Optional

from ride_sharing.constants import BASE_FARE, PER_KM_FARE, PER_MIN_FARE, SERVICE_TAX
from ride_sharing.enums import Commands
from ride_sharing.helpers import get_euclidean_distance, is_command_valid
from ride_sharing.ptypes import Point, Driver, RideInfo, Rider


class RideSharing:
    __riders: [Rider]
    __drivers: [Driver]
    __rides: [RideInfo]
    __rider_driver_matches: dict[str, list]

    def __init__(self):
        self.__rides = []
        self.__riders = []
        self.__drivers = []
        self.__rider_driver_matches = {}

    def get_ride(self, ride_id: str) -> Optional[RideInfo]:
        for ride in self.__rides:
            if ride.id == ride_id:
                return ride

    def get_driver(self, driver_id: str) -> Optional[Driver]:
        for driver in self.__drivers:
            if driver.id == driver_id:
                return driver

    def get_rider(self, rider_id: str) -> Optional[Rider]:
        for rider in self.__riders:
            if rider.id == rider_id:
                return rider

    def __get_rider_driver_matches(self,
                                   rider_point: Point, limit: int = None
                                   ) -> list:
        """Finds the nearest driver to the rider

        Args:
            rider_point (Point): The point of riders
            limit (int, optional): Number of results to return. Defaults to None.

        Returns:
            list: Sorted list of drivers closest to rider point
        """
        distance_between_rider: list[tuple[str, float]] = []
        # find euclidean distance between rider and all drivers
        for driver in self.__drivers:
            if driver.is_available:
                distance = get_euclidean_distance(rider_point, driver.location)
                distance_between_rider.append(
                    (
                        driver.id,
                        distance,
                    )
                )

        # sort according to distance between rider and drivers
        distance_between_rider.sort(key=lambda x: x[1])

        return distance_between_rider[:limit] if limit else distance_between_rider

    def __start_ride(self,
                     ride_id: str,
                     rider_id: str,
                     n: int,
                     ride_matches: list,
                     ):
        """Starts a ride if it exists
        Args:
            ride_id (str): Id of the ride to start
            rider_id (str): Rider for the ride
            n (int): Selected driver for the ride
            ride_matches (list): Total driver matches for the current rider

        Returns:
            str: If ride is already started or added
        """
        if not ride_matches or n > len(ride_matches):
            return "INVALID_RIDE"

        existing_ride = self.get_ride(ride_id)
        if existing_ride:
            return "INVALID_RIDE"

        existing_rider = self.get_rider(rider_id)
        if existing_rider:
            driver_id = ride_matches[n - 1][0]
            self.__rides.append(
                RideInfo(
                    ride_id, rider_id, False, existing_rider.location, driver_id
                )
            )

            # set driver as unavailable
            existing_driver = self.get_driver(driver_id)
            if existing_driver:
                existing_driver.is_available = False

            return f"RIDE_STARTED {ride_id}"

        return "INVALID_RIDE"

    def __stop_ride(self,
                    ride_id: str, destination: Point, time_taken: int,
                    ):
        """Stops a ride for a given ride identifier

        Args:
            ride_id (str): Id of tthe ride to stop
            destination (Point): Destination at which rider stopped
            time_taken (int): Total time taken in minutes for the rider to reach the destination

        Returns:
            str: If ride stopped or not
        """
        if not ride_id:
            return "INVALID_RIDE"

        existing_ride = self.get_ride(ride_id)
        if existing_ride:
            existing_ride.is_completed = True
            existing_ride.time_taken = time_taken
            existing_ride.destination = destination

            # set driver as available
            existing_driver = self.get_driver(existing_ride.driver_id)
            if existing_driver:
                existing_driver.is_available = True

            return f"RIDE_STOPPED {ride_id}"
        return "INVALID_RIDE"

    def __generate_bill(self, ride_id: str, ):
        """Generates bill for the ride

        Args:
            ride_id (str): Id of  the ride to generate bill for

        Returns:
            str: Generated bill data if generated successfully
        """
        for ride in self.__rides:
            if ride.id == ride_id:
                if not ride.is_completed:
                    return "RIDE_NOT_COMPLETED"
                distance_travelled = get_euclidean_distance(ride.destination, ride.source)
                fare = (
                        BASE_FARE
                        + distance_travelled * PER_KM_FARE
                        + ride.time_taken * PER_MIN_FARE
                )
                total_fare = round(fare * (1 + SERVICE_TAX), 2)
                return f"BILL {ride_id} {ride.driver_id} {total_fare}"
        return "INVALID_RIDE"

    def __invoke_command_method(self, command: Commands, *args):
        match command:
            case Commands.ADD_DRIVER:
                self.__drivers.append(Driver(args[0], Point(float(args[1]), float(args[2])), True))
                return
            case Commands.ADD_RIDER:
                self.__riders.append(Rider(args[0], Point(float(args[1]), float(args[2]))))
                return
            case Commands.MATCH:
                for ride in self.__riders:
                    if ride.id == args[0]:
                        driver_matches = self.__get_rider_driver_matches(ride.location)
                        if driver_matches:
                            # save matches with rider id
                            self.__rider_driver_matches[ride.id] = driver_matches
                            return "DRIVERS_MATCHED " + " ".join(
                                [x[0] for x in driver_matches]
                            )
                        else:
                            return "NO_DRIVERS_AVAILABLE"
            case Commands.START_RIDE:
                rider_id = args[2]
                if rider_id in self.__rider_driver_matches:
                    return self.__start_ride(args[0], rider_id, int(args[1]), self.__rider_driver_matches[rider_id])

            case Commands.STOP_RIDE:
                return self.__stop_ride(args[0], Point(float(args[1]), float(args[2])), int(args[3]))

            case Commands.BILL:
                return self.__generate_bill(args[0])

        return "None"

    def run_command(self, command: str, *args):
        """
        Takes and run command with provided arguments
        Args:
            command: String
            *args: List of arguments required by the command

        Returns:
            str: Result of the command
        """
        if is_command_valid(command):
            # TODO invoked command
            invoke_result = self.__invoke_command_method(Commands(command), *args)

            if invoke_result == "None":
                # no command was invoked
                return "INVALID_COMMAND"
            else:
                return invoke_result
        else:
            return "INVALID_COMMAND"
