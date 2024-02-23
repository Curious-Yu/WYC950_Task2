import csv
from datetime import datetime, timedelta

from hashtable import ChainingHashTable


# create package object
class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, notes, status):
        if deadline == "EOD":
            _deadline = "5:00 PM"
        else:
            _deadline = deadline
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = datetime.strptime(_deadline, "%I:%M %p").time()
        self.weight = weight
        self.notes = notes
        self.status = status
        self.depart_time = None
        self.delivery_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.id,
            self.address,
            self.city,
            self.state,
            self.zip,
            self.deadline,
            self.weight,
            # self.notes,
            self.status,
            self.depart_time,
            self.delivery_time,
        )

    # def update_status(self, convert_time):
    #     if self.delivery_time < convert_time:
    #         self.status = "Delivered"
    #     elif self.delivery_time > convert_time:
    #         self.status = "En Route"
    #     else:
    #         self.status = "At Hub"


# create load package data
def load_package_data(hashTable):
    with open("excel/package.csv", "r") as package_file:
        package_data = csv.reader(package_file, delimiter=",")
        next(package_data)
        for item in package_data:
            package_id = int(item[0])
            package_address = item[1]
            package_city = item[2]
            package_state = item[3]
            package_zip = item[4]
            package_deadline = item[5]
            package_weight = item[6]
            package_notes = item[7]
            package_status = "At Hub"

            package_value = Package(
                package_id,
                package_address,
                package_city,
                package_state,
                package_zip,
                package_deadline,
                package_weight,
                package_notes,
                package_status,
            )

            hashTable.insert(package_id, package_value)
    return hashTable


# def update_status(convert_time):
#     if package.delivery_time < convert_time:
#         package.status = "Delivered"
#     elif package.delivery_time > convert_time:
#         package.status = "En Route"
#     else:
#         package.status = "At Hub"
# update_status(convert_time)
