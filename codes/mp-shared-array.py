#!/usr/bin/env python3

import multiprocessing

def mod2(num):
    with shared_arr.get_lock():
        if num % 2 == 0:
            shared_arr[0] += 1
        else:
            shared_arr[1] += 1

if __name__ == '__main__':
    arr = range(100)
    shared_arr = multiprocessing.Array('i', 2, lock=True)
    print(dir(shared_arr))

    with multiprocessing.Pool(processes=20) as pool:
        pool.map(mod2, arr)

    pool.terminate()
    pool.join()
    
    print(shared_arr[:])
