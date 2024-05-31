import unittest

from src.RideSharing import RideSharing


class RideSharingTest(unittest.TestCase):
    def test_get_driver(self):
        _rs_obj = RideSharing()
        _rs_obj.run_command("ADD_DRIVER", "D1", "0", "1")
        self.assertIsNotNone(_rs_obj.get_driver("D1"), "Driver not found")

    def test_get_rider(self):
        _rs_obj = RideSharing()
        _rs_obj.run_command("ADD_RIDER", "R1", "0", "1")
        self.assertIsNotNone(_rs_obj.get_rider("R1"), "Rider not found")

    def test_get_ride(self):
        _rs_obj = RideSharing()
        _rs_obj.run_command("ADD_DRIVER", "D1", "0", "1")
        _rs_obj.run_command("ADD_RIDER", "R1", "0", "1")
        _rs_obj.run_command("MATCH", "R1")
        _rs_obj.run_command("START_RIDE", "RIDE-101", "1", "R1")
        self.assertIsNotNone(_rs_obj.get_ride("RIDE-101"), "Ride not found")

    def test_command_valid(self):
        _rs_obj = RideSharing()
        result = _rs_obj.run_command("SOME_RANDOM_COMMAND")
        self.assertEqual(result, "INVALID_COMMAND", "None")

    def test_ride_start_to_end(self):
        _rs_obj = RideSharing()
        _rs_obj.run_command("ADD_DRIVER", "D1", "2", "1")
        _rs_obj.run_command("ADD_DRIVER", "D2", "3", "5")
        _rs_obj.run_command("ADD_DRIVER", "D4", "4", "4")
        _rs_obj.run_command("ADD_DRIVER", "D5", "5", "4")
        _rs_obj.run_command("ADD_DRIVER", "D6", "6", "3")
        _rs_obj.run_command("ADD_DRIVER", "D7", "7", "2")
        _rs_obj.run_command("ADD_RIDER", "R1", "5", "5")
        _rs_obj.run_command("ADD_RIDER", "R2", "0", "1")
        matches_R2 = _rs_obj.run_command("MATCH", "R2")

        self.assertEqual(matches_R2, "DRIVERS_MATCHED D1 D2 D4")

        _rs_obj.run_command("START_RIDE", "RIDE-101", "1", "R2")

        # now driver D1 should be unavailable till the end of ride
        driver_D1 = _rs_obj.get_driver("D1")

        self.assertEqual(driver_D1.is_available, False, "Driver D1 should be unavailable")

        # driver D2 should be unavailable for other riders in their matches
        matches_R1 = _rs_obj.run_command("MATCH", "R1")
        self.assertEqual(matches_R1, "DRIVERS_MATCHED D5 D4 D2 D6 D7",
                         "Driver D1 should be unavailable for new matches")

        # bill generation should be unavailable for current ride
        bill = _rs_obj.run_command("BILL", "RIDE-101")
        self.assertEqual(bill, "RIDE_NOT_COMPLETED", "Bill generation should be unavailable for current ride")

        _rs_obj.run_command("STOP_RIDE", "RIDE-101", "6", "7", "32")

        # bill generation should be unavailable for current ride
        bill = _rs_obj.run_command("BILL", "RIDE-101")
        self.assertEqual(bill, "BILL RIDE-101 D1 203.02", "Bill should be generated for current ride")

        # driver D1 should be available now
        matches_R1 = _rs_obj.run_command("MATCH", "R1")
        self.assertEqual(matches_R1, "DRIVERS_MATCHED D5 D4 D2 D6 D7 D1",
                         "Driver D1 should be available for new matches")


if __name__ == '__main__':
    unittest.main()
