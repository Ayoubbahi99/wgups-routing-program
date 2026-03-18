# Ayoub El bahi
# Student ID: 012114667
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

        # package 9 has a wrong address until 10:20 AM
        if self.ID == 9:
            if current_time > datetime.timedelta(hours=10, minutes=20):
                self.street = "410 S State St"
                self.zip    = "84111"
            else:
                self.street = "300 State St"
                self.zip    = "84103"