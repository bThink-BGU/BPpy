from bppy.model.event_selection.smt_event_selection_strategy import SMTEventSelectionStrategy

def ExperimentalSMTEventSelectionStrategy():
    from warnings import warn
    warn('Class ExperimentalSMTEventSelectionStrategy is deprecated. Returned SMTEventSelectionStrategy instead.',
         DeprecationWarning, stacklevel=2)
    return SMTEventSelectionStrategy()
