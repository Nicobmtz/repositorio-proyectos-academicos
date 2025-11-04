from principal import *
from configuracion import *
import random
import math
from extras import *

# Función para leer el archivo de productos y cargarlos en una lista
def lectura():
    with open("productos.txt", "r", encoding="utf-8") as productos:
        listaProd = []
        for producto in productos:
            listaProd.append(producto[:-1])  # Elimina el carácter de nueva línea
    return listaProd

# Función que elige un producto al azar y devuelve una lista con sus detalles
def buscar_producto(lista_productos):
    prodElegido = []
    prodElegido.append(random.choice(lista_productos))
    producto = prodElegido[0].split(",")
    tipo = ["economico", "premium"]
    prodFinal = []
    prodFinal.append(producto[0])
    eleccion = random.choice(tipo)
    prodFinal.append(eleccion)
    if eleccion == "economico":
        prodFinal.append(producto[1])
    else:
        prodFinal.append(producto[2])
    return prodFinal

# Función que elige un producto principal, asegurándose de que haya productos similares
def dameProducto(lista_productos, margen):
    while True:
        producto = buscar_producto(lectura())
        precio = int(producto[2])
        if esUnPrecioValido(precio, lista_productos, margen) == True:
            break
        else:
            producto = buscar_producto(lectura())
    return producto

# Función que verifica si el precio aparece al menos 3 veces en la lista de productos
def esUnPrecioValido(precio, lista_productos, margen):
    cont = 0
    for producto in lista_productos:
        nombre, precioEco, precioPrem = producto.split(",")
        precioEco = int(precioEco)
        precioPrem = int(precioPrem)
        valido = False
        if abs(precioEco - precio) <= margen or abs(precioPrem - precio) <= margen:
            cont += 1
        if cont >= 3:
            valido = True
            break
    return valido

# Función que procesa los productos seleccionados, sumando los precios si son válidos
def procesar(producto_principal, producto_candidato, margen):
    precio_principal = int(producto_principal[2])
    precio_candidato = int(producto_candidato[2])

    if abs(precio_principal - precio_candidato) <= margen:
        # Ambos productos son válidos, así que sumamos sus precios
        total_canasta = precio_principal + precio_candidato
        return total_canasta
    else:
        total_canasta = (- precio_principal - precio_candidato)
        # El producto candidato no es válido, devolvemos solo el precio del producto principal
        return total_canasta

# Función que elige productos aleatorios, garantizando que al menos 2 tengan el mismo precio
# y agrega etiquetas de calidad a los nombres de los productos
def dameProductosAleatorios(producto, lista_productos, margen):
    productos = [producto]
    while len(productos) < 6:
        prod = dameProducto(lista_productos, margen)
        if prod not in productos:
            productos.append(prod)
    for x in range(len(productos)):
        if productos[x][1] == "economico":
            productos[x][1] = f"({productos[x][1]})"
        elif productos[x][1] == "premium":
            productos[x][1] = f"({productos[x][1]})"
    productos_seleccionados = productos
    return productos_seleccionados


