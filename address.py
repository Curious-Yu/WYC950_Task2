import csv


# load the address data
def load_address_data():
    with open("excel/address.csv", "r") as address_file:
        address_data = csv.reader(address_file)
        address_data = list(address_data)
    return address_data
