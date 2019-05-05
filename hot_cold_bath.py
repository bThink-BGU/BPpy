from model.b_event import BEvent


def add_hot():
    yield {'request': BEvent(name="HOT")}
    yield {'request': BEvent(name="HOT")}
    yield {'request': BEvent(name="HOT")}


def add_cold():
    yield {'request': BEvent(name="COLD")}
    yield {'request': BEvent(name="COLD")}
    yield {'request': BEvent(name="COLD")}


def control_temp():
    while True:
        yield {'waitFor': BEvent(name="COLD"), 'block': BEvent(name="HOT")}
        yield {'waitFor': BEvent(name="HOT"), 'block': BEvent(name="COLD")}
