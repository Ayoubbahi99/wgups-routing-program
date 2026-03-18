# Student ID: 012114667
# Ayoub El bahi
# Reads the distance CSV and lets me look up miles between any two addresses.
# The address list below has to match the row/column order in distanceCSV.csv exactly.

import csv


ADDRESS_LIST = [
    "4001 South 700 East",                      # 0 - HUB
    "1060 Dalton Ave S",                         # 1
    "1330 2100 S",                               # 2
    "1488 4800 S",                               # 3
    "177 W Price Ave",                           # 4
    "195 W Oakland Ave",                         # 5
    "2010 W 500 S",                              # 6
    "2300 Parkway Blvd",                         # 7
    "233 Canyon Rd",                             # 8
    "2530 S 500 E",                              # 9
    "2600 Taylorsville Blvd",                    # 10
    "2835 Main St",                              # 11
    "300 State St",                              # 12
    "3060 Lester St",                            # 13
    "3148 S 1100 W",                             # 14
    "3365 S 900 W",                              # 15
    "3575 W Valley Central Station bus Loop",    # 16
    "3595 Main St",                              # 17
    "380 W 2880 S",                              # 18
    "410 S State St",                            # 19
    "4300 S 1300 E",                             # 20
    "4580 S 2300 E",                             # 21
    "5025 State St",                             # 22
    "5100 South 2700 West",                      # 23
    "5383 South 900 East #104",                  # 24
    "600 E 900 South",                           # 25
    "6351 South 900 East",                       # 26
]


class DistanceTable:

    def __init__(self, distance_file):
        with open(distance_file) as f:
            self.distances = list(csv.reader(f))

    def get_address_index(self, address):
        # look up the address in the list and return its index
        address = address.strip()
        for i, addr in enumerate(ADDRESS_LIST):
            if addr == address:
                return i
        return None

    def get_distance(self, index1, index2):
        # if either address wasn't found in ADDRESS_LIST show an error
        if index1 is None or index2 is None:
            raise ValueError(
                f"Address not found in ADDRESS_LIST (index1={index1}, index2={index2})"
            )
 
        # the CSV is lower-triangular so some cells are empty
        # this works because distances are the same in both directions
        d = self.distances[index1][index2]
        if d == '':
            d = self.distances[index2][index1]
        return float(d)
