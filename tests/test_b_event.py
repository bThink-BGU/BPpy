import unittest
import bppy as bp

class TestBEvent(unittest.TestCase):

    def test_mutable_data_bug_fix(self):
        e1 = bp.BEvent("e1")
        e2 = bp.BEvent("e2")

        e1.data["x"] = 42
        assert e2.data == {}

    def test_hash_data_bug_fix(self):
        event1 = bp.BEvent("test", {"a": 1, "b": 2})
        event2 = bp.BEvent("test", {"b": 2, "a": 1})
        assert hash(event1) == hash(event2)