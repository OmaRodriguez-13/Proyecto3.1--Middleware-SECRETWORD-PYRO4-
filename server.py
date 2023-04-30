import Pyro4
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import sys

@Pyro4.expose
class JuegoAdivinarPalabra:
    def __init__(self):
        self.palabra = ""
        self.pista1 = ""
        self.pistaPrin = ""
        self.pista2 = ""
        self.intentos_fallidos = 0

        self.usuarios = {}

    def reiniciar_juego(self):
        self.intentos_fallidos = 0

    def establecer_palabra(self, palabra):
        self.palabra = palabra.lower()

    def obtener_palabra(self):
        return self.palabra

    def establecer_pistas(self, pista1):
        self.pista1 = pista1
        self.pista2 = "La palabra empieza con la letra: " + str(self.palabra[0]) + " y tiene " + str(len(self.palabra)) + " letras."

    def obtener_pistas(self):
        if self.intentos_fallidos == 0:
            #return "Adivina la palabra."
            return self.pistaPrin
        elif self.intentos_fallidos == 1:
            return "¡Fallaste! Aquí tienes una pista:\n" + self.pista1
        elif self.intentos_fallidos == 2:
            return "¡Fallaste de nuevo! Aquí tienes otra pista:\n" + self.pista2
        else:
            return "Lo siento, has perdido. La palabra era " + self.palabra + "."
        
    #original
    '''
    def adivinar(self, palabra):
        if palabra.lower() == self.palabra:
            return "¡Felicidades, has ganado!"
        else:
            self.intentos_fallidos += 1
            if self.intentos_fallidos <= 2:
                return "No es la palabra. " + self.obtener_pistas()
            else:
                return self.obtener_pistas()
    '''

        #con este codigo nunca se "pierde"
    '''   
    def adivinar(self, palabra):
        if palabra.lower() == self.palabra:
            self.reiniciar_juego()
            return f"¡Felicidades, has ganado!"
        else:
            self.intentos_fallidos += 1
            if self.intentos_fallidos <= 2:
                return "No es la palabra. " + self.obtener_pistas()
            if self.intentos_fallidos == 3:
                self.reiniciar_juego()
                return self.obtener_pistas()
         '''   
    
    #Los intentos se almacenan para todos los clientes
    def adivinar(self, palabra):
        if self.intentos_fallidos >= 2:
            self.intentos_fallidos = 0
            return "Se han restablecido los intentos." + " Lo siento, has perdido. La palabra era " + self.palabra + "."
        elif palabra.lower() == self.palabra:
            return "¡Felicidades, has ganado!"
        else:
            self.intentos_fallidos += 1
            return "No es la palabra. " + self.obtener_pistas()

    def establecer_prin(cls, pistaPrin):
        cls.pistaPrin = pistaPrin

    def obtener_prin(cls):
        return cls.pistaPrin

    def agregar_usuario(self, usuario):
        self.usuarios[usuario] = False

    def obtener_usuarios(self):
        return self.usuarios

ip = Pyro4.socketutil.getInterfaceAddress("192.168.137.1")
daemon = Pyro4.Daemon(host=ip)

juego = JuegoAdivinarPalabra()
uri = daemon.register(juego, objectId='juego')

# Obtener la palabra del usuario
palabra = simpledialog.askstring("Adivinar la palabra", "Ingresa la palabra a adivinar:")
pistaPrin = simpledialog.askstring("Pista principal", "Ingresa la pista principal:")
pista1 =  simpledialog.askstring("Pista", "Ingresa una nueva pista:")

# Establecer la palabra y pista en el servidor
juego.establecer_palabra(palabra)
juego.establecer_prin(pistaPrin)
juego.establecer_pistas(pista1)

messagebox.showinfo("URI del SERVIDOR", f"Servidor listo. URI= {uri}")
print("Servidor listo. URI= ", uri)

daemon.requestLoop()

