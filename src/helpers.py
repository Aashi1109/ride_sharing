from src.enums import Commands
from src.ptypes import Point


def is_command_valid(command: str) -> bool:
    """Checks if the entered command is valid or not

    Args:
        command (str): command to check

    Returns:
        bool: Is command valid or not
    """
    return Commands.has_command(command)


def get_euclidean_distance(point1: Point, point2: Point) -> float:
    """Calculates the euclidean distance between two points

    Args:
        point1 (Point): Coordinates of point 1
        point2 (Point): Coordinates of point 2

    Returns:
        float: Calculated distance between point 1 and point 2
    """
    return round(((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5, 2)


def read_file(filepath):
    with open(filepath, 'r') as f:
        contents = f.readlines()
    return contents
