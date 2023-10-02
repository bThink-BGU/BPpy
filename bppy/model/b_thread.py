from copy import copy
from probabilities import Choice

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
                    if isinstance(e, Choice):
                        m = e.sample()
                        e = f.send(m)
                    if isinstance(e, dict):
                        local_vars = {var:val for var, val in copy(f.gi_frame.f_locals).items()}
                        e["locals"] = local_vars
                    m = yield e
                    if m is None:
                        break
                except (KeyError, StopIteration):
                    m = yield None
                    break
    return wrapper

