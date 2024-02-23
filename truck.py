import csv

from datetime import datetime, timedelta

from hashtable import ChainingHashTable
from package import Package, load_package_data
from address import load_address_data
from distance import load_distance_data


from rich import print

# delete before submit the assign -  this is only for readability


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
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.pkgs = pkgs
        self.mileage = mileage
        self.start_address = start_address
        self.start_time = start_time
        self.time = start_time
        self.sorted_pkgs: list[Package] = sorted_pkgs

    def __str__(self):
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
