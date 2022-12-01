class Entrada:
    def __init__(self, precio, id_match, codigo, asiento, usage):
        self.price = precio
        self.match = id_match
        self.code = codigo
        self.sit = asiento
        self.usage = usage
                    
class EntradaGeneral(Entrada):
    def __init__(self, precio, id_match, codigo, asiento, usage):
        super().__init__(precio, id_match, codigo, asiento, usage)

class EntradaVip(Entrada):
    def __init__(self, precio, id_match, codigo, asiento, usage, productos):
        super().__init__(precio, id_match, codigo, asiento, usage)
        self.bought_products = productos
