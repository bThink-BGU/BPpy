from copy import copy


def b_thread(func):
    def wrapper(*args):
        while True:
            m = None
            f = func(*args)
            while True:
                try:
                    e = f.send(m)
                    m = yield e
                    if m is None:
                        break
                except (KeyError, StopIteration):
                    m = yield None
                    break
    return wrapper

