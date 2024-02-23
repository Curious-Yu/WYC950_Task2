import csv


# load the distance
def load_distance_data():
    with open("excel/distance.csv", "r") as distance_file:
        distance_data = csv.reader(distance_file)
        distance_data = list(distance_data)
    return distance_data
