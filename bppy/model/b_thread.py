from copy import copy
from bppy.model.sync_statement import sync, choice
from warnings import warn

def execution_thread(func):
    return thread(func, 'execution')

def analysis_thread(func):
    return thread(func, 'analysis')

def thread(func, mode='execution'):
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
                        e = sync(**e)
                    if isinstance(e, sync):
                        local_vars = {var:val for var, val in copy(f.gi_frame.f_locals).items()}
                        e["locals"] = copy(local_vars)
                    elif isinstance(e, choice):
                        pass
                        if mode == 'execution':
                            sample = e.sample()
                            e = f.send(sample)
                    else:
                        raise TypeError("bthread must yield a bppy.model.sync_statement object")
                    m = yield e
                    if m is None:
                        break
                except (KeyError, StopIteration):
                    m = yield None
                    break
    return wrapper


def b_thread(func):
    warn("the b_thread decorator is deprecated, use thread instead.")
    return thread(func)


