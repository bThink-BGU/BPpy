Symbolically verify a BProgram using PyNuSMV
++++++++++++++++++++++++++++++++++++++++++++

This example demonstrates how to verify a behavioral program symbolically using `PyNuSMV`.
The :class:`SymbolicBProgramVerifier <bppy.analysis.symbolic_bprogram_verifier.SymbolicBProgramVerifier>` class implementation requires a b-program generator - a function that creates a new instance of the b-program and the list of program events.
The verifier can operate in two modes: Binary Decision Diagrams (BDD) and SAT-based Bounded Model Checking (BMC).
The specification to be verified, is written `NuSMV <https://nusmv.fbk.eu/>`_ LTL specification format.

    *Note:*

    1. The class requires the installation of `PyNuSMV`. More info on its installation can be found at `https://github.com/LouvainVerificationLab/pynusmv
    <https://github.com/LouvainVerificationLab/pynusmv>`_.

    2. The verifier is currently limited to b-programs with :class:`SimpleEventSelectionStrategy
    <bppy.model.event_selection.event_selection_strategy.SimpleEventSelectionStrategy>`.

    3. The verifier does not support events with data.

.. literalinclude :: ../../examples/dining_philosophers_verification.py
