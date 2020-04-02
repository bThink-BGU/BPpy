from copy import deepcopy


def b_thread(func):
    def wrapper(*args):
        while True:
            m = None
            args_copy = deepcopy(args)
            f = func(*args_copy)
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

