import logging
from multiprocessing import Process, Manager, current_process


def calc_factorize(num, val: Manager):
    name = current_process().name
    res = []
    for n in range(1, num+1):
        if (num % n) == 0:
            res.append(n)
    val[name] = res


def factorize(*number):
    with Manager() as manager:
        m = manager.dict()
        processes = []
        ix = 0
        for ix in range(len(number)):
            num = number[ix]
            pr = Process(target=calc_factorize, name='Process-'+str(ix), args=(num, m))
            pr.start()
            processes.append(pr)

        [pr.join() for pr in processes]
        res = dict(m.items())

    result = []
    for ix in range(len(number)):
        result.append(res['Process-'+str(ix)])
    if len(result) > 1:
        return result
    else:
        return result[0]


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s  %(threadName)s  %(message)s',
        handlers=[
            logging.FileHandler("factorize_parallel.log"),
            logging.StreamHandler()
        ]
    )
    logging.debug('Start')
    a, d, c, b = factorize(128, 10651060, 99999, 255)
    logging.debug('Finish')

    print(a)
    print(b)
    print(c)
    print(d)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
