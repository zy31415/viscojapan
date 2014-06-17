from multiprocessing import Pool

from numpy import ones


def f(x):
    return x*ones((3,3))

if __name__ == '__main__':
    # start 4 worker processes
    with Pool(processes=4) as pool:

        # print "[0, 1, 4,..., 81]"
        print(pool.map(f, range(10)))
