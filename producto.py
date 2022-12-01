class Producto:
    def __init__(self, nombre, precio, tipo, adicional, stock):
        self.name = nombre
        self.price = precio
        self.type = tipo
        self.adicional = adicional
        self.quantity = stock

    def mostrar_caracteristicas(self, cont, restaurante):
        print(f"Producto {cont}:")
        print("     Nombre:", self.name)
        print("     Precio:", self.price)
        print("     Tipo:", self.type)
        print("     Restaurante:", restaurante.name)
        print("     En inventario:", self.quantity)
        print("     Adicional:", self.adicional)

class Bebida(Producto):
    def __init__(self, nombre, precio, adicional, stock):
        super().__init__(nombre, precio, "beverages", adicional, stock)
    def mostrar_caracteristicas(self, cont, restaurante):
        super().mostrar_caracteristicas(cont, restaurante)
    def mostrar_al_vender(self, cont):
        super().mostrar_al_vender(cont)
class Alimento(Producto):
    def __init__(self, nombre, precio, adicional, stock):
        super().__init__(nombre, precio, "food", adicional, stock)
    def mostrar_caracteristicas(self, cont, restaurante):
        super().mostrar_caracteristicas(cont, restaurante)
    def mostrar_al_vender(self, cont):
        super().mostrar_al_vender(cont)

class ProductoComprado(Producto):
    def __init__(self, nombre, precio, tipo, adicional, stock, codigo):
        super().__init__(nombre, precio, tipo, adicional, stock)
        self.codigo = codigo
    def mostrar_al_vender(self, cont):
        print(f"Producto {cont}:")
        print("     Nombre:", self.name)
        print("     Precio:", self.price)
        print("     Tipo:", self.type)
        print("     Adicional:", self.adicional)
                        
