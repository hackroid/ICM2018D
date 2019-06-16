class Edge(object):
    def __init__(
            self,
            eid: int,
            start: int,
            end: int,
            length: int,
            capacity: int
    ):
        self.eid = eid
        self.start = start
        self.end = end
        self.length = length
        self.capacity = int(capacity/10)
        self.max_c = int(capacity) * 2
        self.load = []
        self.done = False
