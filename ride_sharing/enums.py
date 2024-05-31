from enum import Enum


class Commands(Enum):
    ADD_DRIVER = "ADD_DRIVER"
    ADD_RIDER = "ADD_RIDER"
    MATCH = "MATCH"
    START_RIDE = "START_RIDE"
    STOP_RIDE = "STOP_RIDE"
    BILL = "BILL"

    @classmethod
    def has_command(cls, value):
        return any(value == item.value for item in cls)
