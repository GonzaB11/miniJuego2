from principal import *
from configuracion import *
import random
import math

#lista de palabras acertadas para no sumar puntos con palabras correctas ingresadas antes
palabrasAcertadas= []


#MUSICA DE FONDO
pygame.mixer.init()
pygame.mixer.music.set_volume(0.3)  # Ajusta el volumen de la musica principal (rango de 0.0 a 1.0)
pygame.mixer.music.load("Signos.mp3")
pygame.mixer.music.play(-1)  # Con -1 indicamos que queremos que se repita indefinidamente


#Ajustamos el volumen sonido para palabras correctas e incorrectas establecidas en el canal 0
pygame.mixer.Channel(0).set_volume(0.2)


#lee el archivo y carga en la lista diccionario todas las palabras
def lectura(diccionario): #aREVER
    archivo= open("lemario.txt","r")
    lista=archivo.readlines()
    for palabra in lista:
        palabra = palabra.strip() #Eliminar espacios en blanco y caracteres de nueva linea
        diccionario.append(palabra)
    archivo.close()


#Devuelve una cadena de 7 caracteres sin repetir con 2 o 3 vocales y a lo sumo
# con una consonante dificil
def dame7Letras():
    sieteLetras = ""   #Se van a ir almacenando aca las letras y esta variable se retornará

    vocales = ["a", "e", "i", "o", "u"]   #De esta varible sacaremos las vocales necesarias
    dificiles = ["h", "k", "q", "x", "w", "y", "z"]   #De esta varible sacaremos un caracter dificil de ser necesario

    vocalesRestantes = random.sample(vocales, random.randint(2, 3))  #Elije 2 o 3 vocales

    for vocal in range(len(vocalesRestantes)):
        sieteLetras = sieteLetras + vocalesRestantes[vocal]   #Agrega las vocales selccionadas a la variable sieteLetras

    a = random.choice("18")
    if a == "1":    #Decide si agregara o no un caracter dificil
        letraDificil = random.choice(dificiles)
        sieteLetras = sieteLetras + letraDificil   #Se agrega un caracter dificil si el programa asi lo decide

    while len(sieteLetras) < 7:   #El siguiente bloque de codigo agrega letras hasta completar la cantidad y no podra haber letras repetidas
        caracter = random.choice("bcdfgjlmnprstv")
        if caracter not in sieteLetras:
            sieteLetras = sieteLetras + caracter
    return sieteLetras


def dameLetra(letrasEnPantalla): #elige una letra de las letras en pantalla
    letra = random.choice(letrasEnPantalla)
    return letra


#si es valida la palabra devuelve puntos sino resta.
def procesar(letraPrincipal, letrasEnPantalla, candidata, diccionario):

    if esValida(letraPrincipal,letrasEnPantalla, candidata, diccionario, palabrasAcertadas):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("correcto.mp3"))
        return Puntos(candidata)
    else:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("incorrecto.mp3"))
        return -1


#chequea que se use la letra principal, solo use letras de la pantalla y
#exista en el diccionario
def esValida(letraPrincipal, letrasEnPantalla, candidata, diccionario, palabrasAcertadas):
    if len(candidata)<3:
        return False

    if letraPrincipal not in candidata:
        return False

    if candidata in palabrasAcertadas:
        return  False

    # me fijo que solo se usen letras de la pantalla
    for letra in candidata:
        if letra not in letrasEnPantalla: #Pregunto si letra no estan en las letras de pantalla
            return False #Si es asi devuelvo falso y sino sigo
        else:
            palabrasAcertadas.append(candidata)

    # Verifico que la palabra este en diccionario
    return candidata in diccionario


#devuelve los puntos
def Puntos(candidata):
    puntos = 0
    if len(candidata) <= 2:
        return -1
    if len (candidata)==3:
        return puntos + 1
    else:
        if len(candidata)==4:
            return puntos + 2
        else:
            if len (candidata)>=5 and len(candidata)!= 7:
                puntos= puntos + len (candidata)
            else:
                puntos=puntos + 10
    return puntos


#busca en el diccionario paralabras correctas y devuelve una lista de estas
def dameAlgunasCorrectas(letraPrincipal, letrasEnPantalla, diccionario):
    posiblesSoluciones = []
    algunas = letraPrincipal
    for i in range (len(letrasEnPantalla)):
        if i!=letraPrincipal and i<3:
            algunas+=letrasEnPantalla[i]

    for pos in range (len(diccionario)):
        if algunas in diccionario[pos]:
                if len(posiblesSoluciones)<MINIMO:
                    posiblesSoluciones.append(diccionario[pos])

    return posiblesSoluciones
