import bppy as bp
from bppy.model.b_thread import execution_thread
from bppy.utils.dfs import DFSBProgram
from bppy.analysis.bprogram_converter import BProgramConverter


# https://qcomp.org/benchmarks/#coupon

N = 5
DRAWS = 2
B = 5


@bp.analysis_thread
def open_boxes():
	for _ in range(B):
		box = {i: 1/N for i in range(N)}
		for _ in range(DRAWS):
			draw = yield bp.choice(box)
			box.pop(draw)
			box = {i: 1/len(box) for i in box}
			yield bp.sync(request=bp.BEvent(draw))

@bp.execution_thread
def mark_collected():
	collection = set()
	for i in range(B*DRAWS):
		draw = yield bp.sync(waitFor=bp.All())
		collection.add(draw.name)
		if len(collection) == N:
			yield bp.sync(request=bp.BEvent("all_collected"), block=bp.EventSet(lambda e: type(e.name) == int))
			break
	if len(collection) != N:
		yield bp.sync(request=bp.BEvent("failed_to_collect"), block=bp.EventSet(lambda e: type(e.name) == int))
	for _ in range (i, B*DRAWS):
		yield bp.sync(block=bp.EventSet(lambda e: type(e.name) == int))
	


def bp_gen():
	return bp.BProgram(bthreads=[open_boxes(), mark_collected()],
					event_selection_strategy=bp.SimpleEventSelectionStrategy())


converter = BProgramConverter(bp_gen, [bp.BEvent("all_collected"), bp.BEvent("failed_to_collect")]
			+ [bp.BEvent(i) for i in range(N)], max_trace_length=10)
converter.to_prism("coupons.pm")
