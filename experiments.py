from bloom_filter import RevisedExtendedBloomFilter
from random import sample
from random import shuffle

"""
This is a standard prime number used in hashing, as referenced by the paper.
"""
P = 2100000011


def experiment1(n, m, k):
    """
    Run experiment 1, where each key is inserted once each round, for 20 rounds
    :param n: number of distinct keys
    :param m: the size of the bloom filter
    :param k: the number of hashes used by the bloom filter
    """
    distinct_keys = generate_keys(n)
    bf = RevisedExtendedBloomFilter(m, k)
    for _ in range(20):
        for e in distinct_keys:
            bf.insert(e)

    # Check the false positive rate
    print("Experiment 1:", calc_false_positive_rate(bf, distinct_keys, 20))


def experiment2(n, m, k):
    """
    Run experiment 2, where each key is inserted 20 times in a row
    :param n: number of distinct keys
    :param m: the size of the bloom filter
    :param k: the number of hashes used by the bloom filter
    """
    distinct_keys = generate_keys(n)
    bf = RevisedExtendedBloomFilter(m, k)
    for e in distinct_keys:
        for _ in range(20):
            bf.insert(e)

    # Check the false-positive rate
    print("Experiment 2:", calc_false_positive_rate(bf, distinct_keys, 20))


def experiment3(n, m, k):
    """
    Run experiment 3, where each key is inserted 20 times, but all insertions are in a random order
    :param n: number of distinct keys
    :param m: the size of the bloom filter
    :param k: the number of hashes used by the bloom filter
    """
    distinct_keys = generate_keys(n)
    bf = RevisedExtendedBloomFilter(m, k)

    all_keys = distinct_keys * 20
    shuffle(all_keys)
    for e in all_keys:
        bf.insert(e)

    # Check the false-positive rate
    print("Experiment 3:", calc_false_positive_rate(bf, distinct_keys, 20))


def generate_keys(n):
    """
    Generate n distinct integers in the range [1,P-1]
    :param n: the number of distinct integers to generate
    """
    return sample(range(1, P-1), n)


def calc_false_positive_rate(bf, keys, c):
    n = len(keys)
    fp = 0
    for e in keys:
        if bf.has_false_positive(e, c):
            fp += 1

    return fp/n


N = 10000
M = 80000
K = 6
experiment1(N, M, K)
experiment2(N, M, K)
experiment3(N, M, K)
