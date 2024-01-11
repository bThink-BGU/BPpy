import bppy as bp
from bppy.analysis.bprogram_converter import BProgramConverter

@bp.analysis_thread
def coin_flip():
    side = yield bp.choice({'heads': 0.4, 'tails': 0.6})
    yield bp.sync(request=bp.BEvent(side))

bp_gen = lambda: bp.BProgram(bthreads=[coin_flip()],
				event_selection_strategy=bp.SimpleEventSelectionStrategy())
events = [bp.BEvent('heads'), bp.BEvent('tails')]
converter = BProgramConverter(bp_gen, events, ["coin_flip"])
converter.to_prism('coin_flip.pm')