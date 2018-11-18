from bloom_filter import RevisedExtendedBloomFilter
from random import sample
from random import shuffle
from random import randint
from random import random
from math import floor
import numpy as np
import multiprocessing as mp

# from http://code.activestate.com/recipes/360461-fisher-yates-shuffle/
def fisher_yates_shuffle(ary):
    a=len(ary)
    b=a-1
    for d in range(b,0,-1):
      e=randint(0,d)
      if e == d:
            continue
      ary[d],ary[e]=ary[e],ary[d]
    return ary
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
    return calc_false_positive_rate(bf, distinct_keys, 20)


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
    return calc_false_positive_rate(bf, distinct_keys, 20)


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
    fisher_yates_shuffle(all_keys)
    for e in all_keys:
        bf.insert(e)

    # Check the false-positive rate
    return calc_false_positive_rate(bf, distinct_keys, 20)


def experiment4(n, m, k):
    """
    Run experiment 4, where each key is inserted a random number 20 or less times, and all insertions are in a random order
    :param n: number of distinct keys
    :param m: the size of the bloom filter
    :param k: the number of hashes used by the bloom filter
    """
    distinct_keys = generate_keys(n)
    bf = RevisedExtendedBloomFilter(m, k)
    all_keys=[]
    c_list={}
    for e in distinct_keys:
        c = randint(0,20)
        c_list[e]=c
        for _ in range(c):
            all_keys.append(e)
    fisher_yates_shuffle(all_keys)
    for e in all_keys:
        bf.insert(e)
    # Check the false-positive rate
    return calc_false_positive_rate_random(bf, distinct_keys, c_list)

def experiment5(n, m, k):
    """
    Run experiment 5, where each key is inserted a random number 20 or less times
    :param n: number of distinct keys
    :param m: the size of the bloom filter
    :param k: the number of hashes used by the bloom filter
    """
    distinct_keys = generate_keys(n)
    bf = RevisedExtendedBloomFilter(m, k)
    all_keys=[]
    c_list={}
    for e in distinct_keys:
        c = randint(0,20)
        c_list[e]=c
        for _ in range(c):
            all_keys.append(e)
    for e in all_keys:
        bf.insert(e)
    # Check the false-positive rate
    return calc_false_positive_rate_random(bf, distinct_keys, c_list)


def experiment6(n, m, k):
    """
    Run experiment 6, where each key is inserted a poisson random variable with lambda=10 times
    :param n: number of distinct keys
    :param m: the size of the bloom filter
    :param k: the number of hashes used by the bloom filter
    """
    distinct_keys = generate_keys(n)
    bf = RevisedExtendedBloomFilter(m, k)
    all_keys=[]
    c_list={}
    for e in distinct_keys:
        c = np.random.poisson(10)
        c_list[e]=c
        for _ in range(c):
            all_keys.append(e)
    fisher_yates_shuffle(all_keys)
    for e in all_keys:
        bf.insert(e)
    # Check the false-positive rate
    return calc_false_positive_rate_random(bf, distinct_keys, c_list)


def experiment7(n, m, k):
    """
    Run experiment 7, where each key is inserted a poisson random variable with lambda=20 times
    :param n: number of distinct keys
    :param m: the size of the bloom filter
    :param k: the number of hashes used by the bloom filter
    """
    distinct_keys = generate_keys(n)
    bf = RevisedExtendedBloomFilter(m, k)
    all_keys=[]
    c_list={}
    for e in distinct_keys:
        c = np.random.poisson(20)
        c_list[e]=c
        for _ in range(c):
            all_keys.append(e)
    fisher_yates_shuffle(all_keys)
    for e in all_keys:
        bf.insert(e)
    # Check the false-positive rate
    return calc_false_positive_rate_random(bf, distinct_keys, c_list)


def experiment8(n, m, k):
    """
    Run experiment 8, where each key is inserted a random number 40 or less times, and all insertions are in a random order
    :param n: number of distinct keys
    :param m: the size of the bloom filter
    :param k: the number of hashes used by the bloom filter
    """
    distinct_keys = generate_keys(n)
    bf = RevisedExtendedBloomFilter(m, k)
    all_keys=[]
    c_list={}
    for e in distinct_keys:
        c = randint(0,40)
        c_list[e]=c
        for _ in range(c):
            all_keys.append(e)
    fisher_yates_shuffle(all_keys)
    for e in all_keys:
        bf.insert(e)
    # Check the false-positive rate
    return calc_false_positive_rate_random(bf, distinct_keys, c_list)

def generate_keys(n):
    """
    Generate n distinct integers in the range [1,P-1]
    :param n: the number of distinct integers to generate
    """
    return sample(range(1, P), n)


def calc_false_positive_rate(bf, keys, c):
    n = len(keys)
    fp = 0
    for e in keys:
        if bf.has_false_positive(e, c):
            fp += 1

    #return fp/(n*c)
    return fp/(n)

def calc_false_positive_rate_random(bf, keys, c_list):
    n = len(keys)
    fp = 0
    l = sum(c_list.values())
    zeros = 0
    for e in keys:
        if c_list[e] == 0 :
            zeros=zeros+1
        elif bf.has_false_positive(e, c_list[e]):
            # fp += 1
            fp += c_list[e]
    # return fp/(n-zeros)
    return fp/l


experiments = [experiment1, experiment2, experiment3, experiment4,
               experiment5, experiment6, experiment7, experiment8]


def proc_experiments(rounds, e, n, m, k, output):
    results = []
    for _ in range(rounds):
        results.append(experiments[e](n, m, k))
    output.put(results)

# number of rounds to run each configuration on an experiment
#  in the paper it is 1000
NUM_ROUNDS = 100

# N = 10000
M = 40000
K = 6 # 4, 6, 8

NM = [0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
# NM = np.linspace(0.05, 0.25, 11)# values of N/M

# Create csv file for output
filename = "output-{0}-{1}.csv".format(M, K)
f = open(filename, 'w')
f.write("N/M,exp1-mean,exp1-std,exp2-mean,exp2-std,exp3-mean,exp3-std,exp4-mean,exp4-std,exp5-mean,exp5-std,"
        "exp6-mean,exp6-std,exp7-mean,exp7-std,exp8-mean,exp8-std\n")

for nm in NM:
    print("\nN/M =", nm)
    N = int(nm * M)
    f.write("{0}".format(nm))

    for e in range(8):
        fp_rates = []
        print("Running Experiment", e+1)
        num_procs = 4
        output = mp.Queue()
        processes = [mp.Process(target=proc_experiments, args=(int(NUM_ROUNDS/num_procs), e, N, M, K, output)) for _ in range(num_procs)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()

        # for i in range(NUM_ROUNDS):
        #     if i % 5 == 0:
        #         print("  iter: ", i)
        #     fp_rates.append(experiments[e](N, M, K))
        for p in processes:
            fp_rates = fp_rates + output.get()
        f.write(",{0},{1}".format(np.mean(fp_rates), np.std(fp_rates)))

    f.write("\n")

f.close()
