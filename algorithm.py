# Ayoub El bahi
# Student ID: 012114667
# Nearest neighbor delivery algorithm.
# The idea is simple: from wherever the truck is, go to the closest
# undelivered package next. Repeat until the truck is empty, then go home.


import datetime


def deliver_packages(truck, hash_table, distance_table):

    # load the actual package objects into a working list
    in_transit = []
    for pid in truck.packages:
        pkg = hash_table.search(pid)  
        in_transit.append(pkg)

    # Clear the truck's ID list; it will be rebuilt as packages are delivered.
    truck.packages.clear()

    # keep delivering until there's nothing left
    while in_transit:
        nearest  = None
        min_dist = float('inf')

        # find the closest package to where the truck currently is
        for pkg in in_transit:
            d = distance_table.get_distance(
                distance_table.get_address_index(truck.current_location),
                distance_table.get_address_index(pkg.street)
            )
            if d < min_dist:
                min_dist = d
                nearest  = pkg

        # drive there and record the delivery
        truck.miles += min_dist
        truck.time  += datetime.timedelta(hours=min_dist / truck.speed)
        truck.current_location = nearest.street
        nearest.deliveryTime  = truck.time
        nearest.departureTime = truck.depart_time

        in_transit.remove(nearest)
        truck.packages.append(nearest.ID)

    # head back to the hub after all deliveries are done
    return_dist = distance_table.get_distance(
        distance_table.get_address_index(truck.current_location),
        distance_table.get_address_index("4001 South 700 East")
    )
    truck.miles += return_dist
    truck.time  += datetime.timedelta(hours=return_dist / truck.speed)
