import random
import pygame
import pygame.freetype
from pygame.locals import *
from configuracion import *
import sys


def dameLetraApretada(key):
    if K_0 <= key <= K_9:
        return str(key - K_0)
    else:
        return ""


def dibujar(screen, productos_en_pantalla, producto_principal, producto_candidato, puntos, segundos):
    pygame.init()

    defaultFont = pygame.font.Font(pygame.font.get_default_font(), 20)
    defaultFontGrande = pygame.font.Font(pygame.font.get_default_font(), 30)

    # Linea del piso
    pygame.draw.line(screen, (255, 255, 255),
                     (0, ALTO-70), (ANCHO, ALTO-70), 5)
    ren1 = defaultFont.render(producto_candidato, 1, COLOR_TEXTO)
    ren2 = defaultFont.render("Puntos: " + str(puntos), 1, COLOR_TEXTO)
    if (segundos < 15):
        ren3 = defaultFont.render(
            "Tiempo: " + str(int(segundos)), 1, COLOR_TIEMPO_FINAL)
    else:
        ren3 = defaultFont.render(
            "Tiempo: " + str(int(segundos)), 1, COLOR_TEXTO)
   # Dibujar los nombres de los productos uno debajo del otro
    x_pos = 130
    y_pos = ALTO - (ALTO-100)

    pos = 0
    for producto in productos_en_pantalla:
        nombre_en_pantalla = str(pos) + " - "+producto[0]+producto[1]
        if producto[0] == producto_principal[0] and producto[1]== producto_principal[1]:
            screen.blit(defaultFontGrande.render(nombre_en_pantalla,
                        1, COLOR_TIEMPO_FINAL), (x_pos, y_pos))
        else:
            screen.blit(defaultFontGrande.render(
                nombre_en_pantalla, 1, COLOR_LETRAS), (x_pos, y_pos))
        pos += 1
        y_pos += ESPACIO

    screen.blit(ren1, (190, 570))
    screen.blit(ren2, (600, 10))
    screen.blit(ren3, (10, 10))



###funcion que guarda el puntaje del jugador
##def guardar_puntos(jugador ,puntos, nombreArchivo):
##    nombre_jugador= str(jugador)
##    añadir = str(puntos)  # Convierte 'puntos' a cadena para escribirlo en el archivo.
##    with open(nombreArchivo, "a") as archivo:  # Abre el archivo en modo de "anexar" (append).
##        archivo.write(nombre_jugador + ",")
##        archivo.write(añadir + "\n")  # Escribe el puntaje en el archivo, seguido de un salto de línea.
##        print("Su puntaje se ha guardado correctamente")
##
##
##
###funcion que crea un cuadro interactivo para que el jugador ingrese su nombre y asi poder guardarlo despues
###el archivo con los puntajes
##
###esta funcion es para despues poder mostrar el score
##def nombreDelJugador():
##
##    screen = pygame.display.set_mode((800, 600)) #dibuja la pantalla
##
##    # Crear una fuente
##    font = pygame.font.Font(None, 40)
##
##    # Crear un cuadro de entrada de texto
##    input_box = pygame.Rect(300, 300, 200, 32)
##    color_inactive = pygame.Color('lightskyblue3')
##    color_active = pygame.Color('dodgerblue2')
##    color = color_inactive
##    active = False
##    text = ''
##    done = False
##
##    while not done:
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                done = True
##            if event.type == pygame.MOUSEBUTTONDOWN:
##                if input_box.collidepoint(event.pos):
##                    active = not active
##                else:
##                    active = False
##                color = color_active if active else color_inactive
##            if event.type == pygame.KEYDOWN:
##                if active:
##                    if event.key == pygame.K_RETURN:
##                        print(text)
##                        done = True# Terminar el bucle una vez que el jugador presione Enter
##
##                    elif event.key == pygame.K_BACKSPACE:
##                        text = text[:-1]
##                    else:
##                        text += event.unicode
##
##        screen.fill((0, 0, 0))
##                # Renderizar el título "Ingrese su nombre" en un objeto Surface
##        text_surface = font.render("Ingrese su nombre", True, (255, 255, 0))
##
##        # Dibujar el título en la pantalla en las coordenadas especificadas
##        screen.blit(text_surface, (280, 200))
##
##        txt_surface = font.render(text, True, (255, 255, 255))
##        width = max(200, txt_surface.get_width()+10)
##        input_box.w = width
##        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
##        pygame.draw.rect(screen, color, input_box, 2)
##
##        pygame.display.flip()
##    return text
##
###funcion que ordena el score con los puntajes de mayor a menor
##def ranking(nombreArchivo):
##    try:
##        # Procesar el archivo de puntuaciones
##        puntajes = open(nombreArchivo, "r", encoding="utf-8")
##        puntuaciones = []
##        nombres = []
##        puntos = []
##
##        for punto in puntajes:
##            puntuaciones.append(punto[:-1])
##
##        for i in puntuaciones:
##            aux = i.split(",")
##            nombres.append(aux[0])
##            puntos.append(int(aux[1]))
##
##        datos = list(zip(nombres, puntos))
##        datos_ordenados = sorted(datos, key=lambda x: x[1], reverse=True)
##        nombres_ordenados, puntos_ordenados = zip(*datos_ordenados)
##
##        puntajes.close()
##        return nombres_ordenados, puntos_ordenados
##
##    except (IndexError, ValueError):
##        return [], []  # Devolver listas vacías si hay un error en el formato del archivo
##
##
##
##
##
##
##
