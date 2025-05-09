from types import MethodType


class MooreMachine:
    def __init__(self):
        self._transitions = {
            'P0': {'brake': 'P6'},
            'P6': {'amble': 'P4'},
            'P4': {'snap': 'P1'},
            'P1': {'amble': 'P1', 'brake': 'P5'},
            'P5': {'tail': 'P1', 'snap': 'P7'},
            'P7': {'brake': 'P5', 'snap': 'P2'},
            'P2': {'amble': 'P2', 'snap': 'P3'},
            'P3': {'amble': 'P5'},
        }
        self._outputs = {
            'P0': 'V0', 'P6': 'V1', 'P4': 'V2', 'P1': 'V0',
            'P5': 'V2', 'P7': 'V0', 'P2': 'V0', 'P3': 'V1',
        }
        self._all_words = {w for d in self._transitions.values() for w in d}
        self._state = 'P0'
        self._step = 0
        self._seen_edges = set()
        self._max_out = max(len(d) for d in self._transitions.values())

    def run(self, word):
        if word not in self._all_words:
            return 'unknown'
        nxt = self._transitions[self._state].get(word)
        if nxt is None:
            return 'unsupported'
        self._seen_edges.add((self._state, nxt))
        self._state = nxt
        self._step += 1
        return None

    def get_output(self):
        return self._outputs[self._state]

    def get_step(self):
        return self._step

    def seen_edge(self, p_from, p_to):
        return (p_from, p_to) in self._seen_edges

    def has_max_out_edges(self):
        return len(self._transitions[self._state]) == self._max_out

    def __getattr__(self, item):
        if item not in self._all_words:
            def unknown_method(_self, *_a, **_kw):
                return 'unknown'
            return MethodType(unknown_method, self)

        def transition(_self, *_a, **_kw):
            return _self.run(item)
        return MethodType(transition, self)


def main():
    return MooreMachine()


def test():
    m = main()
    assert m.get_output() == 'V0'
    assert m.run('stare') == 'unknown'
    assert m.run('brake') is None
    assert m.get_output() == 'V1'
    assert m.run('snap') == 'unsupported'
    assert m.run('amble') is None
    assert m.get_output() == 'V2'
    assert m.run('snap') is None
    assert m.get_output() == 'V0'
    assert m.run('amble') is None
    assert m.run('brake') is None
    assert m.has_max_out_edges() is True
    assert m.run('tail') is None
    assert m.run('file') == 'unknown'
    assert m.run('brake') is None
    assert m.run('snap') is None
    assert m.run('snap') is None
    assert m.seen_edge('P2', 'P2') is False
    assert m.run('snap') is None
    assert m.get_output() == 'V1'
    assert m.has_max_out_edges() is False
    assert m.run('brake') == 'unsupported'
    assert m.has_max_out_edges() is False
    assert m.run('amble') is None
    assert m.get_output() == 'V2'
    assert m.seen_edge('P4', 'P1') is True
    assert m.unknown_transition() == 'unknown'
    assert m.snap() is None
    assert m.get_output() == 'V0'
    assert m.seen_edge('P7', 'P2') is True
    assert m.get_step() == 12



def sequence_returns():
    m = main()
    ops = [
        ('run', 'merge'), ('run', 'brake'), ('get_output',), ('has_max_out_edges',),
        ('run', 'amble'), ('get_step',), ('has_max_out_edges',), ('get_output',),
        ('has_max_out_edges',), ('run', 'snap'), ('get_output',), ('run', 'merge'),
        ('has_max_out_edges',), ('run', 'brake'), ('get_output',), ('has_max_out_edges',),
        ('seen_edge', 'P2', 'P2'), ('run', 'file'), ('run', 'snap'), ('get_output',),
        ('run', 'snap'), ('run', 'stand'), ('has_max_out_edges',), ('get_step',),
        ('has_max_out_edges',), ('get_output',), ('run', 'amble'), ('seen_edge', 'P7', 'P2'),
        ('get_output',), ('run', 'snap'), ('get_output',), ('has_max_out_edges',),
        ('get_step',), ('seen_edge', 'P5', 'P1'), ('run', 'amble'), ('seen_edge', 'P4', 'P1'),
        ('get_output',), ('run', 'tail'), ('get_step',), ('seen_edge', 'P7', 'P2'),
        ('get_output',)
    ]
    results = []
    for op in ops:
        if op[0] == 'run':
            results.append(m.run(op[1]))
        elif op[0] == 'get_output':
            results.append(m.get_output())
        elif op[0] == 'has_max_out_edges':
            results.append(m.has_max_out_edges())
        elif op[0] == 'get_step':
            results.append(m.get_step())
        elif op[0] == 'seen_edge':
            results.append(m.seen_edge(op[1], op[2]))
    print(results)


if __name__ == '__main__':
    sequence_returns()
