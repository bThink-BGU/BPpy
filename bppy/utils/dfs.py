from bppy.model.b_event import BEvent


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
        visited = [s.data for s in visited]
        return init_s, visited

