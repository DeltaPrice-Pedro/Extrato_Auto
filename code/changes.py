class Change:
    """
    Classe para registrar alterações (add, update, remove) em referências de contas.
    """
    def __init__(self):
        """
        Inicializa as listas de adição, atualização e remoção.
        """
        self.add = []
        self.updt = {}
        self.remove = []
        pass
    def to_add(self, *args):
        """
        Adiciona um novo item à lista de adição.
        """
        self.add.append(*args)

    def to_updt(self, id, *args):
        """
        Adiciona um item à lista de atualização, indexado pelo id.
        """
        self.updt[id] = args
    
    def to_remove(self, id):
        """
        Adiciona um id à lista de remoção.
        """
        self.remove.append(id)

    def data(self):
        """
        Retorna as listas de adição, atualização e remoção.
        """
        return self.add, self.updt, self.remove