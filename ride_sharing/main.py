from ride_sharing.RideSharing import RideSharing
from ride_sharing.helpers import read_file

if __name__ == '__main__':
    # Add file path here to execute the tests
    file_contents = read_file(r"D:\Coding\python\Practice\ride_sharing\data\data2.txt")

    ride_sharing = RideSharing()
    for row in file_contents:
        # remove new line characters
        row = row.replace("\n", "")
        # split the row into command and arguments
        row = row.split(" ")
        # get the command and arguments from the row
        command, args = row[0], row[1:]
        command_result = ride_sharing.run_command(command, *args)
        # print command_result only if not none
        if command_result:
            print(command_result)
