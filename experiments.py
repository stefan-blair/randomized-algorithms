"""
    This is the main file that all the simulations/experiments are run.
    The 8 experiments that are defined in the paper's simulation are each
        implemented below, as well as functions for calculating the false
        positive rates.
    All 8 experiments were run among a range of n/m ratios, as well as
        different configurations of m and k.
    Output for a single configuration of m and k are put into CSV file.
"""
from bloom_filter import RevisedExtendedBloomFilter
from random import sample
from random import randint
import numpy as np
import multiprocessing as mp

# from http://code.activestate.com/recipes/360461-fisher-yates-shuffle/
# used to shuffle the insertion sequences for some of the experiments
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

    # Get the false positive rate
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

    # Get the false-positive rate
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

    # Get the false-positive rate
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

    # Get the false-positive rate
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

    # Get the false-positive rate
    return calc_false_positive_rate_random(bf, distinct_keys, c_list)


def experiment6(n, m, k):
    """
    Run experiment 6, where each key is inserted a poisson random variable with lambda=10 times, and shuffled
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
    # Get the false-positive rat
    # e
    return calc_false_positive_rate_random(bf, distinct_keys, c_list)


def experiment7(n, m, k):
    """
    Run experiment 7, where each key is inserted a poisson random variable with lambda=20 times, and shuffled
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

    # Get the false-positive rate
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

    # Get the false-positive rate
    return calc_false_positive_rate_random(bf, distinct_keys, c_list)


def generate_keys(n):
    """
    Generate n distinct integers in the range [1,P-1]
    :param n: the number of distinct integers to generate
    """
    return sample(range(1, P), n)


def calc_false_positive_rate(bf, keys, c):
    """
    Calculation of the FP-rate used by the first 3 experiments,
        since for each of those, each integer is inserted exactly c times.
    :param bf: the Bloom filter
    :param keys: the distinct elements/integers that were inserted
    :param c: number of times each integer was inserted
    :return: FP-rate calculated as the number of distinct keys/elements that
                had a false positive divided by total number of distinct keys/elements
    """
    n = len(keys)
    fp = 0
    for e in keys:
        if bf.has_false_positive(e, c):
            fp += 1

    return fp/n


def calc_false_positive_rate_random(bf, keys, c_list):
    """
    Calculation of the FP-rate used by the last 5 experiments,
        since for each of those, each integer is inserted a random number of times.
    As in the paper, the FP-rate is calculated by summing up among the integers that had
        a false positive, the number of times that integer was inserted (c_i). And then
        taking that sum and dividing by the total number of insertions that were done.
    :param bf: the Bloom filter
    :param keys: the number of distinct integers inserted
    :param c_list: list containing the number of times that each individual integer was inserted
    :return: the FP-rate
    """
    fp = 0
    l = sum(c_list.values())
    zeros = 0
    for e in keys:
        if c_list[e] == 0 :
            zeros=zeros+1
        elif bf.has_false_positive(e, c_list[e]):
            fp += c_list[e]

    return fp/l


# List of all experiment functions, to be iterated over below
experiments = [experiment1, experiment2, experiment3, experiment4,
               experiment5, experiment6, experiment7, experiment8]


def proc_experiments(rounds, e, n, m, k, output):
    """
    Function used for parallelizing the algorithm (done just to make it run faster)
    :param rounds: number of times the experiment gets run per process
    :param e: the index of the experiment to be run
    """
    #print("Processing Experiment",e,n, m, k)
    results = []
    for _ in range(rounds):
        results.append(experiments[e](n, m, k))
    output.put(results)


# The number of rounds to run each configuration on an experiment.
# In the paper it is 1000.
NUM_ROUNDS = 100

# All combinations of m and k were used to generate results
# M could take the values: 40000, 80000, 160000, or 320000
# K could take the values: 4, 6, or 8
M = [40000,80000,160000,320000]
K = [4,6,8]

# Range of n/m values that were used. Step size of 0.02
NM = np.linspace(0.05, 0.25, 11)

# Loop through each configuration of k and m
for k in K:
    print("K =", k)
    for m in M:
        print("M =", m)
        # Create csv file for output. Filename containing m and k
        filename = "output-{0}-{1}.csv".format(m, k)
        f = open(filename, 'w')
        # File output contains both means and standard deviations for each experiment, for each n/m ratio
        f.write("N/M,exp1-mean,exp1-std,exp2-mean,exp2-std,exp3-mean,exp3-std,exp4-mean,exp4-std,exp5-mean,exp5-std,"
        "exp6-mean,exp6-std,exp7-mean,exp7-std,exp8-mean,exp8-std\n")

        # For each of the n/m ratios, run all 8 experiments
        for nm in NM:
            print("N/M =", nm)
            N = int(nm * m)
            f.write("{0}".format(nm))

            for e in range(8):
                # Each experiment runs NUM_ROUNDS times, in order to get a good
                #   mean and stddev for the false positive rate
                fp_rates = []
                print("Running Experiment", e+1)
                num_procs = 4
                output = mp.Queue()
                processes = [mp.Process(target=proc_experiments, args=(int(NUM_ROUNDS/num_procs), e, N, m, k, output)) for _ in range(num_procs)]
                for p in processes:
                    p.start()
                for p in processes:
                    p.join()
                for p in processes:
                    fp_rates = fp_rates + output.get()
                f.write(",{0},{1}".format(np.mean(fp_rates), np.std(fp_rates)))

            f.write("\n")
        f.close()
