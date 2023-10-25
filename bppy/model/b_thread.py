from copy import copy, deepcopy
from bppy.model.sync_statement import BSync
from bppy.utils.probability import Choice

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
                    if isinstance(e, BSync):
                        local_vars = {var:val for var, val in copy(f.gi_frame.f_locals).items()}
                        e["locals"] = copy(local_vars)
                    m = yield e
                    if m is None:
                        break
                except (KeyError, StopIteration):
                    m = yield None
                    break
    return wrapper

