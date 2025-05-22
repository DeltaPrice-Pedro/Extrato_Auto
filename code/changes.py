class Change:
    def __init__(self):
        self.add = []
        self.updt = {}
        self.remove = []
        pass
    def to_add(self, *args):
        self.add.append(*args)

    def to_updt(self, id, *args):
        self.updt[id] = args
    
    def to_remove(self, id):
        self.remove.append(id)

    def data(self):
        return self.add, self.updt, self.remove