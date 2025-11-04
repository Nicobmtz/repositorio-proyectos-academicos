#! /usr/bin/env python
import os
import random
import sys
import math

import pygame
from pygame.locals import *

from configuracion import *      #revisar porwue el tiempo empieza en 10
from funciones import *
from extras import *
from funcionesExtras import *


def main():

    jugador= nombreDelJugador() #le pide al jugador que ingrese su nombre para despues guardarlo

    # tiempo total del juego
    gameClock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()  #obtener el tiempo actual
    totaltime = 0
    segundos = TIEMPO_MAX
    fps = FPS_inicial

    puntos = 0  # Puntos del jugador
    producto_candidato = ""
    #Para poder hacer la verificacion para el sonido
    acumulado=0

    #Lee el archivo y devuelve una lista con los productos,
    lista_productos = lectura()  # lista de productos

    # Elegir un producto, [producto, calidad, precio]
    producto = dameProducto(lista_productos, MARGEN)

    # Elegimos productos aleatorios, garantizando que al menos 2 mas tengan el mismo precio.
    # De manera aleatoria se debera tomar el valor economico o el valor premium.
    # Agregar  '(economico)' o '(premium)' y el precio
    productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, MARGEN)
    print(productos_en_pantalla)

    # dibuja la pantalla la primera vez
    dibujar(screen, productos_en_pantalla, producto,
            producto_candidato, puntos, segundos)

    while segundos > fps/1000:
        # 1 frame cada 1/fps segundos
        gameClock.tick(fps)
        totaltime += gameClock.get_time()
        if True:
            fps = 3

        # Buscar la tecla apretada del modulo de eventos de pygame
        for e in pygame.event.get():
            # QUIT es apretar la X en la ventana
            if e.type == QUIT:
                pygame.quit()
                return ()
            #codigo aapara habilitar el uso del mouse
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:  # Clic izquierdo
                    x, y = e.pos
                    prod_candidato= manejar_interaccion_con_el_mouse(x, y, productos_en_pantalla)
                    if prod_candidato != producto:
                        puntos+=procesar(producto, prod_candidato, MARGEN)
                        if puntos>acumulado: #codigo para agregar efectos de sonido
                            pygame.mixer.music.load("sonido_correcto.mp3")
                            pygame.mixer.music.play(1)
                            acumulado=puntos
                        else:
                            pygame.mixer.music.load("sonido_error.mp3")
                            pygame.mixer.music.play(1)
                            acumulado=puntos


                        producto_candidato = ""
                        # Elegir un producto
                        producto = dameProducto(lista_productos, MARGEN)
                        # elegimos productos aleatorios, garantizando que al menos 2 mas tengan el mismo precio
                        productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, MARGEN)
                # Ver si fue apretada alguna tecla
            elif e.type == KEYDOWN:
                letra = dameLetraApretada(e.key)
                producto_candidato += letra  # va concatenando las letras que escribe
                if e.key == K_BACKSPACE:
                    # borra la ultima
                    producto_candidato = producto_candidato[0:len(producto_candidato)-1]
                if e.key == K_RETURN:  # presionó enter
                    indice = int(producto_candidato)
                    # chequeamos si el prducto no es el producto principal. Si no lo es procesamos el producto
                    if indice < len(productos_en_pantalla):
                        puntos += procesar(producto, productos_en_pantalla[indice], MARGEN)

                        if puntos>acumulado: #codigo para agregar efectos de sonido
                            pygame.mixer.music.load("sonido_correcto.mp3")
                            pygame.mixer.music.play(1)
                            acumulado=puntos
                        else:
                            pygame.mixer.music.load("sonido_error.mp3")
                            pygame.mixer.music.play(1)
                            acumulado=puntos

                        producto_candidato = ""
                        # Elegir un producto
                        producto = dameProducto(lista_productos, MARGEN)
                        # elegimos productos aleatorios, garantizando que al menos 2 mas tengan el mismo precio
                        productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, MARGEN)
                    else:
                        producto_candidato = ""

        segundos = TIEMPO_MAX - (pygame.time.get_ticks() - start_ticks) / 1000  # restar el tiempo de inicio


        # Verificar si el tiempo ha llegado a 0
        if segundos <= 0:  # Cuando el tiempo es cero, guarda los puntos en el archivo
            guardar_puntos(jugador, puntos, "puntuaciones.txt")
            mostrar_puntuacion(screen, puntos)  # Muestra la puntuación final
            pygame.display.flip()

            # Esperar a que el jugador presione Enter para volver al menú
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return "QUIT"
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            return "MENU"  # Regresar al menú principal
        # Limpiar pantalla anterior
        screen.fill(COLOR_FONDO)
        # Dibujar de nuevo todo
        dibujar(screen, productos_en_pantalla, producto,
                producto_candidato, puntos, segundos)
        pygame.display.flip()

    while 1:
        # Esperar el QUIT del usuario
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return

# Inicialización de la ventana de juego y otros elementos necesarios
if __name__ == "__main__":
    # Centrar la ventana y después inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.display.set_caption("Peguele al precio")
    screen = pygame.display.set_mode((ANCHO, ALTO))

    # Define las fuentes y colores
    font = pygame.font.Font(None, 50)
    selected_color = (255, 255, 0)
    normal_color = (255, 255, 255)

    # Variables de colores para Score
    blanco = (255, 255, 255)
    negro = (0, 0, 0)
    nombres, puntos = ranking("puntuaciones.txt")# Obtener las puntuaciones al inicio del programa

    # Define las opciones del menú
    menu_options = ["Start", "Score", "Quit"]
    selected_option = 0  # Opción seleccionada inicialmente
    en_menu = True  # Indicador de si estás en el menú

    def mostrar_lista():
         # Mostrar la lista de puntajes
        screen.fill(negro)
        message = font.render("Presione ESC para volver al Menú Principal", True, (255, 255, 0))
        screen.blit(message, (50,500))  # Ajustar la posición del mensaje
        for i, (nombre, puntaje) in enumerate(zip(nombres, puntos)):
            texto = font.render(f"{nombre}: {puntaje}", True, blanco)
            screen.blit(texto, (50, 50 + i * 30))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if en_menu:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Opción "Start"
                            en_menu = False  # Cambiar a juego principal
                        elif selected_option == 1:  # Opción "Score"
                            show_scores = True  # Variable para controlar la visualización del ranking
                            while show_scores:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        show_scores = False
                                        running = False  # Si se cierra la ventana, detener el juego
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_ESCAPE:
                                            show_scores = False  # Presionar ESC para salir del ranking
                                screen.fill((0, 0, 0))
                                mostrar_lista()
                                pygame.display.flip()
                            en_menu = True  # Volver al menú después de ver el ranking
                        elif selected_option == 2:  # Opción "Quit"
                            running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Obtener las coordenadas del clic del mouse
                    x, y = pygame.mouse.get_pos()
                    # Verificar si el clic está sobre alguna opción del menú
                    for i, option in enumerate(menu_options):
                        # Crear un rectángulo alrededor del texto de la opción
                        text_rect = font.render(option, True, normal_color).get_rect(center=(ANCHO / 2, ALTO / 2 + i * 40))
                        # Verificar si las coordenadas del clic están dentro del rectángulo
                        if text_rect.collidepoint(x, y):
                            selected_option = i
                            if selected_option == 0:  # Opción "Start"
                                en_menu = False  # Cambiar a juego principal
                            elif selected_option == 1:  # Opción "Score"
                                show_scores = True  # Variable para controlar la visualización del ranking
                                while show_scores:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            show_scores = False
                                            running = False  # Si se cierra la ventana, detener el juego
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_ESCAPE:
                                            show_scores = False  # Presionar ESC para salir del ranking
                                    screen.fill((0, 0, 0))
                                    mostrar_lista()
                                    pygame.display.flip()

                                en_menu = True  # Volver al menú después de ver el ranking
                            elif selected_option == 2:  # Opción "Quit"
                                running = False
            elif not en_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = main()  # Llama a la función del juego principal

                elif selected_option == 2:  # Opción "Quit"
                    running = False

        screen.fill((0, 0, 0))

        if en_menu:
            # Estás en el menú
            for i, option in enumerate(menu_options):
                color = selected_color if i == selected_option else normal_color
                text = font.render(option, True, color)
                text_rect = text.get_rect(center=(ANCHO / 2, ALTO / 2 + i * 40))
                screen.blit(text, text_rect)
        elif not en_menu:
            # Estás en el juego principal
            action = main()  # Llama a la función del juego principal

            if action == "MENU":
                en_menu = True  # Regresar al menú principal
            elif action == "QUIT":
                running = False  # Salir del juego

        if pygame.display.get_init():
            pygame.display.flip()

    if not running:
        pygame.quit()