BPpy: Behavioral Programming In Python
=

Install
============

You can install ``bppy`` with:

```shell
git clone https://github.com/tomyaacov/BPpy.git
cd BPpy
pip install -e .
```


Run
-----------

```python
from bppy import *


def add_hot():
    yield {request: BEvent("HOT")}
    yield {request: BEvent("HOT")}
    yield {request: BEvent("HOT")}


def add_cold():
    yield {request: BEvent("COLD")}
    yield {request: BEvent("COLD")}
    yield {request: BEvent("COLD")}


def control_temp():
    while True:
        yield {waitFor: BEvent("COLD"), block: BEvent("HOT")}
        yield {waitFor: BEvent("HOT"), block: BEvent("COLD")}

   
if __name__ == "__main__":
    b_program = BProgram(source_name="hot_cold_bath",
                         # bthreads=[add_hot(), add_cold(), control_temp()], # alternative to source name
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()

```