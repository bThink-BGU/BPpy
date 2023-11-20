import bppy as bp
from bppy.analysis.dfs_bprogram_verifier import DFSBProgramVerifier


@bp.thread
def add_hot():  # requests "HOT" three times
    for i in range(3):
        yield bp.sync(request=bp.BEvent("HOT"))


@bp.thread
def add_cold():  # requests "COLD" three times
    for i in range(3):
        yield bp.sync(request=bp.BEvent("COLD"))


@bp.thread
def control():  # blocking 2 consecutive HOT events
    while True:
        yield bp.sync(waitFor=bp.BEvent("HOT"))
        yield bp.sync(block=bp.BEvent("HOT"), waitFor=bp.BEvent("COLD"))


@bp.thread
def check():  # checks for 2 consecutive COLD events
    while True:
        yield bp.sync(waitFor=bp.BEvent("COLD"))
        e = yield bp.sync(waitFor=bp.All())
        if e == bp.BEvent("COLD"):
            assert False


# function that generates a b-program with the check b-thread
def bp_gen():
    return bp.BProgram(bthreads=[add_hot(), add_cold(), control(), check()],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy())


# initialize DFS verifier with the b-program generator and specify max_trace_length
ver = DFSBProgramVerifier(bp_gen, max_trace_length=1000)
ok, counter_example = ver.verify()

# check the verification results and print accordingly
if ok:
    print("OK")
else:
    print("Violation Found")
    print("Counterexample:")
    print(counter_example)


# After running the b-program, we can see that the check b-thread is able to detect the violation.
# We will now update the control b-thread to fix the violation.
@bp.thread
def control_new():
    # This b-thread controls the temperature by blocking the previously selected event
    # and waiting for all other events in each iteration of its loop
    e = bp.BEvent("Dummy")
    while True:
        e = yield bp.sync(waitFor=bp.All(), block=e)


def bp_gen_new():
    return bp.BProgram(bthreads=[add_hot(), add_cold(), control_new(), check()],
                       event_selection_strategy=bp.SimpleEventSelectionStrategy())


ver = DFSBProgramVerifier(bp_gen_new, max_trace_length=1000)
ok, counter_example = ver.verify()

if ok:
    print("OK")
else:
    print("Violation Found")
    print("Counterexample:")
    print(counter_example)