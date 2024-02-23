import csv  # import csv module to work with csv files


# function to load address data from csv file
def load_address_data():
    # open the address csv file in read mode
    with open("excel/address.csv", "r") as address_file:
        # use csv reader to read the content of the csv file
        address_data = csv.reader(address_file)
        # converting the csv data into a list
        address_data = list(address_data)
    # return the loaded address data
    return address_data
