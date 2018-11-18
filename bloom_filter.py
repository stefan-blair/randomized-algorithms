from array import array
from random import randint


"""
This is a standard prime number used in hashing, as referenced by the paper.
"""
P = 2100000011


class BloomFilter:

    def __init__(self, m, k):
        """
        Initialize the BloomFilter with the following parameters:
        - bloom_filter: an `array` object with m bytes, each initialized to 0, that is used as the main storage
        - hash_functions: a list of k hash functions.  each function also has the additional attributes c and d, which
            are their hash parameters
        :param m: the length of the bloom filter
        :param k: the number of hash functions used when inserting an object
        """
        # allocate a large array with m bytes, all initialized to 0
        self.bloom_filter = array('B', [0]) * m
        self.m = m
        self.k = k
        # initialize arrays to hold values for the universal hash functions
        self.c_values = []
        self.d_values = []
        for _ in range(k):
            # generate two random parameters
            c = randint(1, P - 1)
            d = randint(0, P - 1)

            self.c_values.append(c)
            self.d_values.append(d)

    def hash(self, i):
        """
        Applies each hash function in self.hash_functions to the item.
        :param i: the item to hash
        :return: the array of hash values
        """
        ret = []
        for h in range(self.k):
            ret.append(((self.c_values[h] * i + self.d_values[h]) % P) % self.m)
        return ret

    def is_marked(self, i):
        """
        Returns if the given item is currently marked in the bloom filter.
        :param i: the item whose membership should be tested
        :return: a boolean indicating if the item is a member or not
        """
        return all(self.bloom_filter[h] > 0 for h in self.hash(i))

    def insert(self, i):
        """
        Insert the given element i into the bloom filter.
        :param i:
        """
        pass


class RazorBloomFilter(BloomFilter):

    def __init__(self, m, k):
        self.revoked_bloom_filter = array('B', [0]) * m
        super().__init__(m, k)

    def is_marked(self, i):
        marked = super().is_marked(i)
        revoked = all(self.revoked_bloom_filter[h] > 0 for h in self.hash(i))

        return marked and not revoked

    def insert(self, i):
        for h in self.hash(i):
            self.bloom_filter[h] = 1

    def revoke(self, i):
        """
        Razor-specific function for removing a given signature from the bloom filter by adding it to the
        revoked bloom filter
        :param i: item to revoke
        """
        for h in self.hash(i):
            self.revoked_bloom_filter[h] = 1


class IntuitiveExtendedBloomFilter(BloomFilter):

    def __init__(self, m, k, r=63):
        """
        :param r: the threshold for the number of hits a bloom filter element must have before being "marked"
        """
        self.r = r
        super().__init__(m, k)

    def is_marked(self, i):
        return min([self.bloom_filter[h] for h in self.hash(i)]) >= self.r

    def has_false_positive(self, i, c):
        """
        Check if key i has a false positive. If returns True, when c is the expected
            number of times inserted, then we have a false-positive
        :param i: the element
        :param c: value to check against how many times this element was inserted
        :return: boolean if the minimum count for this element is not equal to c
        """
        m = min([self.bloom_filter[h] for h in self.hash(i)])
        return m != c

    def insert(self, i):
        for h in set(self.hash(i)):
            # make sure not to increment past r, in case of overflow
            if self.bloom_filter[h] < self.r:
                self.bloom_filter[h] += 1


class RevisedExtendedBloomFilter(IntuitiveExtendedBloomFilter):

    def insert(self, i):
        # find the minimum count indexed by any of the hashes
        minimum = min([self.bloom_filter[h] for h in self.hash(i)])
        # iterate over all of the unique indexes, to avoid local coincidental hits
        for h in set(self.hash(i)):
            # only update the bloom filter indexes that are equal to the minimum, to avoid global coincidental hits
            if self.bloom_filter[h] == minimum and self.bloom_filter[h] < self.r:
                self.bloom_filter[h] += 1
