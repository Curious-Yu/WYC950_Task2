# import the csv module to work with csv files
import csv

# import datetime and timedelta classes
from datetime import datetime, timedelta

# import the chaining hash table class from hashtable module
from hashtable import ChainingHashTable

# import package class and load package data function from package module
from package import Package, load_package_data

# import load address data function from address module
from address import load_address_data

# import load distance data function from distance module
from distance import load_distance_data


# create truck object
class Truck:
    def __init__(
        self,
        capacity,
        speed,
        load,
        pkgs,
        mileage,
        start_address,
        start_time,
        sorted_pkgs,
    ):
        # initializing Truck object with provided attributes
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.pkgs = pkgs
        self.mileage = mileage
        self.start_address = start_address
        self.start_time = start_time
        self.time = start_time
        self.sorted_pkgs: list[Package] = (
            sorted_pkgs  # assume sorted pkgs is a list of Package objects
        )

    def __str__(self):
        # string representation of Truck object
        return "%s, %s, %s, %s, %s, %s, %s" % (
            self.capacity,
            self.speed,
            self.load,
            self.pkgs,
            self.mileage,
            # self.start_address,
            self.start_time,
            self.time,
            # self.sorted_pkgs,
        )
