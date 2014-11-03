import sys
from operator import itemgetter
import matplotlib.pyplot as plt


def i(name):
    """Convert a cars.csv file name to an index."""
    if name == "model":
        return 0
    elif name == "mpg":
        return 1
    elif name == "cylinders":
        return 2
    elif name == "horsepower":
        return 3
    elif name == "weight":
        return 4
    elif name == "year":
        return 5
    elif name == "origin":
        return 6


def s(sides):
    """
    Return the symbol for an n-dimensional polygon in matplotlib.
    3 triangle  "^"
    4 square    "s"
    5 pentagon  "p"
    6 hexagon   "h"/"H"
    7 octagon   "8"
    """
    if sides == 3:
        return "^"
    elif sides == 4:
        return "s"
    elif sides == 5:
        return "p"
    elif sides == 6:
        return "h"
    elif sides == 7:
        return "8"
    else:
        return "o"


def read_file(file):
    """Reads the car.csv file and returns a list of tuples with the appropriate
    types.
    """
    firstline = True
    for line in file:
        if firstline:
            firstline = False
            continue

        point = line.strip().split(",")
        yield (point[0],
               float(point[1]),
               int(point[2]),
               int(point[3]),
               int(point[4]),
               1900 + int(point[5]),
               point[6])


def split_by(data, index):
    """Split the data into a dictionary by the given field."""
    sets = {}
    for point in data:
        if point[index] in sets:
            sets[point[index]].append(point)
        else:
            sets[point[index]] = [point]
    return sets


def sort_by(data, index):
    """Return the data sorted by a given field."""
    return sorted(data, key=itemgetter(index))


def min_max(points, index):
    """Calculate the minimum and maximum for a given field."""
    min = 99999999999
    max = 0
    for point in points:
        if point[index] > max:
            max = point[index]
        if point[index] < min:
            min = point[index]
    return min, max


if __name__ == "__main__":
    data_points = read_file(open("data/cars.csv"))

    sorted_points = sort_by(data_points, i("year"))
    by_origin = split_by(sorted_points, i("origin"))

    multiple_graphs = True


    window = 1
    for origin, points in by_origin.iteritems():
        if multiple_graphs:
            plt.subplot(3, 1, window)
            plt.title(origin)
        plt.axis([1962, 1983, 35, 240])

        if window == 2:
            plt.plot([0], [0], "s",
                    color=".5",
                    markersize=16,
                    label="5000 lbs")
            plt.plot([0], [0], "s",
                    color=".5",
                    markersize=4,
                    label="1600 lbs")
            plt.plot([0], [0], "s",
                    color="0",
                    label="9 Mile/Gallon")
            plt.plot([0], [0], "s",
                    color="1",
                    label="50 Mile/Gallon")
        elif window == 1:
            plt.plot([0], [0], "^",
                    color="0.5",
                    label="Three cylinders")
            plt.plot([0], [0], "s",
                    color="0.5",
                    label="Four cylinders")
            plt.plot([0], [0], "p",
                    color="0.5",
                    label="Five cylinders")
            plt.plot([0], [0], "h",
                    color="0.5",
                    label="Six cylinders")
            plt.plot([0], [0], "8",
                    color="0.5",
                    label="Eight cylinders")
        legend = plt.legend(loc="upper left", numpoints=1, frameon=False)

        plt.ylabel("Horsepower")

        window += 1
        for point in points:
            year = point[i("year")]
            hors = point[i("horsepower")]
            cyli = point[i("cylinders")]
            wght = point[i("weight")]
            mipg = point[i("mpg")]
            plt.plot([year], [hors],
                    s(cyli),
                    color=str((mipg-9)/41),
                    markersize=wght/400)

    plt.xlabel("Year")
    plt.show()
