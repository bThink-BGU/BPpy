from copy import copy
from warnings import warn


def thread(func):
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
                    if type(e) == dict:
                        warn("using dict for statements is deprecated, use bppy.model.sync_statement.sync instead.")
                    if isinstance(e, dict):
                        e["locals"] = copy(f.gi_frame.f_locals)
                        m = yield e
                        if m is None:
                            break
                    else:
                        raise TypeError("bthread must yield a bppy.model.sync_statement.sync object")
                except (KeyError, StopIteration):
                    m = yield None
                    break
    return wrapper


def b_thread(func):
    warn("the b_thread decorator is deprecated, use thread instead.")
    return thread(func)


