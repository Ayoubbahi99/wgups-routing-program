# Student ID: 012114667
# Ayoub El bahi
# Holds all the info for a single delivery package.
import datetime


class Package:

    def __init__(self, ID, street, city, state, zip_code, deadline, weight, notes):
        self.ID           = ID
        self.street       = street
        self.city         = city
        self.state        = state
        self.zip          = zip_code
        self.deadline     = deadline
        self.weight       = weight
        self.notes        = notes
        self.status       = "At Hub"
        self.departureTime = None
        self.deliveryTime  = None
        self.truckID       = None

    def update_status(self, current_time):
        # figure out what the status should be at the given time
        if self.deliveryTime is None:
            self.status = "At Hub"
        elif current_time < self.departureTime:
            self.status = "At Hub"
        elif current_time < self.deliveryTime:
            self.status = "En route"
        else:
            self.status = "Delivered"

    def get_display_address(self, current_time):
        # package 9 has a wrong address on file until 10:20 AM
        # return the correct address for the given time without mutating self.street
        if self.ID == 9:
            if current_time >= datetime.timedelta(hours=10, minutes=20):
                return "410 S State St", "84111"
            else:
                return "300 State St", "84103"
        return self.street, self.zip