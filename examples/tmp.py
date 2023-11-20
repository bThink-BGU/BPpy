import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import b_thread
from bppy.analysis.symbolic_bprogram_verifier import SymbolicBProgramVerifier

# define the number of philosophers
PHILOSOPHER_COUNT = 3

# define the event sets
any_take = dict(
    [(i, [bp.BEvent(f"T{i}R"), bp.BEvent(f"T{(i + 1) % PHILOSOPHER_COUNT}L")]) for i in range(PHILOSOPHER_COUNT)])
any_put = dict(
    [(i, [bp.BEvent(f"P{i}R"), bp.BEvent(f"P{(i + 1) % PHILOSOPHER_COUNT}L")]) for i in range(PHILOSOPHER_COUNT)])
any_take_semaphore = bp.EventSet(lambda e: e.name.startswith("TS"))
any_release_semaphore = bp.EventSet(lambda e: e.name.startswith("RS"))
all_events = [bp.BEvent(f"T{i}R") for i in range(PHILOSOPHER_COUNT)] + \
             [bp.BEvent(f"T{i}L") for i in range(PHILOSOPHER_COUNT)] + \
             [bp.BEvent(f"P{i}R") for i in range(PHILOSOPHER_COUNT)] + \
             [bp.BEvent(f"P{i}L") for i in range(PHILOSOPHER_COUNT)] + \
             [bp.BEvent(f"TS{i}") for i in range(PHILOSOPHER_COUNT)] + \
             [bp.BEvent(f"RS{i}") for i in range(PHILOSOPHER_COUNT)]


# define the behavior of a philosopher
@b_thread
def philosopher(i):
    while True:
        for j in range(2):
            yield {request: [bp.BEvent(f"T{i}R"), bp.BEvent(f"T{i}L")]}
        for j in range(2):
            yield {request: [bp.BEvent(f"P{i}R"), bp.BEvent(f"P{i}L")]}


# define the behavior of a fork
@b_thread
def fork(i):
    while True:
        e, cannot_put = None, None
        e = yield {waitFor: any_take[i], block: any_put[i]}
        cannot_put = bp.BEvent(f"P{(i + 1) % PHILOSOPHER_COUNT}L") if e.name.endswith("R") else bp.BEvent(f"P{i}R")
        yield {waitFor: any_put[i], block: any_take[i] + [cannot_put]}


def init_bprogram():  # function to initialize the b-program with the defined b-threads
    bthreads = [philosopher(i) for i in range(PHILOSOPHER_COUNT)] + [fork(i) for i in range(PHILOSOPHER_COUNT)]
    return bp.BProgram(bthreads=bthreads,
                       event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                       listener=bp.PrintBProgramRunnerListener())  # unnecessary here, as SymbolicBProgramVerifier us SimpleEventSelectionStrategy always.


# Initialize verifier and check that the program does not end using the BPROGRAM_DONE flag.
# The verifier will use BDDs to check the property.
verifier = SymbolicBProgramVerifier(init_bprogram, all_events)
result, explanation_str = verifier.verify(spec="G (!(event = BPROGRAM_DONE))", type="BDD", find_counterexample=True,
                                          print_info=False)

if result:
    print("OK")
else:
    print("Violation Found")
    print("Counterexample:")
    print(explanation_str)

# Initialize verifier and check that philosophers 0 takes the left fork infinitely often.
# The verifier will use SAT-based bounded model checking with bound 10 to check the property.
verifier = SymbolicBProgramVerifier(init_bprogram, all_events)
result, explanation_str = verifier.verify(spec="G (F event = T0L)", type="BMC", bound=10, find_counterexample=True,
                                          print_info=False)

if result:
    print("OK")
else:
    print("Violation Found")
    print("Counterexample:")
    print(explanation_str)

# introduce semaphores to fix the classic problem
@b_thread
def semaphore():
    while True:
        yield {waitFor: any_take_semaphore}
        yield {waitFor: any_release_semaphore, block: any_take_semaphore}


@b_thread
def take_semaphore(i):
    while True:
        yield {request: bp.BEvent(f"TS{i}"), block: [bp.BEvent(f"T{i}R"), bp.BEvent(f"T{i}L")]}
        for j in range(2):
            yield {waitFor: [bp.BEvent(f"T{i}R"), bp.BEvent(f"T{i}L")]}
        yield {request: bp.BEvent(f"RS{i}"), block: [bp.BEvent(f"P{i}R"), bp.BEvent(f"P{i}L")]}
        for j in range(2):
            yield {waitFor: [bp.BEvent(f"P{i}R"), bp.BEvent(f"P{i}L")]}


def init_fixed_bprogram():  # initialize the fixed b-program with semaphores and the defined b-threads
    bthreads = [philosopher(i) for i in range(PHILOSOPHER_COUNT)] + [fork(i) for i in range(PHILOSOPHER_COUNT)] + [
        semaphore()] + [take_semaphore(i) for i in range(PHILOSOPHER_COUNT)]
    return bp.BProgram(bthreads=bthreads,
                       event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                       listener=bp.PrintBProgramRunnerListener())

# Initialize verifier and see that the updated program does not end.
verifier = SymbolicBProgramVerifier(init_fixed_bprogram, all_events)
result, explanation_str = verifier.verify(spec="G (!(event = BPROGRAM_DONE))", type="BDD", find_counterexample=True,
                                          print_info=False)

if result:
    print("OK")
else:
    print("Violation Found")
    print("Counterexample:")
    print(explanation_str)

# Initialize verifier and see that philosophers 0 might stay hungry in the updated program :)
result, explanation_str = verifier.verify(spec="G (F event = T0L)", type="BMC", bound=10, find_counterexample=True,
                                          print_info=False)

if result:
    print("OK")
else:
    print("Violation Found")
    print("Counterexample:")
    print(explanation_str)