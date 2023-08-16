from copy import copy


def b_thread(func):
    """
    A decorator to wrap bthread generator with, in order to handle data transmission and bthread termination.
    """
    def wrapper(*args):
        while True:
            m = None
            f = func(*args)
            while True:
                try:
                    e = f.send(m)
                    if isinstance(e, dict):
                        e["locals"] = copy(f.gi_frame.f_locals)
                    m = yield e
                    if m is None:
                        break
                except (KeyError, StopIteration):
                    m = yield None
                    break
    return wrapper

