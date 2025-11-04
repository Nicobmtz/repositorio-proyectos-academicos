#! /usr/bin/env python
import random
import pygame
import pygame.freetype
import sys
import os
import math
from pygame.locals import *
from configuracion import *
from configuracion import *
from funciones import *
from extras import *
from principal import *




def guardar_puntos(jugador ,puntos, nombreArchivo):
    nombre_jugador= str(jugador)
    añadir = str(puntos)  # Convierte 'puntos' a cadena para escribirlo en el archivo.
    with open(nombreArchivo, "a") as archivo:  # Abre el archivo en modo de "anexar" (append).
        archivo.write(nombre_jugador + ", ")
        archivo.write(añadir + "\n")  # Escribe el puntaje en el archivo, seguido de un salto de línea.
        print("Su puntaje se ha guardado correctamente")



#funcion para el ranking

def ranking(nombreArchivo):
    puntajes= open(nombreArchivo, "r")
    puntuaciones=[]
    nombres=[]
    puntos=[]

    for punto in puntajes:
        puntuaciones.append(punto[:-1])

    for i in puntuaciones:

        aux= i.split(",")
        nombres.append(aux[0])
        puntos.append(int(aux[1]))

# Combina las dos listas en una lista de tuplas (nombre, puntaje)
    datos = list(zip(nombres, puntos))

    # Ordena la lista de tuplas en función de los puntajes de mayor a menor
    datos_ordenados = sorted(datos, key=lambda x: x[1], reverse=True)

    # Separa los nombres y los puntajes ordenados en listas separadas
    nombres_ordenados, puntos_ordenados = zip(*datos_ordenados)

    # Ahora, nombres_ordenados contendrá los nombres ordenados y puntos_ordenados contendrá los puntajes ordenados de mayor a menor.
    puntajes.close()
    return nombres_ordenados, puntos_ordenados

#funcion que guarda el puntaje del jugador
def guardar_puntos(jugador ,puntos, nombreArchivo):
    nombre_jugador= str(jugador)
    añadir = str(puntos)  # Convierte 'puntos' a cadena para escribirlo en el archivo.
    with open(nombreArchivo, "a") as archivo:  # Abre el archivo en modo de "anexar" (append).
        archivo.write(nombre_jugador + ",")
        archivo.write(añadir + "\n")  # Escribe el puntaje en el archivo, seguido de un salto de línea.
        print("Su puntaje se ha guardado correctamente")



#funcion que crea un cuadro interactivo para que el jugador ingrese su nombre y asi poder guardarlo despues
#el archivo con los puntajes

#esta funcion es para despues poder mostrar el score
def nombreDelJugador():
    #dibuja la pantalla
    screen = pygame.display.set_mode((800, 600))

    # Crear una fuente
    font = pygame.font.Font(None, 40)

    # Crear un cuadro de entrada de texto
    input_box = pygame.Rect(300, 300, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        done = True# Terminar el bucle una vez que el jugador presione Enter

                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((0, 0, 0))
                # Renderizar el título "Ingrese su nombre" en un objeto Surface
        text_surface = font.render("Ingrese su nombre", True, (255, 255, 0))

        # Dibujar el título en la pantalla en las coordenadas especificadas
        screen.blit(text_surface, (280, 200))

        txt_surface = font.render(text, True, (255, 255, 255))
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
    return text

#funcion que ordena el score con los puntajes de mayor a menor
def ranking(nombreArchivo):
    try:
        # Procesar el archivo de puntuaciones
        puntajes = open(nombreArchivo, "r", encoding="utf-8")
        puntuaciones = []
        nombres = []
        puntos = []

        for punto in puntajes:
            puntuaciones.append(punto[:-1])

        for i in puntuaciones:
            aux = i.split(",")
            nombres.append(aux[0])
            puntos.append(int(aux[1]))

        datos = list(zip(nombres, puntos))
        datos_ordenados = sorted(datos, key=lambda x: x[1], reverse=True)
        nombres_ordenados, puntos_ordenados = zip(*datos_ordenados)

        puntajes.close()
        return nombres_ordenados, puntos_ordenados

    except (IndexError, ValueError):
        return [], []  # Devolver listas vacías si hay un error en el formato del archivo

def mostrar_puntuacion(screen, puntos):
    screen.fill(COLOR_FONDO)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Tu puntuación es: {puntos}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(ANCHO / 2, ALTO / 2 - 50))  # Modificado para mostrar las opciones un poco más abajo

    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 24)
    message = font.render("Presione ENTER para volver al Menú Principal", True, (255, 255, 0))
    message_rect = message.get_rect(center=(ANCHO / 2, ALTO / 2 + 100))  # Ajustar la posición del mensaje

    screen.blit(message, message_rect)
    pygame.display.flip()

    while True:
        enter_pressed = False  # Variable para controlar si se presionó Enter

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Sale de la función sin retornar nada

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    enter_pressed = True  # Se detecta la tecla Enter
                    break  # Salir del bucle cuando se presiona Enter

        if enter_pressed:
            return "MENU"  # Retorna 'MENU' para volver al menú principal

#recibe la posicion del mouse y para calcular si esta sobre uno de los productos en pantalla
# toma los parametros de configuracion.
def manejar_interaccion_con_el_mouse(x,y, productos_en_pantalla):
    for i, producto in enumerate(productos_en_pantalla):
        y_pos = ALTO - (ALTO - 100) + i * ESPACIO
        if y_pos <= y <= y_pos + ESPACIO:
            producto_candidato=producto
            print(producto_candidato)
    return producto_candidato


