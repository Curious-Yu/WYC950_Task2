# Wen Yu Student ID: 001109626

# import the csv module to work with csv file
import csv

# import datetime and timedelta class
from datetime import datetime, timedelta

# import the chaining hash table class from hashtable module
from hashtable import ChainingHashTable

# import Package class and load package data function
from package import Package, load_package_data

# import load address data function
from address import load_address_data

# import load distance data function
from distance import load_distance_data

# import Truck class
from truck import Truck


# set user local time as the current time
current_time = datetime.now()
convert_time = current_time.strftime("%H:%M:%S")

# --package--
# load package data into a hash table
package_hashTable = ChainingHashTable()
load_package_data(package_hashTable)


# --address--
# load address data
address_data = load_address_data()


# function to get the address number
def address_num(address):
    for row in address_data:
        if address in row[1]:
            return int(row[0])


# --distance--
# load distance data
distance_data = load_distance_data()


# function to find distance between two addresses
def distance_between(address_x: int, address_y: int) -> float:
    distance = distance_data[address_x][address_y]
    return float(distance)


# --trucks--
# define trucks and their details
# assign packages to the truck manually
truck1 = Truck(
    16,
    18,
    None,
    [1, 7, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40],
    0.0,
    "4001 South 700 East",
    timedelta(hours=8),
    [],
)
# set start_time to 8am, this truck1 will leave and come back first to drive the next truck, because there are only 2 drivers

truck2 = Truck(
    16,
    18,
    None,
    [3, 5, 8, 9, 10, 11, 12, 17, 18, 22, 23, 24, 36, 38, 39],
    0.0,
    "4001 South 700 East",
    timedelta(hours=10, minutes=20),
    [],
)
# set start_time to 10:20, this truck2 will deliver packages already assigned to it, the package 9 who will change address around 10:20, and deliver packages with deadline to EOD

truck3 = Truck(
    16,
    18,
    None,
    [2, 4, 6, 21, 25, 26, 27, 28, 32, 33, 35],
    0.0,
    "4001 South 700 East",
    timedelta(hours=9, minutes=5),
    [],
)
# set start_time to 9:05, this truck3 will deliver delayed packages that have deadline before 10:30 and other EOD packages


# function to sort packages in each truck based on deadline
def sort_truck(truck: Truck):
    sorted_packages = []
    for item in truck.pkgs:
        pkg_info = package_hashTable.search(item)
        sorted_packages.append(pkg_info)
    sorted_packages = sorted(
        sorted_packages,
        key=lambda pkg: (pkg.deadline,),
    )
    truck.sorted_pkgs = sorted_packages


# sort packages for each truck
for truck in [truck1, truck2, truck3]:
    sort_truck(truck)


# --algorithm--
# speed is 18MPH
# function to deliver packages using nearest neighbor algorithm
def delivery(truck: Truck):
    # update special package 9 address at 10:20 AM based on current time
    if convert_time >= "10:20:00":
        pkg9 = package_hashTable.search(9)
        pkg9.address = "410 S State St"
        pkg9.zip = "84111"
    else:
        pkg9 = package_hashTable.search(9)
        pkg9.address = "300 State St"
        pkg9.zip = "84103"

    address_x = truck.start_address
    loading_list = []
    mileage = 0

    while truck.sorted_pkgs:
        next_distance = 100
        next_package = None
        for pkg in truck.sorted_pkgs:
            distance = distance_between(
                (address_num(address_x) - 1), (address_num(pkg.address) - 1)
            )
            if distance <= next_distance:
                next_distance = distance
                next_package = pkg

        # add the new found package with the nearest distance to the truck
        loading_list.append(next_package.id)
        # add truck number to package
        next_package.truck_num = f"truck: {truck_num}"
        # the new found package address will be the address use to locate the next package
        address_x = next_package.address
        # keep track of the mileage
        mileage += next_distance
        # keep track of time
        time_changed = timedelta(hours=(next_distance / truck.speed))
        truck.time += time_changed
        # update package depart_time
        next_package.depart_time = truck.start_time
        # update package delivery_time
        next_package.delivery_time = truck.time

        # convert delivery_time to the same format as the converted current time
        delivery_time_str = (
            datetime(2024, 1, 1) + next_package.delivery_time
        ).strftime("%H:%M:%S")
        # convert depart_time to the same format as the converted current time
        depart_time_str = (datetime(2024, 1, 1) + next_package.depart_time).strftime(
            "%H:%M:%S"
        )

        # update status based on the current time
        if delivery_time_str <= convert_time:
            next_package.status = "Delivered"
        elif delivery_time_str > convert_time and depart_time_str <= convert_time:
            next_package.status = "En Route"
        else:
            next_package.status = "At Hub"
        # remove the package from the sorted_pkgs
        truck.sorted_pkgs.remove(next_package)
    # update truck mileage
    truck.mileage += mileage
    # update truck load with the sorted list of packages
    truck.load = loading_list


total_mileage = 0.0

# deliver packages for each truck and update total mileage
for index, truck in enumerate([truck1, truck2, truck3]):
    truck_num = index + 1 # using this to add turck number to each package
    delivery(truck)
    # total mileage
    total_mileage += round(truck.mileage, 2)


# --printing--
# function to print all the package status and total Mileage
def print_all_status():
    print("📍 Status report for all trucks with total mileage")
    print("As of now: ", convert_time, " Total Mileage: ", total_mileage)
    for i in range(len(package_hashTable.table) + 1):
        package = package_hashTable.search(i + 1)
        if package:
            if package.status == "Delivered":
                print(
                    "Package ID: ",
                    package.id,
                    package.truck_num,
                    " Address: ",
                    package.address,
                    " Status: ",
                    package.status,
                    " at ",
                    package.delivery_time,
                )
            else:
                print(
                    "Package ID: ",
                    package.id,
                    package.truck_num,
                    " Address: ",
                    package.address,
                    " Status: ",
                    package.status,
                    " Expected delivery at ",
                    package.delivery_time,
                )


# print_all_status()


# function to print single package status with time
def print_single_status(user_input):
    print("📍 Status report for package: ", user_input)
    print("As of now: ", convert_time)
    input = int(user_input)
    package = package_hashTable.search(input)
    if package:
        if package.status == "Delivered":
            print(
                "Package ID: ",
                package.id,
                package.truck_num,
                " Address: ",
                package.address,
                " Status: ",
                package.status,
                " at ",
                package.delivery_time,
            )
        else:
            print(
                "Package ID: ",
                package.id,
                package.truck_num,
                " Address: ",
                package.address,
                " Status: ",
                package.status,
                " Expected delivery at ",
                package.delivery_time,
            )


# print_single_status(user_input=9)


# function to print all the package status with specific time
def print_all_time(input_time):
    # convert input_time to the same format as the converted current time
    input_time_str = input_time.strftime("%H:%M:%S")
    # update special package 9 address at 10:20 AM based on the input time
    if input_time_str >= "10:20:00":
        pkg9 = package_hashTable.search(9)
        pkg9.address = "410 S State St"
        pkg9.zip = "84111"
    else:
        pkg9 = package_hashTable.search(9)
        pkg9.address = "300 State St"
        pkg9.zip = "84103"
    print("📍 Status report for all trucks at ", input_time_str)
    for i in range(len(package_hashTable.table) + 1):
        package = package_hashTable.search(i + 1)
        # # convert delivery_time to the same format as the input time
        delivery_time_str = (datetime(2024, 1, 1) + package.delivery_time).strftime(
            "%H:%M:%S"
        )
        # convert depart_time to the same format as the input time
        depart_time_str = (datetime(2024, 1, 1) + package.depart_time).strftime(
            "%H:%M:%S"
        )
        # update status based on the input time
        if delivery_time_str <= input_time_str:
            package.status = "Delivered"
        elif delivery_time_str > input_time_str and depart_time_str <= input_time_str:
            package.status = "En Route"
        else:
            package.status = "At Hub"
        # print packages
        if package:
            if package.status == "Delivered":
                print(
                    "Package ID: ",
                    package.id,
                    package.truck_num,
                    " Address: ",
                    package.address,
                    " Status: ",
                    package.status,
                    " at ",
                    package.delivery_time,
                )
            else:
                print(
                    "Package ID: ",
                    package.id,
                    package.truck_num,
                    " Address: ",
                    package.address,
                    " Status: ",
                    package.status,
                    " Expected delivery at ",
                    package.delivery_time,
                )


# print_all_time()


# function to print specific package status with specific time
def print_single_time(input_time, pkgID):
    # convert input_time to the same format as the converted current time
    input_time_str = input_time.strftime("%H:%M:%S")
    # convert input package ID into number
    input = int(pkgID)
    # update special package 9 address at 10:20 AM based on input time
    if input_time_str >= "10:20:00":
        pkg9 = package_hashTable.search(9)
        pkg9.address = "410 S State St"
        pkg9.zip = "84111"
    else:
        pkg9 = package_hashTable.search(9)
        pkg9.address = "300 State St"
        pkg9.zip = "84103"
    print("📍 Status report for truck ", input, " at ", input_time_str)
    package = package_hashTable.search(input)  # search for the specific package
    # convert delivery_time to the same format as the input time
    delivery_time_str = (datetime(2024, 1, 1) + package.delivery_time).strftime(
        "%H:%M:%S"
    )
    # convert depart_time to the same format as the input time
    depart_time_str = (datetime(2024, 1, 1) + package.depart_time).strftime("%H:%M:%S")

    # update status based on the input time
    if delivery_time_str <= input_time_str:
        package.status = "Delivered"
    elif delivery_time_str > input_time_str and depart_time_str <= input_time_str:
        package.status = "En Route"
    else:
        package.status = "At Hub"
    # print packages
    if package:
        if package.status == "Delivered":
            print(
                "Package ID: ",
                package.id,
                package.truck_num,
                " Address: ",
                package.address,
                " Status: ",
                package.status,
                " at ",
                package.delivery_time,
            )
        else:
            print(
                "Package ID: ",
                package.id,
                package.truck_num,
                " Address: ",
                package.address,
                " Status: ",
                package.status,
                " Expected delivery at ",
                package.delivery_time,
            )


# print_single_time(input_time, pkgID)


# function to print details for all trucks
def print_all_truck(truck):
    print("📍 Report for all truck details")
    print("As of now: ", convert_time, " Total Mileage: ", total_mileage)
    for index, truck in enumerate([truck1, truck2, truck3], start=1):
        print("Truck ", index, ": ")
        print("Packages delivered in this order: ", truck.load)
        # # convert truck_time to the same format as the converted current time
        truck_time_str = (datetime(2024, 1, 1) + truck.time).strftime("%H:%M:%S")
        # convert start_time to the same format as the converted current time
        start_time_str = (datetime(2024, 1, 1) + truck.start_time).strftime("%H:%M:%S")

        # update status based on the current time
        if truck_time_str <= convert_time:
            print("Departed the hub at: ", truck.start_time)
            print("Delivered all packages at: ", truck.time)
        elif truck_time_str > convert_time and start_time_str <= convert_time:
            print("Departed the hub at: ", truck.start_time)
            print("Expect to deliver all packages by: ", truck.time)
        else:
            print("Expect to leave the hub at: ", truck.start_time)
            print("Expect to deliver all packages by: ", truck.time)


# print_all_truck(truck)


# UI menu with options asking for inputs
def main():
    print("\nWelcome to WGUPS tracking system!")
    while True:
        print("\n---+---+---")

        print("\nMenu\n")

        print("1. print all package status with delivery & total mileage")
        print("2. print a single package status with delivery time")
        print("3. print all package status with specific time")
        print("4. print single package status with specific time")
        print("5. print details for all trucks & total mileage")

        print("9. exit")

        choice = input("\nEnter your choice: ")

        print("\n---+---+---\n")

        if choice == "1":
            print_all_status()

        elif choice == "2":
            user_input = input("enter the package ID (between 1 - 40): ")
            print_single_status(user_input)

        elif choice == "3":
            user_input = input("enter the time (HH:MM:SS only): ")

            while True:
                # user_input = input("enter the time (HH:MM:SS only): ")
                try:
                    # user_input = input("enter the time (HH:MM:SS only): ")
                    input_time = datetime.strptime(user_input, "%H:%M:%S")
                    print_all_time(input_time)
                except ValueError:
                    print("Invalid input format! Try again.")
                break

        elif choice == "4":
            user_input = input("enter the time (HH:MM:SS only): ")
            pkgID = input("enter the package ID (between 1 - 40):")

            while True:
                # user_input = input("enter the time (HH:MM:SS only): ")
                try:
                    # user_input = input("enter the time (HH:MM:SS only): ")
                    input_time = datetime.strptime(user_input, "%H:%M:%S")
                    print_single_time(input_time, pkgID)
                except ValueError:
                    print("Invalid input format! Try again.")
                break

        elif choice == "5":
            print_all_truck(truck)

        elif choice == "9":
            print("Exiting the tracking system...")
            break


main()
