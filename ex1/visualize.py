import sys
from operator import itemgetter
import matplotlib.pyplot as plt


def i(name):
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


def read_file(file):
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
    sets = {}
    for point in data:
        if point[index] in sets:
            sets[point[index]].append(point)
        else:
            sets[point[index]] = [point]
    return sets


def sort_by(data, index):
    return sorted(data, key=itemgetter(index))


if __name__ == "__main__":
    data_points = read_file(open("data/cars.csv"))

    sorted_points = sort_by(data_points, i("year"))
    by_origin = split_by(sorted_points, i("origin"))

    i = 1
    print by_origin
    for origin, points in by_origin.iteritems():
        plt.subplot(3, 1, i)
        plt.title(origin)
        plt.xlabel("Year")
        plt.axis([1970, 1982, 0, 200])

        i += 1
        for point in points:
            # TODO change me
            plt.plot([1,2,3,4], [1,4,9,16], 'ro')

            # 3 triangle  "^"
            # 4 square    "s"
            # 5 pentagon  "p"
            # 6 hexagon   "h"/"H"
            # 7 octagon   "8"

    plt.show()
