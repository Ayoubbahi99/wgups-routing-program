# Ayoub El bahi
# Student ID: 012114667
# Course    : C950 — Data Structures and Algorithms II
# Program   : WGUPS Routing Program
#
# Purpose:
#   Deliver all 40 WGUPS packages on time while keeping the combined truck
#   mileage under 140 miles, using a nearest-neighbor greedy algorithm and
#   a custom chaining hash table for fast package lookups.

import csv
import datetime

from hash_table     import ChainingHashTable
from package        import Package
from truck          import Truck
from distance_table import DistanceTable
from algorithm      import deliver_packages


def load_packages(filename, hash_table):
    # read each row from the CSV and store the package in the hash table
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            p = Package(int(row[0]), row[1], row[2], row[3],
                        row[4], row[5], row[6], row[7])
            hash_table.insert(p.ID, p)


def assign_truck(truck, hash_table, truck_id):
    # go back and write the truck number onto each package it delivered
    for pid in truck.packages:
        pkg = hash_table.search(pid)
        if pkg:
            pkg.truckID = truck_id


def lookup_all_packages(hash_table):
    time_str = input("\n  Enter time (HH:MM, 24-hour): ").strip()
    try:
        h, m = map(int, time_str.split(":"))
    except ValueError:
        print("  Invalid format, use HH:MM")
        return

    t = datetime.timedelta(hours=h, minutes=m)

    print(f"\n  {'─' * 88}")
    print(f"  Package status at {time_str}")
    print(f"  {'─' * 88}")
    print(f"  {'ID':>3}  {'Address':<42}  {'Deadline':<10}  {'Wt':>4}  {'Truck':>5}  {'Status':<12}  Delivered At")
    print(f"  {'─' * 88}")

    for pid in range(1, 41):
        pkg = hash_table.search(pid)
        if pkg:
            pkg.update_status(t)
            truck_label  = f"T{pkg.truckID}" if pkg.truckID else "--"
            delivery_str = str(pkg.deliveryTime) if pkg.deliveryTime else "Not yet"
            print(f"  {pid:>3}  {pkg.street:<42}  {pkg.deadline:<10}  "
                  f"{pkg.weight:>4}  {truck_label:>5}  {pkg.status:<12}  {delivery_str}")

    print(f"  {'─' * 88}\n")


def lookup_single_package(hash_table):
    pid_str = input("\n  Enter package ID (1-40): ").strip()
    try:
        pid = int(pid_str)
    except ValueError:
        print("  That's not a valid ID")
        return

    pkg = hash_table.search(pid)
    if pkg is None:
        print(f"  Package {pid} not found.")
        return

    time_str = input("  Enter time (HH:MM) or press Enter to see final status: ").strip()
    if time_str:
        try:
            h, m = map(int, time_str.split(":"))
            pkg.update_status(datetime.timedelta(hours=h, minutes=m))
        except ValueError:
            print("  Invalid time")
            return
    else:
        pkg.update_status(datetime.timedelta(hours=23, minutes=59))

    print(f"\n  {'═' * 50}")
    print(f"  Package {pkg.ID}")
    print(f"  {'═' * 50}")
    print(f"  Address  : {pkg.street}")
    print(f"  City     : {pkg.city}")
    print(f"  State    : {pkg.state}")
    print(f"  Zip      : {pkg.zip}")
    print(f"  Deadline : {pkg.deadline}")
    print(f"  Weight   : {pkg.weight} kg")
    print(f"  Notes    : {pkg.notes if pkg.notes else 'None'}")
    print(f"  Truck    : {pkg.truckID if pkg.truckID else 'N/A'}")
    print(f"  Status   : {pkg.status}")
    print(f"  Delivered: {pkg.deliveryTime if pkg.deliveryTime else 'Not yet'}")
    print(f"  {'═' * 50}\n")


def print_mileage(truck1, truck2, truck3):
    total = truck1.miles + truck2.miles + truck3.miles
    print(f"\n  {'─' * 40}")
    print(f"  Mileage Summary")
    print(f"  {'─' * 40}")
    print(f"  Truck 1: {truck1.miles:.2f} miles")
    print(f"  Truck 2: {truck2.miles:.2f} miles")
    print(f"  Truck 3: {truck3.miles:.2f} miles")
    print(f"  {'─' * 40}")
    print(f"  Total  : {total:.2f} miles")
    if total < 140:
        print(f"  Under the 140 mile limit")
    else:
        print(f"  Over the limit!")
    print(f"  {'─' * 40}\n")


def main():
    hash_table = ChainingHashTable()
    load_packages("./data/packageCSV.csv", hash_table)

    distance_table = DistanceTable("./data/distanceCSV.csv")

    # manually loaded trucks based on the package constraints
    # truck 1 leaves at 8am - has the co-delivery group and the early deadlines
    truck1 = Truck(18, "4001 South 700 East", datetime.timedelta(hours=8),
                   [1, 29, 7, 30, 8, 34, 40, 14, 15, 16, 19, 20, 13, 37, 38, 36])

    # truck 2 leaves at 9:05 so the delayed packages have time to arrive
    # also has the truck-2-only packages (3, 18) and package 9 (wrong address until 10:20)
    truck2 = Truck(18, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),
                   [3, 18, 6, 28, 32, 33, 25, 12, 9, 22, 24, 11, 10, 5, 4, 21])

    # truck 3 goes out later once a driver gets back
    truck3 = Truck(18, "4001 South 700 East", datetime.timedelta(hours=11),
                   [2, 17, 23, 26, 27, 31, 35, 39])

    deliver_packages(truck1, hash_table, distance_table)

    # if truck 1 gets back before 9:05, the driver can take truck 2 out early
    truck2.depart_time = min(truck1.time, truck2.depart_time)
    deliver_packages(truck2, hash_table, distance_table)

    deliver_packages(truck3, hash_table, distance_table)

    assign_truck(truck1, hash_table, 1)
    assign_truck(truck2, hash_table, 2)
    assign_truck(truck3, hash_table, 3)

    while True:
        print("  1. View all packages at a specific time")
        print("  2. Look up a single package")
        print("  3. View mileage")
        print("  4. Exit")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            lookup_all_packages(hash_table)
        elif choice == "2":
            lookup_single_package(hash_table)
        elif choice == "3":
            print_mileage(truck1, truck2, truck3)
        elif choice == "4":
            break
        else:
            print("  Enter 1, 2, 3, or 4\n")


if __name__ == "__main__":
    main()
