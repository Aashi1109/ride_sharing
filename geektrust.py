from sys import argv

from src.RideSharing import RideSharing
from src.helpers import read_file


def main(filepath: str):
    file_contents = read_file(filepath)

    src = RideSharing()
    for row in file_contents:
        # remove new line characters
        row = row.replace("\n", "")
        # split the row into command and arguments
        row = row.split(" ")
        # get the command and arguments from the row
        command, args = row[0], row[1:]
        command_result = src.run_command(command, *args)
        # print command_result only if not none
        if command_result:
            print(command_result)


if __name__ == '__main__':
    # Add file path here to execute the tests
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    main(file_path)
