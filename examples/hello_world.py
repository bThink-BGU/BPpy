from model.b_event import BEvent


def hello():
    yield {'request': BEvent(name="Hello")}


def world():
    yield {'request': BEvent(name="World")}


"""request, waitFor, block, interrupt"""




