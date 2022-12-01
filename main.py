import requests #Librerías importadas
import random
from partido import Partido
from equipo import Equipo
from producto import Bebida, Alimento, ProductoComprado
from restaurante import Restaurante
from estadio import Estadio
from asientos import Asiento
from cliente import Cliente
import json
from entrada import EntradaGeneral, EntradaVip
from itertools import permutations
from tabulate import tabulate
import pandas as pd
from bokeh.plotting import figure, show

def create_sits(id, ocupacion, calificacion): # Función encargada la cantidad de objetos "Asiento" que sean necesarios para cada partido de acuerdo al aforo del estadio
    return Asiento(id, ocupacion, calificacion)

def return_sit(asiento): #Función que, luego de salir del programa y de transformar todos los objetos a JSON, se encarga de llevar a cabo el proceso contrario pero para los asientos en específico
    return Asiento(asiento["code"], asiento["occupied"], asiento["type"])

def get_dict_as_objects(tipo_dato, info, inventario = 25): #Función encargada de transformar una determinada estructura de datos recibida en un objeto con el cual se trabajará en el resto del programa. Sirve tanto para información recibida de la API como para ciertas otros objetos que surgen a lo largo del desarrollo del programa, por ejemplo para crear el objeto "Producto comprado". A partir de un tipo de dato y de una información que se precise, crea un objeto 
    if tipo_dato == "equipos":
        return Equipo(info["name"], info["flag"], info["fifa_code"], info["group"], info["id"])
    elif tipo_dato == "bebidas":
        return Bebida(info["name"], info["price"], info["adicional"], inventario)
    elif tipo_dato == "alimentos":
        return Alimento(info["name"], info["price"], info["adicional"], inventario)
    elif tipo_dato == "restaurante":
        return Restaurante(info["name"], info["products"])
    elif tipo_dato == "estadios":
        return Estadio(info["id"], info["name"], info["capacity"], info["location"], info["restaurants"])
    elif tipo_dato == "comprado":
        return ProductoComprado(info["name"], info["price"], info["type"], info["adicional"], info["quantity"], info["codigo"])
def get_partido_as_objects(info, asientos, home_team, away_team, estadio, asistencia = 0, ventas = 0, gastos_totales_vip = 0): #Función que se encarga de transformar la estructura de datos referente a los partidos recibida de la API en objetos. Se hace una función aparte ya que las características del objeto Partido diseñado por mí difieren en cierta manera de la de los demás objetos recibidos desde la API
    return Partido(home_team, away_team, info["date"], info["stadium_id"], estadio, info["id"], asientos, asistencia, ventas, gastos_totales_vip)

def crear_entrada(id_match, code, sit): #Función encargada de crear una entrada en el momento en el que cliente, al estar eligiendo un asiento en un determinado estadio de un partido, se decide por un asiento en particular. Si el asiento esta en la zona VIP entonces la entrada será VIP; pro el contrario, si es general, entonces será una entrada general
    if sit.type == "vip": 
        return EntradaVip(120, id_match,code, sit, False, [])
    elif sit.type == "general":
        return EntradaGeneral(50, id_match, code, sit, False)

def return_entry(info): #Luego de salir del sistema, reinicializar y cargar los datos de los archivos JSON, se observará que la entradas que poseen los clientes tendrán una serie de valores para sus atributos distintos a los de la función pasada. Por ello se hace una función aparte para "retornar la entrada" al cliente
    if info["sit"].type == "vip": 
        return EntradaVip(info["price"], info["match"],info["code"], info["sit"], info["usage"], info["bought_products"])
    elif info["sit"].type == "general":
        return EntradaGeneral(info["price"], info["match"],info["code"], info["sit"], info["usage"])

def mostrar_partidos(partidos): #Función encargada de mostrar la información necesaria sobre un partido cualquiera en la consola
    print("     Equipo local:", partidos.home_team.name)
    print("     Equipo visitante:", partidos.away_team.name)
    print("     Fecha del juego:", partidos.date)
    print("     Estadio donde se jugará:", partidos.stadium.name)
    print("     Id del juego:", partidos.id, "\n")

def factorial(numero): #Función encargada de determinar si un numero es factorial. Se utiliza recursividad
  if numero == 0 or numero == 1:
    return numero
  return numero * factorial(numero - 1)

def numero_vampiro(numero): # Función encargada de determinar si un número cualquiera es o no vampiro. A partir de lo que determine, se devolverá un True si lo es, y si no, pues, un False
    if len(numero) > 1:
        cont = 0
        for i in permutations(numero, len(numero)):
            mitad = int(len(numero)/ 2)
            lista_1 = i[:mitad]
            lista_2 = i[mitad:]
            lista_1 = "".join(lista_1)
            lista_2 = "".join(lista_2)
            if (int(lista_2) * int(lista_1)) == int(numero):
                cont += 1
                return True
        if cont == 0:
            return False
    else:
        return False

def show_sits(lista_partidos, partido_elegido): #Función que integra bastantes procesos. En primer lugar se encarga de mostrarle al cliente el mapa del estadio junto a las gradas y los asientos libres y ocupados que en estas últimas haya. Se valida que un cliente no pueda elegir un asiento fuera del rango y que además no pueda elegir un asiento ya ocupado. Finalmente, el cliente debe determinar el asiento de su elección y entonces reafirmar que el tipo de asiento que haya elegido sea el de su elección (VIP o GENERAL). Además, se devuelve el objeto del asiento para poder utilizarlo luego en el desarrollo del programa
    puestos_no_posibles = []
    puestos_posibles = []
    cont = 0
    print("\n                                                           GENERAL")
    for puestos in lista_partidos:
        if puestos.id == partido_elegido:
            for codigos in puestos.sits:
                if cont % 10 == 0:
                    print("\n", end= "                  ")
                if codigos.occupied == True and codigos.type == "general":
                    cont += 1
                    general_final = codigos.code
                    puestos_no_posibles.append(codigos.code)
                    print("|_xx_|", end=" - ")
                elif codigos.occupied == False and codigos.type == "general":
                    cont += 1
                    general_final = codigos.code
                    if len(str(codigos.code)) == 1: 
                        puestos_posibles.append(codigos.code)
                        print("|_" + str(codigos.code) + " _|", end=" - ")
                    else:
                        puestos_posibles.append(codigos.code)
                        print("|_" + str(codigos.code) + "_|", end=" - ")
                elif codigos.type == "vip":
                    break
    print("\n")
    with open("Proyecto_Qatar2022/campo.txt", "r") as uy:
        print(uy.read())
        uy.close()
    print("\n                                                           VIP")
    for puestos in lista_partidos:
        if puestos.id == partido_elegido:
            vip_inicial = puestos.sits[cont].code
            for codigos in puestos.sits:
                vip_final = codigos.code
                if codigos.type == "vip":
                    if cont % 10 == 0:
                        print("\n", end= "                  ")
                    cont += 1
                    if codigos.occupied == True:
                        puestos_no_posibles.append(codigos.code)
                        print("|_xx_|", end=" - ")
                    else:
                        puestos_posibles.append(codigos.code)
                        print("|_" + str(codigos.code) + "_|", end=" - ")
    print("\n")
    asiento = input(f"Elija el asiento de preferencia:\nTenga en cuenta que de los asientos 1 al {general_final} los asientos son generales; y, de los asientos {vip_inicial} al {vip_final} los asientos son VIP\n--> ")
    while not asiento.isnumeric() or int(asiento) not in puestos_posibles or int(asiento) in puestos_no_posibles:
        print("El puesto al parecer ya está ocupado\nElija otro:\n")
        asiento = input("Elija el asiento de preferencia:\n--> ")
    if int(asiento) >= 1 and int(asiento) <= int(general_final): 
        seguridad_asiento = textos_validador(["s", "n"], "¿Está seguro que desea una entrada general? (S/N)): ")
        if seguridad_asiento == "s":
            for puestos in lista_partidos:
                if puestos.id == partido_elegido:
                    for codigos in puestos.sits:
                        if int(codigos.code) == int(asiento):
                            return codigos
        else:
            return None
    elif int(asiento) >= int(vip_inicial) and int(asiento) <= int(vip_final): 
        seguridad_asiento = textos_validador(["s", "n"], "¿Está seguro que desea una entrada vip? (S/N)): ")
        if seguridad_asiento == "s":
            for puestos in lista_partidos:
                if puestos.id == partido_elegido:
                    for codigos in puestos.sits:
                        if int(codigos.code) == int(asiento):
                            return codigos
        else:
            return None


def romper_true(texto_input): # Función encargada de romper un bucle infinito del tipo "While True". Tiene usos muy variados. Por ejemplo para determinar si un cliente no quiere comprar más boletos
    decision = textos_validador(["s", "n"], texto_input)
    if decision == "s":
        return True
    return False

def validador_numeros(texto_input, numero_mayor = 10000000000, texto_mientras = "OPCIÓN NO VÁLIDA\nIntente nuevamente:\n", numero_menor = 1): #Funciión encargada de validar que el dato ingresado por el cliente sea numérico y que además se encuentre dentro de un rango especificado por el programador
    criterio = input(texto_input)
    while not criterio.isnumeric() or int(criterio) > numero_mayor or int(criterio) < numero_menor:
        print("\n", texto_mientras)
        criterio = input(texto_input)
    return criterio


def facturacion(vampiro, precio): #Función encargada de calcular y devolver los valores correspondientes al precio final, el descuento, y el IVA del que un producto será objeto
    descuento = 0
    if vampiro:
        print("Ha recibido un descuento del 50% por ser su cédula un número vampiro.")
        descuento = precio * 0.50
    precio_final = precio - descuento
    return precio_final + (precio_final * 0.16), descuento, precio_final * 0.16

def textos_validador(lista_opciones, texto_input, texto_mientras = "Ingresa una opción válida:\n"): #Función encargada de validar que el dato ingresado sea alfabético y que además pide una lista de opciones a partir de la cual corrobora que no cualquier tipo de dato sea ingresado, sino solo un dato perteneciente a una lista de opciones
    opcion = input(texto_input).lower()
    while opcion not in lista_opciones:
        print("\n", texto_mientras)
        opcion = input(texto_input).lower()
    return opcion
    
def numero_perfecto(numero):#Función encargada de determinar si un número es perfecto o no
    divisores = []
    for i in range(1, numero):
        if (numero % i) == 0:
            divisores.append(i)
    if sum(divisores) == numero:
        return True    
    return False 

def elegir_partido(lista_partidos):#Función encargada de mostrarle al cliente los partidos de los que se dispone para que, a partir de allí, decida a cuál partido desea ir. Se crea un método en el objeto Partido para mostrar la información más relevante de los partidos
    print("Se dispone de los siguientes partidos:\n")
    cont = 0
    for partido in lista_partidos:
        cont += 1
        print(f"Partido {cont}")
        mostrar_partidos(partido)
    id = validador_numeros("Indique el id del partido al que desea asistir\n--> ", "48")
    return id

def corroborar_autenticidad(codigo, lista_entradas_por_usar, las_entradas_usadas): #Función encargada de corroborar que un boleto sea auténtico. A partir de los datos obtenidos determina si el código del boleto ingresado por el cliente se corresponde con uno de los boletos pertenecientes a su persona
        cont = 0
        for entradas in lista_entradas_por_usar:
            if entradas == codigo:
                cont += 1
                print("\nEl ticket es válido. El usuario puede ingresar al recinto")
                lista_entradas_por_usar.remove(codigo)
                las_entradas_usadas.append(codigo)
                return True
        if cont == 0:
            for entradas in las_entradas_usadas:
                if entradas == codigo:
                    cont += 1
                    print("\nEl código ya fue utilizado. El ticket no es válido.")
                    return False
        if cont == 0:
            print("\nEl código no existe. El ticket no es válido.")
            return False

def mostrar_cliente(cliente, cont): #Muestra pr consola la información más relevante de un cliente
    print(f"Cliente N°{cont}:")
    print("     Nombre:", cliente.name)
    print("     Cédula:", cliente.id)
    print("     Edad:", cliente.age)
    print("     Cantidad de boletos:", len(cliente.ticket_type))

def get_from_api(url): #Función sustancial. Se encarga de transformar los datos de la API recibida y luego los lleva a formato JSON. Se utiliza cada vez que los datos del sistema sean reiniciados
    info_a_tomar = requests.get(url)
    datos = info_a_tomar.json()
    return datos

def producto_validador(lista_productos, texto_input, edad_cliente): #Función encargada de validar que un cliente menor de edad no pueda comprar bebidas alocohólicas
    decision = textos_validador(lista_productos, "Elija el producto que desea comprar:\n--> ", "ERROR\nDebe ingresar uno de los productos ofertados en el restaurante")
    if int(edad_cliente) < 18 and decision == "beer":
        print("Usted es menor de edad y no puede consumir bebidas alcohólicas")
        return producto_validador(lista_productos, texto_input, edad_cliente)
    return decision

def return_client(info): #Función encargada de volver a crear los clientes a partir de los archivos JSON utilizados para guardar los datos del sistema
    return Cliente(info["name"], info["id"], info["age"], info["ticket_type"])

def create_client(lista_clientes): #Función encargada de crear un cliente cada vez que, en el módulo 2, sea elegida la opción 1. Además valida que dos objetos clientes distintos con una misma cédula puedan ser creados. De no ser así, retorna la cédula del cliente para así trabajar con ella en el desarrollo del programa
    nombre = input("Nombre cliente: ")
    while not nombre.isalpha():
        print("Introduce un nombre con caractéres válidos\n")
        nombre = input("Nombre cliente: ")
    cedula_cliente = input("Cédula cliente: ")
    cedulas = []
    for cliente in lista_clientes:
        cedulas.append(cliente.id)
    while cedula_cliente in cedulas:
        print("Esa cédula ya existe, si lo que desea comprar otra entrada presione X, ingrese nuevamente al módulo, y seleccione la opción correspondiente a comprar nuevas entradas")
        cedula_cliente = input("Cédula cliente (o X para salir): ")
        if cedula_cliente.lower() == "x":
            break
    if cedula_cliente != "x":
        while not cedula_cliente.isnumeric():
            print("Introduce una cédula válida. Sólo Números\n")
            cedula_cliente = input("Cédula cliente: ")
        edad = validador_numeros("Edad cliente: ")
        lista_clientes.append(Cliente(
            nombre,
            cedula_cliente,
            edad,
            []
        ))
        return cedula_cliente
    return 0
    
def main(): #Función main donde todo el código espinal se verá plasmado
    productos_iniciales = []
    with open("Proyecto_Qatar2022/datos_clientes.json", "r") as cy: #Se cargan datos desde el archivo JSON creado para estos
        clientes_reading = json.loads(cy.read())
        cy.close()
    with open("Proyecto_Qatar2022/datos_base.json", "r") as by:#Se cargan datos desde el archivo JSON creado para estos
        base_reading = json.loads(by.read())
        by.close()
    with open("Proyecto_Qatar2022/datos_extra.json", "r") as ey:#Se cargan datos desde el archivo JSON creado para estos
        extra_reading = json.loads(ey.read())
        ey.close()
    if base_reading == []:
        partidos_por_jugar = get_from_api("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json") #Obtención de la información contenida en la API. Se tranforma tal información a una edd
        equipos_lista = get_from_api("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json")#Obtención de la información contenida en la API. Se tranforma tal información a una edd
        estadios_lista = get_from_api("https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json")#Obtención de la información contenida en la API. Se tranforma tal información a una edd
        for estadio in estadios_lista: # Transformación de las edd obtenidas a partir de las API anteriormente en objetos de acuerdo al objeto que se quiera crear.
            for restaurante in estadio["restaurants"]:
                for producto in restaurante["products"]:
                    if producto["name"].lower() not in productos_iniciales:
                        productos_iniciales.append(producto["name"].lower())
                    if producto["type"] == "food":
                        restaurante["products"][restaurante["products"].index(producto)] = get_dict_as_objects("alimentos", producto)
                    else:
                        restaurante["products"][restaurante["products"].index(producto)] = get_dict_as_objects("bebidas", producto)
                estadio["restaurants"][estadio["restaurants"].index(restaurante)] = get_dict_as_objects("restaurante", restaurante)
        for equipo in equipos_lista: # Transformación de las edd obtenidas a partir de las API anteriormente en objetos de acuerdo al objeto que se quiera crear.
            equipos_lista[equipos_lista.index(equipo)] = get_dict_as_objects("equipos", equipo)
        for estadio in estadios_lista: # Transformación de las edd obtenidas a partir de las API anteriormente en objetos de acuerdo al objeto que se quiera crear.
            estadios_lista[estadios_lista.index(estadio)] = get_dict_as_objects("estadios", estadio)
        for partido in partidos_por_jugar: # Transformación de las edd obtenidas a partir de las API anteriormente en objetos de acuerdo al objeto que se quiera crear. en este caso particular, se hacen referencias directas a los objetos en ciertos atributos para los partidos, por ejemplo para los asiento, para el equipo local, visitante, y para el estadio y toda la información que él contiene
            capacidad = 1
            for estadio in estadios_lista:
                if estadio.id == partido["stadium_id"]:
                    estadio_a_jugar = estadio
                    capacidad_general = estadio.capacity[0]
                    capacidad_vip = estadio.capacity[1]
            for equipo in equipos_lista:
                if equipo.name == partido["home_team"]:
                    home_team = equipo
                if equipo.name == partido["away_team"]:
                    away_team = equipo
            asientos = []
            for i in range(1, capacidad_general + 1):
                asientos.append(create_sits(i, False, "general"))
            for i in range(capacidad_general + 1, capacidad_general + capacidad_vip + 1):
                asientos.append(create_sits(i, False, "vip"))
            partidos_por_jugar[partidos_por_jugar.index(partido)] = get_partido_as_objects(partido, asientos, home_team, away_team, estadio_a_jugar)
    else: #Este "else" tiene básicamente el mismo proósito que las líneas de código de arriba, solo que para este particular sólo se ejecutarán las líneas en caso de que el programa se cierre y la información tratada a lo largo de él no sea reiniciada. De no ser así, se ejecutarán las de arriba
        equipos_lista, partidos_por_jugar, estadios_lista = base_reading[0], base_reading[1], base_reading[2]
        for equipo in equipos_lista:
            equipos_lista[equipos_lista.index(equipo)] = get_dict_as_objects("equipos", equipo)
        for estadio in estadios_lista:
            for restaurante in estadio["restaurants"]:
                for producto in restaurante["products"]:
                    if producto["type"] == "food":
                        restaurante["products"][restaurante["products"].index(producto)] = get_dict_as_objects("alimentos", producto, producto["quantity"])
                    else:
                        restaurante["products"][restaurante["products"].index(producto)] = get_dict_as_objects("bebidas", producto, producto["quantity"])
                estadio["restaurants"][estadio["restaurants"].index(restaurante)] = get_dict_as_objects("restaurante", restaurante)
        for estadio in estadios_lista:
            estadios_lista[estadios_lista.index(estadio)] = get_dict_as_objects("estadios", estadio)
        for partido in partidos_por_jugar:
            capacidad = 1
            for estadio in estadios_lista:
                if estadio.id == partido["stadium_id"]:
                    estadio_a_jugar = estadio
                    for limites in estadio.capacity:
                        capacidad *= limites
            for equipo in equipos_lista:
                if equipo.name == partido["home_team"]["name"]:
                    home_team_new = equipo
                if equipo.name == partido["away_team"]["name"]:
                    away_team_new = equipo
            asientos = []
            for i in partido["sits"]:
                asientos.append(create_sits(i["code"], i["occupied"], i["type"]))
            partidos_por_jugar[partidos_por_jugar.index(partido)] = get_partido_as_objects(partido, asientos, home_team_new, away_team_new, estadio_a_jugar, partido["asistance"], partido["sell"], partido["spends_total_vip"])
    if extra_reading == []: #Estas lista creadas a continuación contendrán información de importancia espinal para validar ciertos datos y que no ocurran estrépitos por un malentendido entre los datos del sistema. Por ejemplo, se corroba cuáles entradas han sido usada y cuáles están por usar
        productos_dict = {}
        for prod in productos_iniciales:
            productos_dict[prod] = 0 
        entradas_por_usar = []
        codigos_que_intervienen_vip = []
        entrada_usadas = []
        entradas_que_intervienen_vip = []
    else: # Se ejecuta en caso de que, al cerrar, no se reinicien los datos del sistema
        productos_dict = extra_reading[0]
        entradas_por_usar = extra_reading[1]
        codigos_que_intervienen_vip = extra_reading[2]
        entrada_usadas = extra_reading[3]
        entradas_que_intervienen_vip = extra_reading[4]
    if clientes_reading == []: #Lista que contendrá los distintos clientes que se vayan creando a lo largo del programa
        clientes = []
    else: #Aquí, se vuelven a crear los objetos Cliente a partir del archivo JSON preexistente encargado de guardar sus datos
        clientes = clientes_reading
        for cli in clientes:
            for tickets in cli["ticket_type"]:
                tickets["sit"] = return_sit(tickets["sit"])
                if tickets["sit"].type == "vip":
                    for productos in tickets["bought_products"]:
                        if productos["type"] == "food":
                            tickets["bought_products"][tickets["bought_products"].index(productos)] = get_dict_as_objects("comprado", productos,)
                        else:
                            tickets["bought_products"][tickets["bought_products"].index(productos)] = get_dict_as_objects("comprado", productos)
                cli["ticket_type"][cli["ticket_type"].index(tickets)] =  return_entry(tickets)
            clientes[clientes.index(cli)] = return_client(cli)
    contador_uso_multiple = 0 #Contador que servirá para múltiples propósitos a lo largo del programa y que constantemente se igualará a cero con el propósito de reutilizarlo
    condicion_salida = "n" #Condición hardcodeada que asegura que, al reiniciar los datos del sistema, los archivos JSON que contenían información queden vacíos
    while True: #Inicio del programa de gestión de Qatar 2022
        decision_init = validador_numeros("\nBienvenido a Qatar 2022! La fiebre mundialista hierve por las venas! Qué desea hacer:\n1-Gestionar partidos y estadios\n2-Gestionar venta de entradas\n3-Gestionar asistencia a partidos\n4-Gestionar restaurantes\n5-Gestionar ventas de restaurantes\n6-Ver indicadores de gestión (Estadísticas)\n7-Salir del Sistema\n8-Reiniciar datos del sistema y salir\n--> ", 8, "ELIJA UNA OPCIÓN VÁLIDA. ESTAS VAN DEL 1 AL 9") #Decisión inicial a partir de la cual el cliente decidirá qué información desea gestionar con el programa
        if decision_init == "1": #Se gestionan los partidos
            decision_1_1 = validador_numeros("¿Bajo qué filtro deseas buscar un partido?\n1-Por país\n2-Por estadio\n3-Por fecha\n -->", 3) #Se gestionan los partidos de acuerdo al criterio que indique el usuario
              # ------------------------------------------------------------------------------------------------------
            if decision_1_1 == "1": #Partidos de acuerdo a algún equipo
                print("Los siguientes equipos siguen en el ruedo:\n")
                equipos_valid = []
                for equipos in equipos_lista:
                    print("--", equipos.name)
                    equipos_valid.append(equipos.name.lower())
                print("\n")
                decision_1_1_1 = textos_validador(equipos_valid,"Eliga el nombre del país cuyos partidos desea evaluar\n--> ", "ERROR\nDebe ingresar el nombre de una de las selecciones participantes en Qatar 2022") # El usuario debe especificar el equipo textualmente con su nombre y luego se valida que exista o no tal equipo
                print(f"{decision_1_1_1.capitalize()} jugará los siguientes partidos:\n") # Se muestran los partidos
                for partidos in partidos_por_jugar:
                    if partidos.home_team.name.lower() == decision_1_1_1 or partidos.away_team.name.lower() == decision_1_1_1:
                        contador_uso_multiple += 1
                        print(f"Partido {contador_uso_multiple}:")
                        mostrar_partidos(partidos)
                      # ------------------------------------------------------------------------------------------------------
            elif decision_1_1 == "2": #Partidos de acuerdo a algún estadio
                print("Se jugará en los siguientes estadios:\n")
                estadios_valid = []
                for estadios in estadios_lista:
                    print(f"{estadios.id}-{estadios.name}")
                    estadios_valid.append(estadios.name.lower())
                print("\n")
                decision_1_1_2 = textos_validador(estadios_valid, "Eliga el nombre del estadio cuyos partidos desea evaluar\n--> ", "ERROR\nDebe ingresar el nombre de uno de los estadios sede de Qatar 2022") # El usuario debe especificar el estadio textualmente con su nombre y luego se corrobora que exista o no tal estadio
                for estadios in estadios_lista:
                    if estadios.name.lower() == decision_1_1_2:
                        print(f"En el {decision_1_1_2.capitalize()} se jugarán los siguientes partidos:\n") #Se muestran los partidos
                for partidos in partidos_por_jugar:
                    if partidos.stadium.name.lower() == decision_1_1_2:
                        contador_uso_multiple += 1
                        print(f"Partido {contador_uso_multiple}:")
                        mostrar_partidos(partidos)
                      # ------------------------------------------------------------------------------------------------------
            elif decision_1_1 == "3": #Partidos de acuerdo a alguna fecha
                print("En las siguientes fechas habrán juegos:\n")
                fechas = []
                for partidos in partidos_por_jugar:
                    partidos_fecha = partidos.date.split(" ")
                    if partidos_fecha[0] not in fechas:
                        fechas.append(partidos_fecha[0])
                for fecha in fechas:
                    print(fecha, end= " -- ")
                print("\n")
                decision_1_1_3 = input("Eliga la fecha cuyos partidos desea evaluar (con '/' entre los números)\n--> ") # El usuario debe especificar la fecha textualmente y luego se corrobora que exista o no tal fecha 
                decision_1_1_3_validar = "".join(decision_1_1_3.split("/"))
                while not decision_1_1_3_validar.isnumeric():
                    print("Debe ingresar números")
                    decision_1_1_3 = input("Fecha cuyos partidos desea evaluar\n--> ")
                    decision_1_1_3_validar = "".join(decision_1_1_3.split("/"))
                print(f"El {decision_1_1_3} se jugarán los siguientes partidos:\n") #Se muestran los partidos que hay o no en una fecha
                for partidos in partidos_por_jugar:
                    if decision_1_1_3 in partidos.date:
                        contador_uso_multiple += 1
                        print(f"Partido {contador_uso_multiple}:")
                        mostrar_partidos(partidos)
                if contador_uso_multiple == 0:
                    print(f"Al parecer en la fecha que eligió: {decision_1_1_3} no habrán juegos o ya se jugaron los mismos.\n")
                else:
                    contador_uso_multiple = 0
                    # ------------------------------------------------------------------------------------------------------
        elif decision_init == "2": #Gestión de clientes: se crean nuevos clientes con sus respectivo boletos o, en su defecto, un cliente preexistente compra más boletos
            entradas_cliente = [] #Sirve esta lista para que, al facturar, solo se cuenten aquella entradas compradas en la vuelta en desarrollo y no otras que un cliente pueda poseer de antes
            decision_2_1 = validador_numeros("Indique qué desea hacer\n1-Crear un nuevo cliente\n2-Añadir nuevas entradaas a un cliente\n--> ", 2)
            if decision_2_1 == "1": # Se crea un nuevo cliente
                cedula = create_client(clientes) # Se crea un cliente, en la función se validará si su cédula es preexistente o no
                for cliente in clientes:
                    if cedula == cliente.id:
                        while True:
                            for partidos in partidos_por_jugar:
                                mostrar_partidos(partidos)
                            id_match = validador_numeros("Indique el id del partido al que desea asistir:\n--> ", 48, "ERROR. ESTE VALOR DEBE IR DESDE EL 1 AL 48") # Se selecciona el partido deseado
                            asiento = show_sits(partidos_por_jugar, id_match) # Se selecciona el asiento deseado
                            if asiento != None:
                                code = random.randint(1000000,10000000) #Se crea un código que identificará a la entrada a lo largo del desarrollo del programa
                                while code in entradas_por_usar or code in entrada_usadas:
                                    code = random.randint(1000000,10000000)
                                entradas_por_usar.append(code) #Se agrega a entradas por usar
                                entradas_cliente.append(code) #Se indica que esta entrada solo corresponderá a esta vuelta
                                cliente.ticket_type.append(crear_entrada(id_match,code, asiento))
                            if not romper_true("¿Desea comprar otra entrada? (S/N))\n--> "):
                                break
                        if entradas_cliente != []: #Siempre y cuando se hayan comprado realmente boletos
                            monto_total = 0
                            descuento_total = 0
                            iva_total = 0
                            total_total = 0
                            for precios in cliente.ticket_type: # Se sacan los descuento, el subtotal, el IVA y el monto final a partir de las entradas compradas por el cliente. Para ello se usan contadores que cada vuelta se igualarán a cero. Además, el atributo del precio de la entrada se cambiará a nivel de objeto ya en manos del cliente para así facilitar las estadísticas luego
                                if precios.code in entradas_cliente:
                                    monto_total_parcial = precios.price
                                    total_parcial, descuento_parcial, iva_parcial = facturacion(numero_vampiro(cliente.id), monto_total_parcial)
                                    precios.price = total_parcial
                                    total_total += total_parcial
                                    iva_total += iva_parcial
                                    descuento_total += descuento_parcial
                                    monto_total += monto_total_parcial
                            if numero_vampiro(cliente.id): #¿Es número vampiro? Se evalua
                                print("Felicitaciones! Tiene un 50 por ciento de descuento en su compra")
                            cliente.comprar_entrada(descuento_total, total_total, iva_total, monto_total, entradas_cliente) #Se muestra por consola las entradas compradas y el monto total a pagar si se desea continuar
                            se_compra = textos_validador(["s", "n"], "¿Desea proceder?\n--> ") # el cliente decide si proceder o no
                            if se_compra == "s": #El puesto a nivel partido pasa a estar ocupado si el cliente decide proseguir. Además, se le suma al atributo de ventas del partido en cuestión la cantidad de tickets que se hayan comprado para él
                                print("Compra exitosa!!")
                                for puestos in partidos_por_jugar:
                                    for entradas in cliente.ticket_type:
                                        if entradas.match == puestos.id:
                                            for puesto in puestos.sits:
                                                if int(entradas.sit.code) == puesto.code:
                                                    puesto.occupied = True
                                            if int(entradas.code) in entradas_cliente:
                                                puestos.sell += 1
                            else: #El cliente será borrado de la lista de clientes si no prosigue
                                print("Será en una siguiente oportunidad.")
                                clientes.remove(cliente)
                        else:
                            print("Será en una siguiente oportunidad.")
                # ----------------------------------------------------------------------------------------
            elif decision_2_1 == "2": #Un cliente preexistente decide comprar nuevamente otras entradas
                contador_uso_multiple = 0
                cedula_cliente = validador_numeros("Introduzca la cédula de un cliente para evaluar su existencia\n--> ", 10000000000, "INTRODUZCA UN NÚMERO")
                for cliente in clientes:
                    if cliente.id == cedula_cliente:
                        print(f"Bienvenido de nuevo {cliente.name.capitalize()}")
                        contador_uso_multiple += 1
                        while True:
                            for partidos in partidos_por_jugar:
                                mostrar_partidos(partidos)
                            id_match = validador_numeros("Indique el id del partido al que desea asistir:\n--> ", 48, "ERROR. ESTE VALOR DEBE IR DESDE EL 1 AL 48")
                            asiento = show_sits(partidos_por_jugar, id_match)
                            if asiento != None:
                                code = random.randint(1000000,10000000)
                                while code in entradas_por_usar or code in entrada_usadas:
                                    code = random.randint(1000000,10000000)
                                entradas_por_usar.append(code)
                                entradas_cliente.append(code)
                                cliente.ticket_type.append(crear_entrada(id_match,code, asiento))
                            if not romper_true("¿Desea comprar otra entrada? (S/N))\n--> "):
                                break
                        if entradas_cliente != []:
                            monto_total = 0
                            descuento_total = 0
                            iva_total = 0
                            total_total = 0
                            for precios in cliente.ticket_type: # Se sacan los descuento, el subtotal, el IVA y el monto final a partir de las entradas compradas por el cliente. Para ello se usan contadores que cada vuelta se igualarán a cero. Además, el atributo del precio de la entrada se cambiará a nivel de objeto ya en manos del cliente para así facilitar las estadísticas luego
                                if precios.code in entradas_cliente:
                                    monto_total_parcial = precios.price
                                    total_parcial, descuento_parcial, iva_parcial = facturacion(numero_vampiro(cliente.id), monto_total_parcial)
                                    precios.price = total_parcial
                                    total_total += total_parcial
                                    iva_total += iva_parcial
                                    descuento_total += descuento_parcial
                                    monto_total += monto_total_parcial
                            if numero_vampiro(cliente.id): #¿Es número vampiro? Se evalua
                                print("Felicitaciones! Tiene un 50 por ciento de descuento en su compra")
                            cliente.comprar_entrada(descuento_total, total_total, iva_total, monto_total, entradas_cliente)
                            se_compra = textos_validador(["s", "n"], "¿Desea proceder?\n--> ")
                            if se_compra == "s":
                                print("Compra exitosa!!") # el cliente decide si proceder o no
                            if se_compra == "s": #El puesto a nivel partido pasa a estar ocupado si el cliente decide proseguir. Además, se le suma al atributo de ventas del partido en cuestión la cantidad de tickets que se hayan comprado para él 
                                for puestos in partidos_por_jugar:
                                    for entradas in cliente.ticket_type:
                                        if entradas.match == puestos.id:
                                            for puesto in puestos.sits:
                                                if int(entradas.sit.code) == puesto.code:
                                                    puesto.occupied = True
                                            if int(entradas.code) in entradas_cliente:
                                                puestos.sell += 1
                            else:
                                print("Será en una siguiente oportunidad.") # En este caso no se borra al objeto cliente en sí. Eso sería erróneo. Sólo se borran aquellas entradas que hayan sido pretendidas en esta vuelta y no las demás
                                print(entradas_cliente)
                                for entradas in entradas_cliente:
                                    for tickets in cliente.ticket_type:
                                        if tickets.code == entradas:
                                            cliente.ticket_type.remove(tickets)
                if contador_uso_multiple == 0: # Si el cliente con tal cédula no existe, se notifica
                    print("El cliente no ha sido encontrado.")
                                  # ------------------------------------------------------------------------------------------------------
        elif decision_init == "3": #Se corrobora la autenticidad de un boleto al entrar a un estadio
            contador_uso_multiple = 0
            cedula_cliente = validador_numeros("Introduzca su cédula para conocer qué boletos tiene a su disposición:\n--> ", 10000000000, "INTRODUZCA UN NÚMERO")
            for cliente in clientes:
                if cliente.id == cedula_cliente:
                    for tickets in cliente.ticket_type:
                        if tickets.usage == False: #Siempre y cuando la entrada no haya sido utilizada previamente, entonces el cliente podrá hacer uso de una entrada
                            print(f"Usted dispone de las siguientes entradas:")
                            break
                    for tickets in cliente.ticket_type:
                        if tickets.usage == False:
                            contador_uso_multiple += 1
                            print(f"Boleto {contador_uso_multiple}") #Se muestran por consola el código de los boletos, el partido al que corresponden y el tipo de boleto que es
                            print(f"    Codigo Boleto: {tickets.code}       Tipo: {tickets.sit.type}        Partido: {tickets.match}")
            code_autenticity = 0
            for cliente in clientes: #En caso se coincidir la cédula introducida con la de un cliente, entonces se valida que tal cliente posea el código de la entrada ingresado a través de la consola por el usuario
                if cliente.id == cedula_cliente and contador_uso_multiple != 0:
                    code_autenticity = validador_numeros("Se corroborará la autenticidad de un boleto. Debe indicar a continuación el código del boleto para llevar a cabo tal proceso:\n--> ", 10000000, "INTRODUZCA UNO DE LOS NÚMEROS CORRESPONDIENTES A SUS BOLETOS")
            if code_autenticity != 0:
                if corroborar_autenticidad(int(code_autenticity), entradas_por_usar, entrada_usadas): #En caso de ser verídica la entrada y no utilizada anteriormente, entonces, a nivel de partido, el atributo de este último objeto correspondiente a la asistencia aumentará en uno
                    for cliente in clientes:
                        for tickecito in cliente.ticket_type:
                            if int(code_autenticity) == tickecito.code and tickecito.usage == False:
                                contador_uso_multiple += 1
                                tickecito.usage = True
                                for partidazo in partidos_por_jugar:
                                    if tickecito.match == partidazo.id:
                                        partidazo.asistance += 1
                                        break
            if contador_uso_multiple == 0: # De no existir boletos a nombre del cliente, pues se le notificará por consola
                print("No hay boletos a su nombre")
                  # ------------------------------------------------------------------------------------------------------
        elif decision_init == "4": #Gestión de los productos 
            productos_posibles = []
            partido_productos = validador_numeros("Indique el id del partido en el que se encuentra para hallar el inventario actualizado de los restaurantes\n--> ", 48, "ERROR: DEBE INDICAR UN ID DE PARTIDO ENTRE EL 1 Y EL 48") #Primeramente, el usuario debe indicar en qué estadio se encuentra para entonces mostrar la oferta
            for partidos in partidos_por_jugar:
                if partidos.id == partido_productos:
                    contador_uso_multiple += 1
                    decision_4_1 = validador_numeros("¿Bajo qué filtro deseas buscar un producto?\n1-Por nombre\n2-Por tipo\n3-Por rango de precio\n--> ", 3, "INGRESE UN VALOR VÁLIDO ENTRE EL 1 Y EL 3")  # Debe decidir bajo qué filtro desea buscar un producto en tal estadio
                      # ------------------------------------------------------------------------------------------------------
                    if decision_4_1 == "1":  #Por nombre
                        for i in partidos.stadium.restaurants:
                            for producto in i.products:
                                if producto.name.lower() not in productos_posibles:
                                    productos_posibles.append(producto.name.lower())
                        contador_uso_multiple = 0
                        print("Se dispone de los siguientes productos:")
                        for i in productos_posibles:
                            contador_uso_multiple += 1
                            print(f"{contador_uso_multiple}-{i.capitalize()}")
                        contador_uso_multiple = 0
                        decision_4_1_1 = textos_validador(productos_posibles, "Indique el nombre del producto que busca\n--> ", "Debe ingresar el nombre de uno de los productos ofertados") # Se muestran los nombre de los productos ofertados en ese estadio y a partir de allí el cliente debe indicar qué producto desea conocer
                        print(f"La información para el producto: {decision_4_1_1.capitalize()} es la siguiente:\n")
                        for restaurantes in partidos.stadium.restaurants:
                            for productos in restaurantes.products:
                                if decision_4_1_1 == productos.name.lower() and productos.quantity != 0:
                                    contador_uso_multiple += 1
                                    productos.mostrar_caracteristicas(contador_uso_multiple, restaurantes)
                              # ------------------------------------------------------------------------------------------------------
                    elif decision_4_1 == "2": #Por tipo
                        contador_uso_multiple = 0
                        decision_4_1_2 = validador_numeros("Indique el tipo de producto que busca\n1-Alimentos\n2-Bebidas\n--> ", 2, "Debe indicar una de ambas opciones: 1 ó 2") # Se indica si quiere bebidas o alimentos y a partir de allí se muestran todas las opciones disponibles en un estadio en particular
                        if decision_4_1_2 == "2":
                            decision_4_1_2 = "beverages"
                        elif decision_4_1_2 == "1":
                            decision_4_1_2 = "food"
                        print(f"Se tienen a disposición para el tipo: {decision_4_1_2.capitalize()} los siguientes productos:\n")
                        for restaurantes in partidos.stadium.restaurants:
                            for productos in restaurantes.products:
                                if decision_4_1_2 == productos.type and productos.quantity != 0:
                                    contador_uso_multiple += 1
                                    productos.mostrar_caracteristicas(contador_uso_multiple, restaurantes)
                          # ------------------------------------------------------------------------------------------------------
                    elif decision_4_1 == "3": # Por rango de precio
                        contador_uso_multiple = 0
                        print("Ha decidido dentro de un rango de precios, por favor, ingrese primero el límite inferior y luego el límite superior\n")
                        decision_4_1_3_inferior, decision_4_1_3_superior = input("Límite inferior: "), input("Límite superior: ") # Debe indicar el límite inferior y luego el superior
                        while not decision_4_1_3_inferior.isnumeric() or not decision_4_1_3_superior.isnumeric() or decision_4_1_3_superior < decision_4_1_3_inferior:
                            print("\nOPCIÓN INVÁLIDA\nTal vez no ingresó un número o el límite inferior que ingresó es mayor al límite mayor\nIntente nuevamente:\n")
                            decision_4_1_3_inferior, decision_4_1_3_superior = input("Límite inferior: "), input("Límite superior: ") # De no ser ingresados números o de ser ingresado un límite inferior mayor al límite mayor entonces se le pedirá nuevamente ambos al usuario por consola
                        print(f"Los productos dentro del rango de precios: {decision_4_1_3_inferior}-{decision_4_1_3_superior} son los siguientes:\n") # Se muestran los productos dentro de ese rango de precios en los restaurantes del estadio
                        for restaurantes in partidos.stadium.restaurants:
                            for productos in restaurantes.products:
                                if int(decision_4_1_3_inferior) < productos.price < int(decision_4_1_3_superior) and productos.quantity != 0:
                                    contador_uso_multiple += 1
                                    productos.mostrar_caracteristicas(contador_uso_multiple, restaurantes)
              # ------------------------------------------------------------------------------------------------------
        elif decision_init == "5": # Compra de productos
            contador_uso_multiple = 0
            entradas_compra = [] #Se guardarán todas las entradas VIP ya usadas para luego validar que el cliente no pueda utilizar alguna otra de las que pueda poseer
            codigos_productos = [] #Se le asigna a cada producto un código único para entonces poder facturar unicamente aquellos productos comprados en la vuelta en desarrollo
            restaurantes_posibles = [] #Se valida que el cliente deba comprar en uno de los restaurante en la inmediaciones del estadio. No podrá elegir algún otro
            partido_compra, evaluacion_vip = validador_numeros("Indique en qué partido se encuentra comprando:\n--> ", 48, "ERROR: DEBE INDICAR UN ID DE PARTIDO ENTRE EL 1 Y EL 48"), validador_numeros("Ingrese la cédula del cliente para evaluar si es VIP:\n--> ", 1000000000,  "ERROR. DEBE INGRESAR  UN NÚMERO")
            for cliente in clientes:
                if cliente.id == evaluacion_vip: #Se le muestran al cliente los boletos VIP ya usados
                    print(f"Usted dispone de las siguientes entradas VIP para el partido {partido_compra}:")
                    for tickets in cliente.ticket_type:
                        if tickets.match == partido_compra and tickets.usage == True and tickets.sit.type == "vip":
                            contador_uso_multiple += 1
                            entradas_compra.append(str(tickets.code))
                            print(f"Boleto {contador_uso_multiple}")
                            print(f"    Codigo Boleto: {tickets.code}        Asiento: {tickets.sit.code}")
            if entradas_compra != []: #Si no hay boletos con las características antes precisadas, entonces el resto del código correspondiente a este módulo no hallará igualdades en el resto del código al asignar al boleto_elegio un valor de cero
                contador_uso_multiple = 0
                boleto_elegido = textos_validador(entradas_compra, "Ingrese el código del boleto con el que desea comprar:\n--> ", "INTRODUZCA UNO DE LOS NÚMEROS CORRESPONDIENTES A SUS BOLETOS DEL PARTIDO")
            else:
                boleto_elegido = "0"
            if boleto_elegido != "0": #Si efectivamente se escogió un boleto, entonces se prosigue
                for partidos in partidos_por_jugar:
                    if partidos.id == partido_compra:
                        print("Se disponen de los siguientes restaurantes en el estadio:\n")
                        for restaurantes in partidos.stadium.restaurants:
                            contador_uso_multiple += 1
                            restaurantes_posibles.append(restaurantes.name.lower())
                            print(f"Restaurante {contador_uso_multiple}:")
                            print("     ", restaurantes.name)
                restaurante_elegido = textos_validador(restaurantes_posibles, "Elija el restaurante en el que desea comprar:\n--> ", f"Debe ingresar el nombre de uno de los restaurantes emplazados en el {partidos.stadium.name}") # El usuario debe definir en qué restaurante desea comprar a partir de los mostrados por consola
            else:
                restaurante_elegido = "0"
                print(f"Usted no tiene boletos VIP para el partido {partido_compra}")
            contador_uso_multiple = 0
            monto_inicial = 0 # Contadores realtivos a las cuentas que se harán posteriormente
            descuento_final = 0
            iva_final = 0
            total_final = 0
            for cliente in clientes:
                if cliente.id == evaluacion_vip:
                    productos_posibles = [] # Se valida que el cliente elija únicamente los productos ofertados por el restaurante elegido
                    for partidos in partidos_por_jugar:
                        for restaurantes in partidos.stadium.restaurants:
                            for tickets in cliente.ticket_type:
                                if restaurantes.name.lower() == restaurante_elegido and partidos.id == partido_compra and tickets.code == int(boleto_elegido) and tickets.sit.type == "vip":
                                    print(f"Se disponen de los siguientes productos en el restaurante {restaurante_elegido.capitalize()}")
                                    for productos in restaurantes.products:
                                        productos_posibles.append(productos.name.lower())
                                        contador_uso_multiple += 1
                                        productos.mostrar_caracteristicas(contador_uso_multiple, restaurantes)
                                    while True: # Mientras el cliente desee comprar productos, bien puede proseguir. La compra de productos se hace de un producto a un producto. No es posible comprar dos o diez productos, por ejemplo, en una sola vuelta del "While True"
                                        producto_elegido = producto_validador(productos_posibles, "Elija el producto que desea comprar:\n--> ", cliente.age)
                                        for productos in restaurantes.products:
                                            contador_uso_multiple = 0
                                            if productos.name.lower() == producto_elegido:
                                                contador_uso_multiple += 1
                                                tickets.bought_products.append(ProductoComprado(productos.name, productos.price, productos.type, productos.adicional, restaurantes.name, None))
                                        if not romper_true("¿Desea comprar otro producto en el mismo restaurante? (S/N)\n--> "): #Si no desea comprar más, pues se romperá el "While True"
                                            break
                                else:
                                    break
                    for ticke in cliente.ticket_type: # A cada producto, como ya se dijo, se le asigna un código único que lo identificará a lo largo del programa
                        if ticke.sit.type == "vip":               
                            for producto in ticke.bought_products:
                                if producto.codigo == None:
                                    code = random.randint(100000,1000000)
                                    codigos_productos.append(code)
                                    producto.codigo = code
                    contador_uso_multiple = 0
                    if codigos_productos != []: #Si no hay productos comprados, entonces el código que sigue no se ejecutará
                        print("Está comprando:\n")
                        for productos in cliente.ticket_type:
                            for producto in productos.bought_products:
                                if producto.codigo in codigos_productos:
                                    monto_inicial += producto.price
                                    if numero_perfecto(int(cliente.id)): # Se valida que la cédula del cliente sea número perfecto. Además, a partir de allí se sacan las cuentas. al atributo precio del producto, se le cambiará el valor para tomar en consideración un eventual descuento y el IVA
                                        descuento_final += round((producto.price * 0.15), 2)
                                        producto.price = round((producto.price * 0.85), 2)
                                        iva_final += round((producto.price * 0.16), 2)
                                        producto.price = round((producto.price * 1.16), 2)
                                    else: # De no ser número perfecto, pues se ejecutará lo siguiente
                                        iva_final += round((producto.price * 0.16), 2)
                                        producto.price = round((producto.price * 1.16), 2)
                                    contador_uso_multiple += 1 #Se muestran por consola, uno a uno, los productos a comprar por el cliente
                                    print(f"Producto {contador_uso_multiple}:")
                                    print("     ", producto.name)
                                    total_final += round(producto.price, 2) #se define el total final de la cuenta, considerando IVA y descuentos
                        compra_productos = textos_validador(["s", "n"], f"La compra total es de {round(total_final, 2)} (descuentos e IVA incluidos)). ¿Desea continuar con la compra? (S/N)\n--> ")
                        contador_uso_multiple = 0
                        if compra_productos == "s": # Si se decide a comprar, pues se le imprimirá por consola una factura y además se le restará al inventario del restaurante en el que compró la cantidad de productos que haya comprado
                            print("Compra exitosa!!\n******************** FACTURA ********************\nNombre:", cliente.name, "\nCédula:", cliente.id, "\nHa comprado:")
                            for productos in cliente.ticket_type:
                                for producto in productos.bought_products:
                                    if producto.codigo in codigos_productos:
                                        contador_uso_multiple += 1
                                        producto.mostrar_al_vender(contador_uso_multiple)
                                        for partidos in partidos_por_jugar:
                                            for restaurantes in partidos.stadium.restaurants:
                                                if restaurantes.name.lower() == producto.quantity.lower() and partido_compra == partidos.id:
                                                    for prod in restaurantes.products:
                                                        if producto.name.lower() == prod.name.lower():
                                                            prod.quantity -= 1
                                                            
                            print("Subtotal:", round(monto_inicial, 2), "\nIVA (16%):", round(iva_final, 2), "\nDescuento:", round(descuento_final, 2), "\nTotal:", round(total_final, 2))
                        else: # Se removerán de la lista de productos de la entrada VIP elegida los productos que pretendían ser comprados por el cliente en cuestión
                            print("Será en una siguiente oportunidad.")
                            contador_uso_multiple += 1
                            for productos in cliente.ticket_type:
                                for codigos in codigos_productos:
                                    for producto in productos.bought_products:
                                        if producto.codigo == codigos:
                                            productos.bought_products.remove(producto)
                  # ------------------------------------------------------------------------------------------------------
        elif decision_init == "6": #Módulo correspondiente a las estadísticas del sistema
            decision_6_1 = validador_numeros("¿Qué estadística desea observar?\n1-Promedio de gasto de un cliente VIP en un partido \n2-Tabla con la asistencia a los partidos (de mejor a peor)\n3-Partido con mayor asistencia\n4-Partido con mayor boletos vendidos\n5-Top 3 productos más vendidos en el restaurante\n6-Top 3 de clientes (más boletos)\n7-Visualizar gráficos de dichas estadísticas\n -->", 7, "ERROR. DEBE INGRESAR UN NÚMERO ENTRE EL 1 Y EL 7\n")
            if decision_6_1 == "1": #Promedio de gastos de clientes VIP, únicamente con los boletos VIP que pudieran poseer, en el total de partidos
                for partido in partidos_por_jugar: #En estas líneas se le suma al atributo de los partidos gasto_total_de_los_clientes_vip únicamente los gastos que los clientes con entradas VIP para un partido en específico haya hecho.
                    for cliente in clientes:
                        for tickets in cliente.ticket_type:
                            if tickets.match == partido.id and tickets.sit.type == "vip":
                                if tickets.code not in entradas_que_intervienen_vip:
                                    entradas_que_intervienen_vip.append(tickets.code)
                                    partido.spends_total_vip += tickets.price
                                for productos in tickets.bought_products:
                                    if productos.codigo not in codigos_que_intervienen_vip:
                                        codigos_que_intervienen_vip.append(productos.codigo)
                                        partido.spends_total_vip += productos.price
                promedio_gasto_clientes_vip = 0
                partido_gasto_clientes_vip = 0
                for partido in partidos_por_jugar: 
                    clientes_cantidad = 0
                    for client in clientes:
                        for ticke in client.ticket_type: #Se evaluán la cantidad de clientes VIP que hay en un partido
                            if partido.id == ticke.match and ticke.sit.type == "vip":
                                clientes_cantidad += 1
                                break
                    if partido.spends_total_vip != 0:
                        promedio_gasto_clientes_vip += partido.spends_total_vip/clientes_cantidad #Si el gasto de los clientes VIP es diferente a cero, entonces se divide el total gastado por los VIP en ese partido entre la cantidad de clientes VIP en el mismo
                        partido_gasto_clientes_vip += 1
                try: #Se muestra por consola el promedio. En caso de no haber datos para tal promedio, se precisa la excepción de ser el promedio igual a cero
                    print(f"El promedio de gasto de los clientes VIP en un partido es de {round((promedio_gasto_clientes_vip/partido_gasto_clientes_vip), 2)}.")
                except:
                    print(f"El promedio de gasto de los clientes VIP en un partido es de 0.")
                # --------------------------------------------------------------------------------
            elif decision_6_1 == "2": #Tabla asistencia de mejor a peor
                contador_uso_multiple = 0
                cont = 0
                partidos_por_jugar_ordenar = partidos_por_jugar.copy() #Se copia la edd principial para no alterarla posteriormente
                for i in range(len(partidos_por_jugar_ordenar)): #Se utiliza un algoritmo de ordenamiento con el propósito de ordenar de menor a mayor los partidos de acuerdo al número de asistentes que tengan
                    temp = i
                    valor = partidos_por_jugar_ordenar[i].asistance
                    valor_2 = partidos_por_jugar_ordenar[i]
                    j = i-1
                    while j >= 0 and valor < partidos_por_jugar_ordenar[j].asistance:
                        partidos_por_jugar_ordenar[temp] = partidos_por_jugar_ordenar[j]
                        partidos_por_jugar_ordenar[j] =  valor_2
                        temp -= 1
                        j -= 1
                partidos_por_jugar_ordenar = partidos_por_jugar_ordenar[::-1] #Ahora se lleva ese orden de mayor a menor, tal y como es pedido
                for partidos_ordenar in partidos_por_jugar_ordenar: #A partir de los objetos se sustituye en la edd copiada de la original de los partidos los objetos partidos por una lista que contenga los datos que interese colocar en la tabla requerida
                    try:
                        partidos_por_jugar_ordenar[contador_uso_multiple] = [partidos_ordenar.id, partidos_ordenar.home_team.name, partidos_ordenar.away_team.name, partidos_ordenar.stadium.name, partidos_ordenar.sell, partidos_ordenar.asistance, round((partidos_ordenar.asistance/partidos_ordenar.sell), 2)]
                        contador_uso_multiple += 1
                    except: #La excepción se aplica en caso de tener una divisón entre cero en el caso anterior para la relación asistencia/venta
                        partidos_por_jugar_ordenar[contador_uso_multiple] = [partidos_ordenar.id, partidos_ordenar.home_team.name, partidos_ordenar.away_team.name, partidos_ordenar.stadium.name, partidos_ordenar.sell, partidos_ordenar.asistance, round((partidos_ordenar.asistance/1), 2)]
                        contador_uso_multiple += 1
                datos = ["Partido", "Local", "Visitante", "Estadio", "Ventas", "Asistencias", "Relación asistencia/venta"] #Se definen los headers que irán en la tabla
                print(tabulate(partidos_por_jugar_ordenar, headers = datos, tablefmt="grid")) #Usando la librería tabulate se crea la tabla, se define qué datos contendrá ella, cuales serán los headers, y además el tipo de tabla que querremos

            # --------------------------------------------------------------------------------
            elif decision_6_1 == "3": #Partido con mayor asistencia
                contador_uso_multiple = 0
                contador_uso_multiple_2 = 0
                for partido in partidos_por_jugar:
                    if partido.asistance > contador_uso_multiple:
                        contador_uso_multiple = partido.asistance #Se utiliza un contador que evaluará cuál es la mayor asistencia de los partidos
                print("**************** PARTIDO(S) CON MÁS ASISTENCIA ******************")
                for partidos in partidos_por_jugar:
                    if contador_uso_multiple == partidos.asistance and partidos.asistance != 0: #Si uno o más partidos igualan a la mayor asistencia, entonces serán impresos por consola. Estos valores no pueden ser ceros
                        contador_uso_multiple_2 += 1
                        print("     Equipo local:", partidos.home_team.name)
                        print("     Equipo visitante:", partidos.away_team.name)
                        print("     N° partido:", partidos.id)
                        print("     Estadio:", partidos.stadium.name)
                        print("     Asistencia:", partidos.asistance)
                        print("     Fecha:", partidos.date, "\n")
                if contador_uso_multiple_2 == 0: #De no haber asistencias y haber puros ceros, entonces se imprimirá en consola que no hay asistentes
                    print("Al parecer aún no ha habido asistentes a ningún partido.")
            # --------------------------------------------------------------------------------
            elif decision_6_1 == "4":
                contador_uso_multiple = 0
                contador_uso_multiple_2 = 0
                for partido in partidos_por_jugar:
                    if partido.sell > contador_uso_multiple:
                        contador_uso_multiple = partido.sell #Se utiliza un contador que evaluará cuál es la mayor venta de los partidos
                print("**************** PARTIDO(S) CON MÁS VENTAS ******************")
                for partidos in partidos_por_jugar:
                    if contador_uso_multiple == partidos.sell and partido.sell != 0: #Si uno o más partidos igualan a la mayor venta, entonces serán impresos por consola. Estos valores no pueden ser ceros
                        contador_uso_multiple_2 += 1 
                        print("     Equipo local:", partidos.home_team.name)
                        print("     Equipo visitante:", partidos.away_team.name)
                        print("     N° partido:", partidos.id)
                        print("     Estadio:", partidos.stadium.name)
                        print("     N° de ventas:", partidos.sell)
                        print("     Fecha:", partidos.date, "\n")
                if contador_uso_multiple_2 == 0: #De no haber ventas y haber puros ceros, entonces se imprimirá en consola que no hay ventas
                    print("Al parecer aún no se han vendido boletos.")
            # --------------------------------------------------------------------------------
            elif decision_6_1 == "5": #Productos más comprados
                productos_total_comprado = productos_dict.copy() #Se copia el diccionario con todos los productos existentes en los restaurantes y se igualan a cero
                for cliente in clientes: #Se evaluan qué productos han comprado los clientes y luego se le suman uno a uno al diccionario que fui copiado anteriormente
                    for entradas in cliente.ticket_type:
                        if entradas.sit.type == "vip":
                            for products in entradas.bought_products:
                                for valores in productos_total_comprado.keys():
                                    if products.name.lower() == valores:
                                        productos_total_comprado[valores] += 1
                mayor_n = [] #En una lista se ingresan todos los valores de los productos
                for mayores in productos_total_comprado.values():
                    mayor_n.append(mayores)
                mayor_n = sorted(mayor_n) #Se ordenan de menor a mayor
                mayor_n = mayor_n[::-1] #Ahora de llevan de mayor a menor
                comparador = len(mayor_n)
                for mayores in mayor_n[:3]: #se toman únicamente aquellos tres valores mayores, y luego se igualan con el total existente en el diccionario de antes para así poder
                    for producto, valores in productos_total_comprado.items():
                        if contador_uso_multiple == 3:
                            break
                        if mayores == valores and mayores != 0:
                            contador_uso_multiple += 1 #Se imprimen por consola, el nombre de los productos, indicando su posición en el top 3, y además se precisa cuánto se ha vendido. Este valor no puede ser igual a cero
                            print(f"Producto N°{contador_uso_multiple}:")
                            print("     ", producto.capitalize(), "\n     Cantidad:",valores)
            # --------------------------------------------------------------------------------
            elif decision_6_1 == "6": #Mejores clientes
                contador_uso_multiple = 0
                cantidad_boletos = [] #Se ingresa en una lista la cantidad de boletos que cada cliente ha comprado
                clientes_evaluados = []
                for cliente in clientes:
                    cantidad_boletos.append(len(cliente.ticket_type))
                cantidad_boletos = sorted(cantidad_boletos) 
                cantidad_boletos = cantidad_boletos[::-1] #Luego de haberla ordenado de menor a mayor, ahora se ordena mayor a menor
                comparador = len(cantidad_boletos) #se toma en cuenta la cantidad de clientes que exista
                if comparador >= 3:#Se evalúan tres situaciones: si hay tres o más clientes, si hay dos clientes, si hay uno solo
                    for mayores in cantidad_boletos[:3]: #se toman únicamente aquellos tres valores mayores, y luego se igualan con el len() de la cantidad de boletos comprados por cada cliente, al llegar el contador a tres, se detiene todo
                        for cliente in clientes:
                            if contador_uso_multiple == 3:
                                break
                            if len(cliente.ticket_type) == mayores and cliente.id not in clientes_evaluados:
                                clientes_evaluados.append(cliente.id)
                                contador_uso_multiple += 1
                                mostrar_cliente(cliente, contador_uso_multiple)
                                break
                elif comparador == 2: #se toman únicamente aquellos dos valores existentes
                    for mayores in cantidad_boletos[:2]:
                        for cliente in clientes:
                            if len(cliente.ticket_type) == mayores:
                                contador_uso_multiple += 1
                                mostrar_cliente(cliente, contador_uso_multiple)
                                break
                else: #se toman el único valor que exista
                    for cliente in clientes:
                        contador_uso_multiple += 1
                        mostrar_cliente(cliente, contador_uso_multiple)
            # --------------------------------------------------------------------------------
            elif decision_6_1 == "7": # Gráficas correspondientes a los datos antes tratados
                decision_6_1_1 = validador_numeros("¿Qué gráfica desea observar?\n1-Gastos clientes VIP \n2-Asistencia de cada partido\n3-Productos vendidos\n4-Número de boletos por cliente\n5-Ventas de boletos de cada partido\n -->", 5, "ERROR. DEBE INGRESAR UN NÚMERO ENTRE EL 1 Y EL 5\n")
                if decision_6_1_1 == "1": # Gráficas correspondientes al número de gastos por cliente
                    listica_clientes = []
                    gastos_clientes = []
                    for cliente in clientes:
                        gastos = 0
                        listica_clientes.append(cliente.name.capitalize())
                        for gasto in cliente.ticket_type:
                            gastos += gasto.price
                            if gasto.sit.type == "vip":
                                for product in gasto.bought_products:
                                    gastos += product.price
                        gastos_clientes.append(gastos)
                    grafica_gastos = figure(x_range=listica_clientes, width = 1500, height = 250, title = "Gastos de cada cliente", toolbar_location = None, tools = "")
                    grafica_gastos.vbar(x=listica_clientes, top = gastos_clientes, width = 0.5)
                    show(grafica_gastos)
                elif decision_6_1_1 == "2": # Gráficas correspondientes al número de asistencias por partido
                    partidillos = []
                    asistencia = []
                    for partido in partidos_por_jugar:
                        partidillos.append(partido.id), asistencia.append(partido.asistance)
                    grafica_asistencia = figure(x_range=partidillos, width = 1500, height = 250, title = "Asistencia por partido", toolbar_location = None, tools = "")
                    grafica_asistencia.vbar(x=partidillos, top = asistencia, width = 0.5)
                    show(grafica_asistencia)
                elif decision_6_1_1 == "3": # Gráficas correspondientes al número de productos comprados en total
                    productos_total_comprado = productos_dict.copy()
                    for cliente in clientes:
                        for entradas in cliente.ticket_type:
                            if entradas.sit.type == "vip":
                                for products in entradas.bought_products:
                                    for valores in productos_total_comprado.keys():
                                        if products.name.lower() == valores:
                                            productos_total_comprado[valores] += 1
                    productos_grafica = []
                    cantidades = []
                    for nombre, valores in productos_total_comprado.items():
                        productos_grafica.append(nombre.capitalize()), cantidades.append(valores)
                    grafica_productos = figure(x_range=productos_grafica, height = 250, title = "Cantidad de productos comprados en los restaurantes", toolbar_location = None, tools = "")
                    grafica_productos.vbar(x=productos_grafica, top=cantidades, width = 0.5)
                    show(grafica_productos)
                elif decision_6_1_1 == "4": # Gráficas correspondientes al número de boletos comprados por los distintos clientes que existan
                    clientes_grafica = []
                    boletos_cliente = []
                    for client in clientes:
                        clientes_grafica.append(client.name), boletos_cliente.append(len(client.ticket_type))
                    grafica_clientes = figure(x_range=clientes_grafica, height = 250, title = "Boletos comprado por cliente", toolbar_location = None, tools = "")
                    grafica_clientes.vbar(x=clientes_grafica, top=boletos_cliente, width = 0.5)
                    show(grafica_clientes)
                elif decision_6_1_1 == "5": # Gráficas correspondientes al número de boletos vendidos por partido
                    partidillos = []
                    vendidas = []
                    for partido in partidos_por_jugar:
                        partidillos.append(partido.id), vendidas.append(partido.sell)
                    grafica_ventas = figure(x_range=partidillos, width = 1500, height = 250, title = "Venta de boletos por partido", toolbar_location = None, tools = "")
                    grafica_ventas.vbar(x=partidillos, top = vendidas, width = 0.5)
                    show(grafica_ventas)

            # --------------------------------------------------------------------------------
        elif decision_init == "7": #Cierre del programa
            print("Hasta luego! Disfruta enormemente de Qatar 2022!")
            break
        elif decision_init == "8": #Reinicio del sistema y salida
            condicion_salida = "s" #La condición:salida para guardar los datos cambia, y ya no se ejecutará
            links = ["Proyecto_Qatar2022/datos_clientes.json", "Proyecto_Qatar2022/datos_base.json", "Proyecto_Qatar2022/datos_extra.json"]
            for link in links:
                with open(link, "w") as f: #En estas líneas, se sustituye lo que sea que haya dentro de los archivos JSON por una lista vacía que permitirá cargar los dato nuevamente desde la API
                    f.write(json.dumps([]))
                    f.close()
            break
    if condicion_salida == "n": #Condición salida que, de no ejecutarse el módulo 8, entonces podrá guardar todos los datos tratados durante el desarrollo del programa en los distintos archivos JSON encargados de guardar tales datos
        contador_uso_multiple = 0
        for client in clientes:
            contador_uso_multiple_2 = 0
            clientes[contador_uso_multiple] = client.__dict__
            for tickets in client.__dict__["ticket_type"]:
                contador_uso_multiple_3 = 0
                asiento = tickets.__dict__["sit"]
                clientes[contador_uso_multiple]["ticket_type"][contador_uso_multiple_2] = tickets.__dict__
                clientes[contador_uso_multiple]["ticket_type"][contador_uso_multiple_2]["sit"] = asiento.__dict__
                if asiento.__dict__["type"] == "vip":
                    for products in tickets.__dict__["bought_products"]:
                        clientes[contador_uso_multiple]["ticket_type"][contador_uso_multiple_2]["bought_products"][contador_uso_multiple_3] = products.__dict__
                        contador_uso_multiple_3 += 1
                contador_uso_multiple_2 += 1
            contador_uso_multiple += 1
        contador_uso_multiple = 0
        for estadio in estadios_lista:
            contador_uso_multiple_2 = 0
            estadios_lista[contador_uso_multiple] = estadio.__dict__
            for restaurantes in estadio.__dict__["restaurants"]:
                contador_uso_multiple_3 = 0
                estadios_lista[contador_uso_multiple]["restaurants"][contador_uso_multiple_2] = restaurantes.__dict__
                for productos in restaurantes.__dict__["products"]:
                    estadios_lista[contador_uso_multiple]["restaurants"][contador_uso_multiple_2]["products"][contador_uso_multiple_3] = productos.__dict__
                    contador_uso_multiple_3 += 1
                contador_uso_multiple_2 += 1
            contador_uso_multiple += 1
        contador_uso_multiple = 0
        for equipos in equipos_lista:
            equipos_lista[contador_uso_multiple] = equipos.__dict__
            contador_uso_multiple += 1
        contador_uso_multiple = 0
        for partidos in partidos_por_jugar:
            contador_uso_multiple_2 = 0
            partidos_por_jugar[contador_uso_multiple] = partidos.__dict__
            for estadios in estadios_lista:
                if partidos.__dict__["stadium_id"] == estadios["id"]:
                    partidos_por_jugar[contador_uso_multiple]["stadium"] = estadios
            for equipos in equipos_lista:
                try:
                    if partidos_por_jugar[contador_uso_multiple]["home_team"].name == equipos["name"]:
                        partidos_por_jugar[contador_uso_multiple]["home_team"] = equipos
                except AttributeError:
                    if partidos_por_jugar[contador_uso_multiple]["home_team"] == equipos["name"]:
                        partidos_por_jugar[contador_uso_multiple]["home_team"] = equipos
                try: 
                    if partidos_por_jugar[contador_uso_multiple]["away_team"].name == equipos["name"]:
                        partidos_por_jugar[contador_uso_multiple]["away_team"] = equipos
                except AttributeError:
                    if partidos_por_jugar[contador_uso_multiple]["away_team"] == equipos["name"]:
                        partidos_por_jugar[contador_uso_multiple]["away_team"] = equipos
            for asientos in partidos.__dict__["sits"]:
                partidos_por_jugar[contador_uso_multiple]["sits"][contador_uso_multiple_2] = asientos.__dict__
                contador_uso_multiple_2 += 1
            contador_uso_multiple += 1
        with open("Proyecto_Qatar2022/datos_clientes.json", "w") as f: #Insertación de los clientes en un JSON
            f.write(json.dumps(clientes, indent=" "))
            f.close()
        with open("Proyecto_Qatar2022/datos_base.json", "w") as w: #Insertación de los datos base obtenidos desde la API en un JSON
            w.write(json.dumps([equipos_lista, partidos_por_jugar, estadios_lista], indent=" "))
            w.close()
        with open("Proyecto_Qatar2022/datos_extra.json", "w") as b:#Insertación de los datos extra que permiten validar ciertos datos a lo largo del programa en un JSON
            b.write(json.dumps([productos_dict, entradas_por_usar, codigos_que_intervienen_vip, entrada_usadas, entradas_que_intervienen_vip], indent=" "))
            b.close()

main()