"""
    Simple file for testing our implementation of the bloom filters
    Was not used in empirical analysis/running of experiments.
"""

from bloom_filter import RazorBloomFilter


bf = RazorBloomFilter(10000, 4)

vals = {
    'a': 1234,
    'b': 2345,
    'c': 1462,
    'd': 1647,
    'e': 7464
}


def review():
    for key_2 in vals:
        print('is', key_2, 'in bloom filter =', bf.is_marked(vals[key_2]))


for key in vals:
    review()
    print('inserted', key, 'into bloom filter')
    bf.insert(vals[key])

bf.revoke(vals['c'])
print('revoked c from bloom filter')

review()


