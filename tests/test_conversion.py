import unittest
import bppy as bp
from bppy.analysis.bprogram_converter import BProgramConverter

class TestBProgram(unittest.TestCase):

	def test_prism_conversion(self):
		@bp.analysis_thread
		def main():
			r = yield bp.choice({'a': 0.2, 'b': 0.3, 'c': 0.5})
			yield bp.sync(request=bp.BEvent(r))

		def bp_gen():
			return bp.BProgram(bthreads=[main()],
							event_selection_strategy=bp.SimpleEventSelectionStrategy())

		converter = BProgramConverter(bp_gen, [bp.BEvent('a'), bp.BEvent('b'), bp.BEvent('c')])
		output = converter.to_prism(None)
		assert output
