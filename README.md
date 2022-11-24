# BPpy: Behavioral Programming In Python
A Python implementation for the Behavioral Programming paradigm

## Install
You can install ``bppy`` with pip:

```shell
pip install bppy
```

## Running the Hot-Cold Example
python bppy/examples/hot_cold_all.py


## Writing a BPpy program
[bppy/examples/hot_cold_all.py](bppy/examples/hot_cold_all.py):
```python
from bppy import *

@b_thread
def add_hot():
    yield {request: BEvent("HOT")}
    yield {request: BEvent("HOT")}
    yield {request: BEvent("HOT")}

@b_thread
def add_cold():
    yield {request: BEvent("COLD")}
    yield {request: BEvent("COLD")}
    yield {request: BEvent("COLD")}

@b_thread
def control_temp():
    e = BEvent("Dummy")
    while True:
        e = yield {waitFor: All(), block: e}

if __name__ == "__main__":
    b_program = BProgram(bthreads=[add_hot(), add_cold(), control_temp()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
```

## Using Z3-Solver SMT
[bppy/examples/hot_cold_smt.py](bppy/examples/hot_cold_smt.py):
```python
from bppy import *

hot = Bool('hot')
cold = Bool('cold')

@b_thread
def three_hot():
    for i in range(3):
        while (yield {request: hot})[hot] == false:
            pass

@b_thread
def three_cold():
    for j in range(3):
        m = yield {request: cold}
        while m[cold] == false:
            m = yield {request: cold}

@b_thread
def exclusion():
    while True:
        yield {block: And(hot, cold)}

@b_thread
def schedule():
    yield {block: cold}

if __name__ == "__main__":
    b_program = BProgram(bthreads=[three_cold(), three_hot(), exclusion(), schedule()],
                         event_selection_strategy=SMTEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
```

## Dynamically adding b-threads

[bppy/examples/hot_cold_dynamic.py](bppy/examples/hot_cold_dynamic.py):
```python
from bppy import *


@b_thread
def add_hot():
    yield {request: BEvent("HOT")}
    yield {request: BEvent("HOT")}
    yield {request: BEvent("HOT")}


@b_thread
def add_cold():
    yield {request: BEvent("COLD")}
    yield {request: BEvent("COLD")}
    yield {request: BEvent("COLD")}


@b_thread
def control_temp(block_event):
    block_event = yield {waitFor: All(), block: block_event}
    b_program.add_bthread(control_temp(block_event))


if __name__ == "__main__":
    b_program = BProgram(bthreads=[add_hot(), add_cold(), control_temp(BEvent("HOT"))],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
```

To cite this repository in publications:
```
@misc{bppy,
  author = {Tom Yaacov},
  title = {BPpy: Behavioral Programming In Python},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/bThink-BGU/BPpy}},
}
```
