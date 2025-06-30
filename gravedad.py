#   load solar_sistem.json
#   size view 100e11;100e11
#   solar_sistem asteroid_belt 250
#   solar_sistem kuiper_belt 300
#   solar_sistem asteroids 100
#   time.mode uniform 50000  Velocidad de tiempo constante más baja
#   time.mode uniform 200000   Velocidad de tiempo constante más alta
"""
Puedes simular el sistema solar, añadir el cinturón de asteroides, y ajustar la vista con los siguientes comandos:
Cargar el Sistema Solar
load solar_sistem.json#

Ajustar el Tamaño de la Vista
size view 100e11;100e11

Añadir el Cinturón de Asteroides
Puedes añadir el cinturón de asteroides con la siguiente línea:
solar_sistem asteroid_belt 250
Este comando añadirá 250 asteroides en el cinturón entre Marte y Júpiter. Si quieres más o menos asteroides, cambia el número 250 por cualquier otro valor.
Añadir el Cinturón de Kuiper

Para añadir el cinturón de Kuiper:
solar_sistem kuiper_belt 300

Añadir Asteroides Aleatorios
Si quieres generar asteroides sueltos en posiciones aleatorias:
solar_sistem asteroids 100

4. Ajustar la Velocidad del Modo de Tiempo Uniforme
Si deseas que la simulación sea más rápida o lenta, puedes modificar el valor de time.mode uniform. Un valor mayor hará que los cuerpos se muevan más rápido en cada frame:
time.mode uniform 50000  Velocidad de tiempo constante más baja
time.mode uniform 200000   Velocidad de tiempo constante más alta

5. Añadir Guardado Automático durante la Simulación
Para asegurarte de que no pierdas los datos generados, puedes activar el guardado automático usando el siguiente comando:
#active_save
Esto creará un archivo .json con los datos de la simulación mientras está en marcha, lo que te permitirá cargar esos datos más tarde si lo necesitas.
run = ejecutar la simulación
"""

# ----------------- importar librerias --------------------- 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import *
from vectores import *
from funciones_extra import *
import time
import random
import colorsys
import json
import os
import ctypes
from decimal import Decimal, getcontext

# Habilitar el soporte de colores ANSI en la consola de Windows, si aplica.
if os.name == 'nt': # 'nt' es el identificador para Windows
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except (AttributeError, OSError):
        # Si falla, no es crítico. El programa puede continuar.
        pass

# precisión de los datos
getcontext().prec = 250

import random

class Evento:
    def __init__(self, tipo, tiempo_de_aparicion, parametros):
        self.tipo = tipo
        self.tiempo_de_aparicion = tiempo_de_aparicion
        self.parametros = parametros

    def ejecutar(self, universo):
        if self.tipo == "cometa":
            self.crear_cometa(universo)
        elif self.tipo == "perturbacion_gravitacional":
            self.crear_perturbacion_gravitacional(universo)
        elif self.tipo == "objeto_aleatorio":
            self.crear_objeto_aleatorio(universo)

    def crear_cometa(self, universo):
        # Crea un cometa con una órbita aleatoria
        posicion = Vector2(random.uniform(-1000000, 1000000), random.uniform(-1000000, 1000000))
        velocidad = Vector2(random.uniform(-1000, 1000), random.uniform(-1000, 1000))
        masa = random.uniform(1000, 10000)
        diametro = random.uniform(10, 100)

        cometa = Cuerpo("Cometa", posicion, velocidad, masa, diametro)
        universo.cuerpos.append(cometa)

    def crear_perturbacion_gravitacional(self, universo):
        # Crea una perturbación gravitacional en un punto aleatorio del espacio
        posicion = Vector2(random.uniform(-1000000, 1000000), random.uniform(-1000000, 1000000))
        fuerza = Vector2(random.uniform(-1000, 1000), random.uniform(-1000, 1000))

        for cuerpo in universo.cuerpos:
            cuerpo.aplicar_fuerza(fuerza, 1)

    def crear_objeto_aleatorio(self, universo):
        # Crea un objeto aleatorio con una órbita aleatoria
        posicion = Vector2(random.uniform(-1000000, 1000000), random.uniform(-1000000, 1000000))
        velocidad = Vector2(random.uniform(-1000, 1000), random.uniform(-1000, 1000))
        masa = random.uniform(1000, 10000)
        diametro = random.uniform(10, 100)

        objeto = Cuerpo("Objeto aleatorio", posicion, velocidad, masa, diametro)
        universo.cuerpos.append(objeto)


class Universo:
    def __init__(self, fisica, grid):
        self.fisica = fisica
        self.grid = grid 

class Fisica:
    def __init__(self, g) -> None:
        self.g = g
    
    def gravedad(self, cuerpo_a, cuerpo_b):
        '''devuelve el vector de la fuerza que reciven los cuerpos'''
        # calcular la fuerza usando la formula de newton
        fuerza_total = self.g*((cuerpo_a.masa * cuerpo_b.masa) / (Decimal_distancia(cuerpo_a.posicion, cuerpo_b.posicion) ** 2))
        
        # calcular el vector de la direccion usando trigonometria
        ang = atan2(cuerpo_a.posicion.y - cuerpo_b.posicion.y, cuerpo_a.posicion.x - cuerpo_b.posicion.x)
        fuerza_x = fuerza_total * Decimal(cos(ang))
        fuerza_y = fuerza_total * Decimal(sin(ang))
        
        return Vector2(fuerza_x, fuerza_y)
    
    def calcular_velocidad_orbital(self, cuerpo_central, cuerpo_orbiando):
        v = Decimal(math.sqrt((self.g * cuerpo_central.masa)/ Decimal_distancia(cuerpo_central.posicion, cuerpo_orbiando.posicion)))
        return v
        
    def calcular_aceleracion(self, fueza_aplicada, masa, tiempo):
        '''aplicar la formula F = ma'''
        aceleracion  = fueza_aplicada / masa
        # se suma la velocidad a la velocidad previa anterior
        return aceleracion * tiempo
    

# ---------------------- Crear la clase Cuerpo ----------------------------
class Cuerpo:
    # inicializar variables
    def __init__(self, nombre, posicion, velocidad, masa, diam = None, exact = True):
        self.nombre = nombre
        self.posicion = posicion
        self.velocidad = velocidad
        self.masa = Decimal(masa)
        # establecer una tag aleatoria
        self.tag = crear_string_random(5)
        # establecer un color aleatorio
        self.color = colorsys.hsv_to_rgb(random.uniform(0,1),1,1)
        self.diametro = diam
        self.exact = exact
        self.posiciones = []

        if diam != None:
            self.diametro = diam
        else:
            self.diametro = float(masa) * dot_scale
    
    def guardar_pos(self):
        self.posiciones.append(self.posicion)
    
    # funcion para aplicar una fuerza
    def aplicar_fuerza(self, fuerza_aplicada, tiempo):
        # aplicar la formula F = ma
        velocidad_r = universo.fisica.calcular_aceleracion(fuerza_aplicada, self.masa, tiempo)
        # sumar la velocidad
        self.velocidad = self.velocidad + velocidad_r
    
    # funcion para aplicar la gravedad
    def aplicar_gravedad(self, otro, delta_time):
        # calcular la gravedad
        fuerza = universo.fisica.gravedad(self, otro)
        
        # aplicar la fuerza obtenida al otro
        otro.aplicar_fuerza(Vector2(fuerza.x, fuerza.y), delta_time)
        
        # aplicar la fuerza obtenida a el mismo
        self.aplicar_fuerza(Vector2(fuerza.x, fuerza.y) * -1, delta_time)
    
    # funcion para calcular la posición del objeto en cada momento
    def constante(self, delta_time):
        # mover lo que indica la velocidad que tiene multiplicado por el tiempo que tarda cada frame
        self.posicion += self.velocidad * delta_time

# -------------------- Clase para visualizar los puntos --------------------------------
class Puntos:
    # inicializar las variables
    def __init__(self):
        # lista con los cuerpos que tiene que visualizar
        self.cuerpos = []
        # crear las variables para la ventana y los ejes
        self.fig, self.ax = plt.subplots()

        # establecer la variable para el grafico de dispersión
        self.scatter = self.ax.scatter([], [])
        
        # establecer el tamaño que muestran los ejes
        self.ax.set_xlim(view_scale.x * -1, view_scale.x) # x
        self.ax.set_ylim(view_scale.y * -1, view_scale.y) # y
        
        # establecer el color de fondo del grafico a negro
        self.ax.set_facecolor('black')
        # establecer el color de fondo de la ventana a negro
        self.fig.patch.set_facecolor('black')
        
        # ajustar la visualizacion para que 1 unidad en X mida lo mismo en la pantalla que 1 unidad en Y
        self.ax.set_aspect('equal', adjustable='datalim')
        
        # cambiar el color de los ejes a gris
        self.ax.tick_params(axis='x', colors='gray')
        self.ax.tick_params(axis='y', colors='gray')
        
        # cambiar el color del recuadro a gris
        for spine in self.ax.spines.values():
            spine.set_color('gray')
        
        # activar el modo interactivo en el grafico
        plt.ion()
        
        # crear una animacion
        self.ani = FuncAnimation(self.fig, self.actualizar_grafico, interval=16.7 /2, frames=60)

    # agregar varios cuerpos
    def agregar_cuerpos(self, cuerpos):
        for item in cuerpos:
            self.cuerpos.append(item)

    # funcion para actualizar el grafico
    # Código corregido
    def actualizar_grafico(self, frame):
    # ...
        # establecer las variables que se van a usar en el grafico
        xs, ys, nombres, pres = zip(*[(i.posicion.x, i.posicion.y, i.nombre, i.exact) for i in self.cuerpos])
        # actualizar las posiciones
        self.scatter.set_offsets(list(zip(xs, ys)))
        
        # Eliminar etiquetas anteriores
        for annotation in self.ax.texts:
            annotation.remove()
        
        # Mostrar etiquetas en blanco en cada punto
        for x, y, nombre, pre in zip(xs, ys, nombres, pres):
            if pre == True:
                self.ax.annotate(nombre, (x, y), ha='center', va='top', color='white', fontsize=8, xytext=(0, -10), textcoords='offset points')
    
        # mostrar cambios
        self.fig.canvas.get_tk_widget().update()
        
    def iniciar_animacion(self):
        plt.show()
        
        diametros, colores = zip(*[(i.diametro, i.color) for i in self.cuerpos])

        # actualizar las diametros
        self.scatter.set_sizes(list(diametros))
        # actualizar el color
        self.scatter.set_color(list(colores))

# -------------------- funcion para pedir datos --------------------------
def pedir_dato(nombre_del_dato, tipo_de_dato, close = "exit", pass_command = False): # los tipos de datos van 0 = int; 1 = float; 2 = vector; 3 = string; 4 = Decimal; 5 = vector Decimal
    # pedir dato inicial
    dato = input(f'{c["verde"]} {nombre_del_dato} = {c["default"]}')
    
    # si el dato es igual a el comando de salida
    if dato == close:
        # retornar falso
        return False
    elif pass_command != False:
        if dato == pass_command:
            return None
    
    if tipo_de_dato == 3: # si el tipo de dato es una string
        # retornar el dato sin modificar
        return dato
    
    elif es_numero(dato): # si el dato otorgado por el usuario es un numero
        
        if tipo_de_dato == 0: # si el tipo de dato pedido es int
            # retornar el int del dato
            return int(dato)
        
        elif tipo_de_dato == 1: # si el tipo de dato pedido es float
            # retornar el float del dato
            return float(dato)
        
        elif tipo_de_dato == 4: # si el tipo de dato pedido es decimal
            # retornar el decimal del dato
            return Decimal(dato)
    
    elif tipo_de_dato == 2: # si el tipo de dato pedido era un vector 2 
        # separar el input por el ;
        vector = dato.split(";") 
        
        if len(vector) == 2: # si la cantidad de datos es 2
            if es_numero(vector[0]) and es_numero(vector[1]): # si ambos datos son numeros
                # retornar el vector 2
                return Vector2(float(vector[0]),float(vector[1]))
    
    elif tipo_de_dato == 5: # si el tipo de dato pedido era un vector 2 
        # separar el input por el ;
        vector = dato.split(";") 
        
        if len(vector) == 2: # si la cantidad de datos es 2
            if es_numero(vector[0]) and es_numero(vector[1]): # si ambos datos son numeros
                # retornar el vector 2
                return Vector2(Decimal(vector[0]),Decimal(vector[1]))

    
    
    # --- en caso de que nada de eso pase
    # indicar al usuario que el dato no es valido
    print_error(tipos_de_errores[0], mensaje_extra="El tipo de dato otorgado no es valido en este contexto")
    
    # volver a pedir los datos
    close_this = close
    tipo_de_dato_this = tipo_de_dato
    nombre_del_dato_this = nombre_del_dato
    return pedir_dato(nombre_del_dato_this, close=close_this, tipo_de_dato=tipo_de_dato_this)

# ------------ funcion para crear un cuerpo ----------------------------------------
import random

def crear_cinturon_asteroides(cantidad, distancia_min, distancia_max):
    asteroides = []
    for i in range(cantidad):
        distancia = random.uniform(distancia_min, distancia_max)
        angulo = random.uniform(0, 2 * 3.14159265359)  # Ángulo aleatorio en radianes
        x = distancia * np.cos(angulo)
        y = distancia * np.sin(angulo)
        velocidad = random.uniform(10000, 30000)  # Velocidad aleatoria en un rango razonable

        asteroide = {
            "nombre": f"Asteroide_{i+1}",
            "posicion": {"x": x, "y": y},
            "velocidad": {"x": -velocidad * np.sin(angulo), "y": velocidad * np.cos(angulo)},
            "masa": "1e+15",  # Masa típica de un asteroide
            "diametro": "5"
        }
        asteroides.append(asteroide)
    return asteroides

# Constante de gravitacion universal
g = Decimal('0.01')

# Modo de tiempo
time_mode = True # si es True se usa delta_time si es False es constante 
# valor de delta_time si el time_mode es false
uniform_time = 0.1

# escala de los puntos
dot_scale = 1

# escala del campo de vision
view_scale = Vector2(150,150)

# guardado de la simulacion
active_save = False
save_in = ""
ciclos = 1

# ------------ crear cuerpos -------------------------
todos_los_cuerpos = list()
todos_los_aproximados = list()

cantidad_de_asteroides_0 = 0
cantidad_de_asteroides_1 = 0
cantidad_de_asteroides_2 = 0

sigue = True
# ----------- bucle de personalizacion del usuario -----------------------
while sigue:
    # pedir input al usuario
    input_del_usuario = input('>>> ')
    # separar el input por palabras
    input_separado = input_del_usuario.split(" ")
    
    # ~~~~~~~~~~~~~~~~~~~~ si dice "run" ~~~~~~~~~~~~~~~~~~~~
    if input_del_usuario == "run":
        # se finaliza el bucle
        sigue = False
        break
    
    # ~~~~~~~~~~~~~~~~~~~~ si dice "help" ~~~~~~~~~~~~~~~~~~~~
    elif input_del_usuario == "help":
        # dar la informacion
        print(f"""{c["amarillo"]}add:{c["default"]} añadir un cuerpo
{c["amarillo"]}G:{c["default"]} constante de gravitacion universal
    ? muestra su valor actual
    = igualar a (valor siguiente a \"=\")
{c["amarillo"]}run:{c["default"]} empezar simulacion
{c["amarillo"]}cuerpos:{c["default"]} datos de los cuerpos
{c["amarillo"]}load:{c["default"]} cargar un archivo: load [nombre_del_archivo.json]
{c["amarillo"]}save:{c["default"]} guardar datos de los cuerpos: save [nombre_del_archivo.json]
{c["amarillo"]}time.mode:{c["default"]} asignar el tipo de tiempo que se va a usar
  - delta_time varia dependiendo de cuanto tarda entre frame y frame (automático)
  - uniform un valor constante cada frame
{c["amarillo"]}size:{c["default"]} valores de tamaños
  - dots tamaño automático de los cuerpos
  - view tamaño de visión
{c["amarillo"]}active_save:{c["default"]} Guarda los datos generados durante la simulación en un archivo .json
""")
        
    # ~~~~~~~~~~~~~~~~~~~~ si dice "add" ~~~~~~~~~~~~~~~~~~~~
    elif input_separado[0] == "add":
        # crear un cuerpo
        def crear_cuerpo():
            nombre = pedir_dato("Nombre del cuerpo", 3)
            posicion = pedir_dato("Posición (x;y)", 2)
            velocidad = pedir_dato("Velocidad (x;y)", 2)
            masa = pedir_dato("Masa", 4)
            diametro = pedir_dato("Diámetro", 1, pass_command="None")
            exact = pedir_dato("¿Mostrar nombre en la visualización? (True/False)", 3)
            
            if diametro is None:
                diametro = None
            else:
                diametro = float(diametro)
            
            if exact.lower() == "true":
                exact = True
            else:
                exact = False
            
            nuevo_cuerpo = Cuerpo(nombre, posicion, velocidad, masa, diametro, exact)
            todos_los_cuerpos.append(nuevo_cuerpo)
            print(f"{c['amarillo']}Se añadió {nuevo_cuerpo.nombre} (tag: {nuevo_cuerpo.tag}){c['default']}")

        crear_cuerpo()
        # dejar un espacio
        print("\n")
    
    # ~~~~~~~~~~~~~~~~~~~~ si dice "G" ~~~~~~~~~~~~~~~~~~~~
    elif input_separado[0] == "G":
        # -- si tiene 1 palabra --
        if len(input_separado) == 1:
            
            # dar instrucciones de uso
            print("""Seleccione que quiere hacer con la variable G
    \"=\" para asignar un valor
    \"?\" para ver el valor actual""")
            
            # dejar un espacio
            print("\n")
        
        # -- si la segunda palabra es "?" --
        elif input_separado[1] == "?":
            # Dar el valor de g
            print(g)
        
        # -- si la segunda palabra es "=" y tiene 3 palabras
        elif input_separado[1] == "=" and len(input_separado) == 3:
            
            # si la tercera palabra es un numero
            if es_numero(input_separado[2]):
                # cambiar el valor de g
                g = Decimal(input_separado[2])
                print(f"{c["amarillo"]}Nuevo valor de G. Ahora es: {g}{c["default"]}")
            else:
                # dar un error de tipo de dato
                print_error(tipos_de_errores[0])
        else:
            # dar un error de sintaxis
            print_error(tipos_de_errores[1])
    
    # ~~~~~~~~~~~~~~~~~~~~ si dice "cuerpos" ~~~~~~~~~~~~~~~~~~~~ 
    elif input_separado[0] == "cuerpos":
        # -- si solo tiene una palabra -- 
        if len(input_separado) == 1:
            # dar instrucciones de uso
            print("""Seleccione que quiere hacer con "cuerpos"
    \"see\" para ver todos los cuerpos actuales
    \"delete\" para ver el valor actual \"cuerpos delete [tag]\"""")
        
        # -- la segunda palabra es "see" --
        elif input_separado[1] == "see":
            
            # si tiene cuerpos
            if (len(todos_los_cuerpos) > 0):
                # iterar los cuerpos
                for i in todos_los_cuerpos:
                    # mostrar datos
                    print(f"{c["amarillo"]}{i.tag}:{c["default"]} nombre: {i.nombre}, masa = {i.masa}, posicion = {i.posicion}, velocidad = {i.velocidad}")
            
            else:
                
                # indicar que no hay datos
                print("todavía no hay ningun cuerpo")
        
        # -- si la segunda palabra es "delete" --
        elif input_separado[1] == "delete":
            # si tiene tres palabras
            if len(input_separado) == 3:
                # recorre todos los cuerpos
                for i in todos_los_cuerpos:
                    # si la tag es igual a la dada por el usuario
                    if i.tag == input_separado[2]:
                        # indicar que se elimino el cuerpo
                        print(f"{c["amarillo"]}Se elimino {i.nombre} (tag: {i.tag}){c["default"]}")
                        # quitar el cuerpo de la lista
                        todos_los_cuerpos.remove(i)
                        # terminar bucle for
                        break
                
                # si no se encuentra
                else:
                    # indicar un error de input al no existir el cuerpo indicado
                    print_error(tipos_de_errores[3], f"no existe ningun cuerpo con la tag \"{input_separado[2]}\"")
            else:
                # indicar un error de sintaxis
                print_error(tipos_de_errores[1])
        else:
            # indicar un error de sintaxis
            print_error(tipos_de_errores[1])
    
    # ~~~~~~~~~~~~~~~~~~~~ si dice "load" ~~~~~~~~~~~~~~~~~~~~ 
    elif input_separado[0] == "load":
        # -- comprobar que sean 2 palabras --
        if len(input_separado) == 2:
            # comprobar que el archivo exista
            if os.path.exists(input_separado[1]):
                # crear una lista para ir agregando los cuerpos del archivo 
                objetos_agregados = []
                # cargar el archivo
                with open(input_separado[1], 'r') as archivo:
                    # guardar los datos en un diccionario
                    DCLD = json.load(archivo)
                
                # iterar los cuerpos
                for dato in DCLD["cuerpos"]:
                    # guardar los datos de la posicion 
                    n_posicion = Vector2(Decimal(dato["posicion"]["x"]), Decimal(dato["posicion"]["y"]))
                    # guardar los datos de la velocidad
                    n_velocidad = Vector2(Decimal(dato["velocidad"]["x"]), Decimal(dato["velocidad"]["y"]))
                    # crear el cuerpo usando el nombre, la posicon, la velocidad y la masa que indica el archivo
                    cuerpo_cargado = Cuerpo(dato["nombre"],n_posicion,n_velocidad,Decimal(dato["masa"]), float(dato["diametro"]))
                    
                    # se agrega el cuerpo a las listas que contienen los cuerpos
                    todos_los_cuerpos.append(cuerpo_cargado)
                    objetos_agregados.append(cuerpo_cargado)
                    
                    # mostrar el cuerpo que se añadio
                    print(f"{c["amarillo"]}Se añadio {cuerpo_cargado.nombre} (tag: {cuerpo_cargado.tag}){c["default"]}")
                
                # mostrar el numero de cuerpos que se añadieron
                print(f"se añadieron {len(objetos_agregados)} cuerpos")
                
                # si el valor de G es diferente al del archivo
                if (DCLD["G"] != g):
                    g = Decimal(DCLD["G"])
                    print(f"{c["verde"]}Se actualizo el valor de G{c["default"]}")
                    print(f"{c["verde"]}Nuevo valor de G es: {g}{c["default"]}")
                
            else:
                print_error(tipos_de_errores[3], "el archivo dado no existe")
        else:
            print_error(tipos_de_errores[1])

    # ~~~~~~~~~~~~~~~~~~~~ si dice "save" ~~~~~~~~~~~~~~~~~~~~ 
    elif input_separado[0] == "save":
        # -- si la cantidad de palabras es igual a 2 --
        if len(input_separado) == 2:
            # se crea la variable con los datos
            datos = crear_archivo_json(todos_los_cuerpos, g)
            # se crea el archivo
            with open(input_separado[1], 'w') as archivo:
                # se añaden los datos
                json.dump(datos, archivo, indent=4)
        else:
            print_error(tipos_de_errores[1])
    
    # ~~~~~~~~~~~~~~~~~~~~ si dice "time.mode" ~~~~~~~~~~~~~~~~~~~~ 
    elif input_separado[0] == "time.mode":
        # -- si la cantidad de palabras son 2 --
        if len(input_separado) == 2:
            # si la segunda palabra es delta_time
            if input_separado[1] == "delta_time":
                # se activa el modo delta_time
                time_mode = True
            else:
                # dar un error de sintaxis
                print_error(tipos_de_errores[1])
        
        # -- si tiene 3 palabras
        elif len(input_separado) == 3:
            # si la segunda palabra es uniform 
            if input_separado[1] == "uniform":
                # si la 3 palabra es un numero
                if es_numero(input_separado[2]) :
                    # si la 3 palabra es mayor a 0
                    if float(input_separado[2]) > 0:
                        # se activa el modo uniform
                        time_mode = False
                        uniform_time = float(input_separado[2])
                    else:
                        print_error(tipos_de_errores[0], "el tiempo tiene que ser mayor a 0")
                else:
                    print_error(tipos_de_errores[0], "el tiempo tiene que ser un valor float mayor a 0")
            else:
                print_error(tipos_de_errores[1])
        else:
            print_error(tipos_de_errores[1])
    
    # ~~~~~~~~~~~~~~~~~~~~ si dice "size" ~~~~~~~~~~~~~~~~~~~~
    elif input_separado[0] == "size":
        if len(input_separado) == 3:
            if input_separado[1] == "dots":
                if es_numero(input_separado[2]):
                    dot_scale = float(input_separado[2])
                    print(f"{c["amarillo"]}La nueva escala de los puntos. Ahora es: masa * {dot_scale}{c["default"]}")
                else:
                    print_error(tipos_de_errores[0])
            if input_separado[1] == "view":
                xy = input_separado[2].split(";")
                if len(xy) == 2:
                    if es_numero(xy[0]) and es_numero(xy[1]):
                        if float(xy[0]) > 0 and float(xy[1]) > 0:
                            view_scale = Vector2(float(xy[0]),float(xy[1]))
                            print(f"{c["amarillo"]}La nueva escala de vision. Ahora es: {view_scale}{c["default"]}")
                        else:
                            print_error(tipos_de_errores[0])
                    else:
                        print_error(tipos_de_errores[0])
                else:
                    print_error(tipos_de_errores[1])
            else:
                print_error(tipos_de_errores[3], "")
        else:
            print_error(tipos_de_errores[1])
    
    # ~~~~~~~~~~~~~~~~~~~~ si dice "solar_sistem" ~~~~~~~~~~~~~~~~~~~~
    elif input_separado[0] == "solar_sistem":
        if len(input_separado) == 3:
            if input_separado[1] == "asteroid_belt":
                if es_numero_int(input_separado[2]):
                    cantidad_de_asteroides_1 = int(input_separado[2])
                    print(f"{c['amarillo']}La cantidad de asteroides en el cinturon ahora es de: {cantidad_de_asteroides_1} {c["default"]}")
                else:
                    print_error(tipos_de_errores[0], "La cantidad de asteroides tiene que ser compatible con int")
            
            elif input_separado[1] == "kuiper_belt":
                if es_numero_int(input_separado[2]):
                    cantidad_de_asteroides_2 = int(input_separado[2])
                    print(f"{c['amarillo']}La cantidad de asteroides en el cinturon de kuiper ahora es de: {cantidad_de_asteroides_2} {c["default"]}")
                else:
                    print_error(tipos_de_errores[0], "La cantidad de asteroides tiene que ser compatible con int")
            
            elif input_separado[1] == "asteroids":
                if es_numero_int(input_separado[2]):
                    cantidad_de_asteroides_0 = int(input_separado[2])
                    print(f"{c['amarillo']}La cantidad de asteroides ahora es de: {cantidad_de_asteroides_0} {c["default"]}")
                else:
                    print_error(tipos_de_errores[0], "La cantidad de asteroides tiene que ser compatible con int")
            
            else:
                print_error(tipos_de_errores[3], f"El dato {input_separado[1]} no exite")
        else:
            print_error(tipos_de_errores[1], "La sintaxis deve ser: \"solar_sistem {valor a modificar} {cantidad}\"")
        
    # ~~~~~~~~~~~~~~~~~~~~ si dice "active_save" ~~~~~~~~~~~~~~~~~~~~
    elif input_separado[0] == "active_save":
        print(f"""{c["amarillo"]}Este comando gruarda los datos generados durante la simulacion, no los datos proporcionados en esta instancia
si lo que decea es guardar los datos iniciales proporcionados utilice el comando \"save\"
si decea cancelar este comando deje la casilla vacia{c["default"]}""")
        
        si = input('Ruta de guardado: ')
        if si != "":
            active_save = True
            save_in = si
            cic = input('Ciclos: ')
            while es_numero_int(cic) == False:
                print_error(tipos_de_errores[2],"la cantidad de ciclos debe de ser un valor int")
                cic = input('Ciclos: ')
                if cic == "":
                    break
            
            if cic != "":
                active_save = True
                ciclos = int(cic)
            else:
                active_save = False
        else:
            active_save = False

    else:
        # indicar un error al no ser un comando valido
        print_error(f"\"{input_del_usuario}\"", mensaje_extra="no es un comando valido. Para ayuda escriba: help")

grid = Grid(300,300, view_scale.x)

fisica = Fisica(g)
universo = Universo(fisica,grid)

# <- colocar funciones de generacion de cuerpos aqui

# ---------- crear asteroides aleatorios en todo el sistema solar ---------- 
for i in range(cantidad_de_asteroides_0):
    n_posicion = Vector2(Decimal(random.uniform(-4558857000000, 4558857000000)), Decimal(random.uniform(-4558857000000, 4558857000000)))
    n_velocidad = Vector2(0,0)
    
    cuerpo_temp = Cuerpo(str(i), n_posicion, n_velocidad, Decimal(2.8e21))
    M_velocidad = universo.fisica.calcular_velocidad_orbital(todos_los_cuerpos[0], cuerpo_temp)
    # calcular el vector de la direccion usando trigonometria
    ang = atan2(n_posicion.y, n_posicion.x)
    n_velocidad.x = M_velocidad * Decimal(cos(ang + 1.57079632679))
    n_velocidad.y = M_velocidad * Decimal(sin(ang + 1.57079632679))
    
    cuerpo = Cuerpo(str(i), n_posicion, n_velocidad, Decimal(2.8e21), 3, exact=False)
    todos_los_aproximados.append(cuerpo)

# ---------- crear asteroides en el cinturon de asteroides ---------- 
for i in range(cantidad_de_asteroides_1):
    n_posicion = Vector2(Decimal(random.uniform(-508632758000, 508632758000)), Decimal(random.uniform(-508632758000, 508632758000)))
    while Decimal(3.291e+11) > Decimal_distancia(Vector2(0,0), n_posicion) or Decimal_distancia(Vector2(0,0), n_posicion) > Decimal(4.787e+11):
        n_posicion = Vector2(Decimal(random.uniform(-508632758000, 508632758000)), Decimal(random.uniform(-508632758000, 508632758000)))

    # print(str(Decimal_distancia(Vector2(0,0), n_posicion)))

    n_velocidad = Vector2(0,0)
    
    cuerpo_temp = Cuerpo(str(i), n_posicion, n_velocidad, Decimal(2.8e21))
    M_velocidad = universo.fisica.calcular_velocidad_orbital(todos_los_cuerpos[0], cuerpo_temp)
    # calcular el vector de la direccion usando trigonometria
    ang = atan2(n_posicion.y, n_posicion.x)
    n_velocidad.x = M_velocidad * Decimal(cos(ang + 1.57079632679))
    n_velocidad.y = M_velocidad * Decimal(sin(ang + 1.57079632679))
    
    # print(str(n_velocidad))
    # print(str(n_velocidad.magnitud()))
    
    cuerpo_nuevo = Cuerpo(str(i) + " Cinturon", n_posicion, n_velocidad, Decimal(2.8e21), diam=3, exact=False)
    todos_los_aproximados.append(cuerpo_nuevo)

# ---------- crear asteroides en el cinturon de kuiper ---------- 
for i in range(cantidad_de_asteroides_2):
    n_posicion = Vector2(Decimal(random.uniform(-7.48e+12, 7.48e+12)), Decimal(random.uniform(-7.48e+12, 7.48e+12)))
    while Decimal(4488000000000) > Decimal_distancia(Vector2(0,0), n_posicion) or Decimal_distancia(Vector2(0,0), n_posicion) > Decimal(7480000000000):
        n_posicion = Vector2(Decimal(random.uniform(-7.48e+12, 7.48e+12)), Decimal(random.uniform(-7.48e+12, 7.48e+12)))
        
    # print(str(Decimal_distancia(Vector2(0,0), n_posicion)))
    n_velocidad = Vector2(0,0)
    
    cuerpo_temp = Cuerpo(str(i), n_posicion, n_velocidad, Decimal(2.8e21))
    M_velocidad = universo.fisica.calcular_velocidad_orbital(todos_los_cuerpos[0], cuerpo_temp)
    # calcular el vector de la direccion usando trigonometria
    ang = atan2(n_posicion.y, n_posicion.x)
    n_velocidad.x = M_velocidad * Decimal(cos(ang + 1.57079632679))
    n_velocidad.y = M_velocidad * Decimal(sin(ang + 1.57079632679))
    
    # print(str(n_velocidad))
    # print(str(n_velocidad.magnitud()))
    
    cuerpo_nuevo = Cuerpo(str(i) + " Cinturon", n_posicion, n_velocidad, Decimal(2.8e21), diam=3, exact=False)
    todos_los_aproximados.append(cuerpo_nuevo)

universo.grid.actualizar(todos_los_aproximados)

# Uso de la clase para tener la ventana
puntos = Puntos()

# Agregar los puntos para cada cuerpo
puntos.agregar_cuerpos(todos_los_cuerpos)

puntos.agregar_cuerpos(todos_los_aproximados)

for i in puntos.cuerpos:
    print(i.nombre)
# iniciar la animacion
puntos.iniciar_animacion()

# variable para el delta time
last_time = time.perf_counter()

UPT = time.perf_counter()

tiempo_inicial = time.perf_counter()
tiempo_transcurrido = 0 

# ---------------- empezando el bucle infinito ---------------------------
# ---------------- empezando el bucle infinito ---------------------------
# Inicialización de variables para el bucle
ciclos_transcurridos = 0
last_time = time.perf_counter() # Necesario para el primer cálculo de delta_time
tiempo_transcurrido = 0

while True:
    # --- 1. CALCULAR EL TIEMPO TRANSCURRIDO (delta_time) ---
    # Esto debe ser lo PRIMERO en el bucle, ya que la física depende de ello.
    if time_mode:
        current_time = time.perf_counter()
        delta_time = current_time - last_time
        last_time = current_time
    else:
        delta_time = uniform_time
    
    tiempo_transcurrido += delta_time

    # --- 2. ACTUALIZAR LA FÍSICA DE TODOS LOS CUERPOS ---
    # a) Gravedad entre los cuerpos principales (exactos)
    for i, objeto in enumerate(todos_los_cuerpos):
        for otros_objetos in todos_los_cuerpos[i+1:]:
            objeto.aplicar_gravedad(otros_objetos, delta_time)
    
    # b) Gravedad entre los cuerpos aproximados (usando la Grid)
    todos_los_casilleros = universo.grid.get_all()
    for pos in todos_los_casilleros:
        centro_de_masas = pos.centro_de_masa()
        # Creamos un cuerpo temporal que representa el centro de masas del casillero
        este = Cuerpo("cm", centro_de_masas, Vector2(0,0), pos.masa)
        
        # Aplicar la fuerza de los cuerpos principales a los aproximados de este casillero
        for otro_principal in todos_los_cuerpos:
            fuerza = universo.fisica.gravedad(este, otro_principal)
            for cuerpo_en_casillero in pos.valor:
                cuerpo_en_casillero.aplicar_fuerza(fuerza * -1, delta_time)
    
    # c) Mover todos los cuerpos según su velocidad final
    for i in todos_los_cuerpos:
        i.constante(delta_time)
        
    for pos in todos_los_casilleros:
        for cuerpo_en_casillero in pos.valor:
            cuerpo_en_casillero.constante(delta_time)
            
    # d) Actualizar la grid con las nuevas posiciones de los cuerpos aproximados
    universo.grid.actualizar(todos_los_aproximados)

    # --- 3. IMPRIMIR EL ESTADO ACTUAL ---
    # Imprimimos los resultados DESPUÉS de haberlos calculado en este ciclo.
    if time_mode:
        print(f"Delta Time: {delta_time}")
    
    # Se eliminó la línea "print(f"---------------------> {DTPT}")" que causaba el NameError.
    print(f"Tiempo transcurrido: {str(tiempo_transcurrido /60/60/24)} dias")

    # --- 4. PAUSAR PARA PERMITIR QUE LA VENTANA SE DIBUJE ---
    # Esta pausa le da tiempo al backend gráfico para renderizar la animación.
    plt.pause(0.001)

    # --- 5. GESTIONAR EL GUARDADO Y LA SALIDA DEL BUCLE ---
    if active_save:
        ciclos_transcurridos += 1
        for i in todos_los_cuerpos:
            i.guardar_pos()
        
        if ciclos_transcurridos >= ciclos:
            print("Guardado automático completado. Terminando simulación.")
            break

# --- CÓDIGO DE GUARDADO FINAL (FUERA DEL BUCLE) ---
if active_save:
    # Se crea la variable con los datos
    datos = crear_archivo_json_de_sim(todos_los_cuerpos, ciclos)
    # Se crea el archivo
    with open(save_in, 'w') as archivo:
        # Se añaden los datos
        json.dump(datos, archivo, indent=4)
        print(f"Datos de la simulación guardados en: {save_in}")
    
