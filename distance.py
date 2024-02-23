import csv  # import csv model to work with csv files


# function to load distance data from csv file
def load_distance_data():
    # open the distance csv file in read mode
    with open("excel/distance.csv", "r") as distance_file:
        # use csv reader to read the content of the csv file
        distance_data = csv.reader(distance_file)
        # convert the csv data into a list
        distance_data = list(distance_data)
    # return the loaded distance data
    return distance_data
