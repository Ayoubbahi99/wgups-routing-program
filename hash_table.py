# Ayoub El bahi
# Student ID: 012114667
# Custom hash table using chaining to handle collisions.
# I built this without any extra libraries, just plain Python lists.


class ChainingHashTable:
    # Each bucket is a list of [key, value] pairs.
    # If two keys land in the same bucket they just get added to that list.

    def __init__(self, capacity=40):
        # 40 buckets to match the number of packages
        self.table = [[] for _ in range(capacity)]

    def insert(self, key, item):
        # figure out which bucket this key goes into
        bucket = hash(key) % len(self.table)

        # if the key already exists, just update it
        for pair in self.table[bucket]:
            if pair[0] == key:
                pair[1] = item
                return

        # otherwise add a new entry
        self.table[bucket].append([key, item])

    def search(self, key):
        bucket = hash(key) % len(self.table)

        for pair in self.table[bucket]:
            if pair[0] == key:
                return pair[1]

        return None
