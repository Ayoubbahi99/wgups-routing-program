# Student ID: 012114667
# Ayoub El bahi
# Truck class — keeps track of where the truck is, how far it's gone, etc.

class Truck:

    def __init__(self, speed, location, depart_time, packages):

        self.speed            = speed          # Travel speed in miles per hour.
        self.miles            = 0.0            # Accumulated mileage; starts at zero.
        self.current_location = location       # Street address the truck is currently at.
        self.depart_time      = depart_time    # Time the truck officially left the hub.
        self.time             = depart_time    # Running clock; advances as the truck drives.
        self.packages         = packages       # List of package IDs currently on board.
