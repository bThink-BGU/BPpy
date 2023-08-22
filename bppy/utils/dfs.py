from bppy.model.b_event import BEvent
from bppy.utils.exceptions import BPAssertionError

class Node:
    def __init__(self, prefix, data):
        self.prefix = prefix
        self.data = data
        self.transitions = {}

    def __key(self):
        return str(self.data)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __str__(self):
        return str(self.prefix) + str(self.data)

    def get_key(self):
        return self.__key()


class DFSBThread:
    def __init__(self, bthread_gen, ess, event_list):
        self.bthread_gen = bthread_gen
        self.ess = ess
        self.event_list = event_list

    def get_state(self, prefix):
        bt = self.bthread_gen()
        s = bt.send(None)
        for e in prefix:
            if s is None:
                break
            if 'block' in s:
                if isinstance(s.get('block'), BEvent):
                    if e == s.get('block'):
                        return None
                else:
                    if e in s.get('block'):
                        return None
            if self.ess.is_satisfied(e, s):
                s = bt.send(e)
        if s is None:
            return {}
        return s

    def run(self):
        init_s = Node(tuple(), self.get_state(tuple()))
        visited = []
        stack = []
        stack.append(init_s)

        while len(stack):
            s = stack.pop()
            if s not in visited:
                visited.append(s)

            for e in self.event_list:
                new_s = Node(s.prefix + (e,), self.get_state(s.prefix + (e,)))
                if new_s.data is None:
                    continue
                s.transitions[e] = new_s
                if new_s not in visited:
                    stack.append(new_s)
        return init_s, visited


class NodeList:
    def __init__(self, nodes, prefix):
        self.nodes = nodes
        self.prefix = prefix
        self.transitions = {}

    def __key(self):
        return ";".join([n.get_key() for n in self.nodes])

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()


class DFSBProgram:
    def __init__(self, bprogram_generator, event_list=None):
        self.bprogram_generator = bprogram_generator
        self.event_list = event_list

    def run(self):
        if self.event_list:
            mapper = {}
            init = []
            n = len(self.bprogram_generator().bthreads)
            ess = self.bprogram_generator().event_selection_strategy
            for i in range(n):
                f = lambda: self.bprogram_generator().bthreads[i]
                dfs = DFSBThread(f, ess, self.event_list)
                init_s, visited = dfs.run()
                mapper[i] = visited
                init.append(init_s)

            init = NodeList(init, tuple())
            visited = []
            stack = [init]
            while len(stack):
                s = stack.pop()
                if s not in visited:
                    visited.append(s)

                for e in ess.selectable_events([x.data for x in s.nodes if x.data is not None]):
                    new_s = []
                    for i, bt_s in enumerate(s.nodes):
                        new_s.append(mapper[i][mapper[i].index(bt_s)].transitions[e])
                    new_s = NodeList(new_s, s.prefix + (e, ))
                    s.transitions[e] = new_s
                    if new_s not in visited:
                        stack.append(new_s)
            return init, visited
        else:
            ess = self.bprogram_generator().event_selection_strategy
            bprogram = self.bprogram_generator()
            bprogram.setup()
            init = NodeList([Node(tuple(), t) for t in self.tickets_without_bt(bprogram.tickets)], tuple())
            visited = []
            stack = [init]
            while len(stack):
                s = stack.pop()
                if s not in visited:
                    visited.append(s)

                for e in ess.selectable_events([x.data for x in s.nodes if x.data is not None]):
                    bprogram = self.bprogram_generator()
                    bprogram.setup()
                    for pre_e in s.prefix:
                        bprogram.advance_bthreads(bprogram.tickets, pre_e)
                    try:
                        bprogram.advance_bthreads(bprogram.tickets, e)
                    except AssertionError:
                        raise BPAssertionError("Assertion error in DFSBProgram", s.prefix + (e,))
                    new_s = NodeList([Node(s.prefix + (e,), t) for t in self.tickets_without_bt(bprogram.tickets)], s.prefix + (e,))
                    s.transitions[e] = new_s
                    if new_s not in visited:
                        stack.append(new_s)
            return init, visited

    @staticmethod
    def tickets_without_bt(tickets):
        return [dict([(k, v) for k, v in t.items() if k != 'bt']) for t in tickets]




