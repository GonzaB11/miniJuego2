import os
import random
import sys
import math
import pygame
from pygame.locals import *
from configuracion import *
from funcionesVACIAS import *
from extras import *

# Cargar el fondo de pantalla y ajustar al tamaño de la pantalla
fondo_img = pygame.image.load("fondo.jpg")
fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))

# Función para mostrar el menú y obtener la opción seleccionada por el usuario
def menu(screen):
    pygame.mouse.set_visible(True)  # Mostrar el cursor del mouse

    # Cargar la fuente de texto para las opciones del menú
    fuente = pygame.font.Font(None, 150)  # tamaño de letra

    # Opción "Jugar"
    texto_jugar = fuente.render("Jugar", True, COLOR_TEXTO)  # Usar el color definido en la configuración
    posicion_texto_jugar = texto_jugar.get_rect(center=(380, 200))  # posición en la pantalla

    # Opción "Salir"
    texto_salir = fuente.render("Salir", True, COLOR_TEXTO)  # Usar el color definido en la configuración
    posicion_texto_salir = texto_salir.get_rect(center=(380, 400))  # posición en la pantalla

    opcion = None
    while opcion is None:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if posicion_texto_jugar.collidepoint(pos):
                    opcion = "1"
                elif posicion_texto_salir.collidepoint(pos):
                    opcion = "2"
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(fondo_img, (0, 0))  # Dibujar el fondo en la pantalla
        # Dibujar el texto "Jugar" en la pantalla
        screen.blit(texto_jugar, posicion_texto_jugar)
        # Dibujar el texto "Salir" en la pantalla
        screen.blit(texto_salir, posicion_texto_salir)
        pygame.display.flip()

    return opcion


# Función principal
def main():
    # Centrar la ventana y luego inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    # Preparar la ventana
    pygame.display.set_caption("Armar palabras con...")
    screen = pygame.display.set_mode((ANCHO, ALTO))

    # Tiempo total del juego
    gameClock = pygame.time.Clock()
    totaltime = 0
    segundos = TIEMPO_MAX
    fps = FPS_inicial

    puntos = 0
    candidata = ""
    diccionario = []

    # Leer el diccionario
    lectura(diccionario)

    while True:
        opcion = menu(screen)

        if opcion == "1":
            # Elegir las 7 letras al azar y una de ellas como principal
            letrasEnPantalla = dame7Letras()
            letraPrincipal = dameLetra(letrasEnPantalla)

            # Quedarse con 7 letras que permitan armar muchas palabras
            while len(dameAlgunasCorrectas(letraPrincipal, letrasEnPantalla, diccionario)) < MINIMO:
                letrasEnPantalla = dame7Letras()
                letraPrincipal = dameLetra(letrasEnPantalla)

            # Dibujar la pantalla por primera vez
            dibujar(screen, letraPrincipal, letrasEnPantalla, candidata, puntos, segundos)

            while segundos > fps / 1000:
                # 1 frame cada 1/fps segundos
                gameClock.tick(fps)
                totaltime += gameClock.get_time()

                if True:
                    fps = 3

                # Buscar la tecla apretada del módulo de eventos de pygame
                for e in pygame.event.get():

                    # QUIT es apretar la X en la ventana
                    if e.type == QUIT:
                        pygame.quit()
                        return

                    # Ver si fue apretada alguna tecla
                    if e.type == KEYDOWN:
                        letra = dameLetraApretada(e.key)
                        candidata += letra  # va concatenando las letras que escribe
                        if e.key == K_BACKSPACE:
                            candidata = candidata[0: len(candidata) - 1]  # borra la última
                        if e.key == K_RETURN:  # presionó enter
                            puntos += procesar(letraPrincipal, letrasEnPantalla, candidata, diccionario)
                            candidata = ""

                segundos = TIEMPO_MAX - pygame.time.get_ticks() / 1000

                # Limpiar pantalla anterior
                screen.blit(fondo_img, (0, 0))

                # Dibujar de nuevo todo
                dibujar(screen, letraPrincipal, letrasEnPantalla, candidata, puntos, segundos)
                pygame.display.flip()

        elif opcion == "2":
            pygame.quit()
            return

# Programa Principal ejecuta Main
if __name__ == "__main__":
    main()

