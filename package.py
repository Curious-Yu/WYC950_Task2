# import the csv module to work with csv files
import csv

# import datetime and timedelta classes
from datetime import datetime, timedelta

# import the chaining hash table class from hashtable module
from hashtable import ChainingHashTable


# create package object
class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, notes, status):
        # convert deadline EOD to standard time format
        if deadline == "EOD":
            _deadline = "5:00 PM"
        else:
            _deadline = deadline
        # initialize Package object with provided attributes
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = datetime.strptime(
            _deadline, "%I:%M %p"
        ).time()  # convert deadline string to time object
        self.weight = weight
        self.notes = notes
        self.status = status
        self.depart_time = None
        self.delivery_time = None

    def __str__(self):
        # string representation of Package object
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
            self.truck_num,
        )


# create load package data
def load_package_data(hashTable):
    with open("excel/package.csv", "r") as package_file:
        package_data = csv.reader(package_file, delimiter=",")
        next(package_data)
        for item in package_data:
            # extracting package data from csv
            package_id = int(item[0])
            package_address = item[1]
            package_city = item[2]
            package_state = item[3]
            package_zip = item[4]
            package_deadline = item[5]
            package_weight = item[6]
            package_notes = item[7]
            package_status = "At Hub"

            # creating Package object
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
            # insert Package object into the hash table
            hashTable.insert(package_id, package_value)
    return hashTable
