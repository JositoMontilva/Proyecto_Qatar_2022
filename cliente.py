class Cliente:
    def __init__(self, nombre, cedula, edad, entradas):
        self.name = nombre
        self.id = cedula
        self.age = edad
        self.ticket_type = entradas
    def comprar_entrada(self, descuento, total, iva, monto_inicial, lista_entradas):
        cont = 0
        print("************ INFORMACIÓN DE COMPRA *************")
        for info in self.ticket_type:
            cont += 1
            if info.code in lista_entradas:
                print(f"Boleto {cont}")
                print("     Precio:", info.price)
                print("     Partido:", info.match)
                print("     Asiento:", info.sit.code)
                print("     Tipo de boleto:", info.sit.type.upper())
                print("     Código boleto:", info.code)
        print("\n")
        print("     Subtotal:", round(monto_inicial, 2))
        print("     Descuento aplicado:", round(descuento, 2))
        print("     Iva (16%):", round(iva, 2))
        print("     Total:", round(total, 2))
        

