import Pyro4
from Pyro4 import socketutil
import tkinter as tk
from tkinter import messagebox, simpledialog

@Pyro4.expose
class JuegoAdivinarPalabra:
    def __init__(self):
        self.palabra = ""
        self.pista1 = ""
        self.pistaPrin = ""
        self.pista2 = ""
        self.intentos_fallidos = 0

    def establecer_palabra(self, palabra):
        self.palabra = palabra.lower()

    def obtener_palabra(self):
        return self.palabra

    def establecer_pistas(self, pista1):
        self.pista1 = pista1
        self.pista2 = "La palabra empieza con la letra: " + str(self.palabra[0]) + " y tiene " + str(len(self.palabra)) + " letras."

    #Método para devolverle "pistas" al cliente por cada vez que falle (3 intentos)
    def obtener_pistas(self):
        if self.intentos_fallidos == 0:
            #return "Adivina la palabra."
            return self.pistaPrin
        elif self.intentos_fallidos == 1:
            return "¡Fallaste! Aquí tienes una pista:\n" + self.pista1
        elif self.intentos_fallidos == 2:
            return "¡Fallaste de nuevo! Aquí tienes otra pista:\n" + self.pista2
        else:
            return "Lo siento, has perdido. La palabra era: " + self.palabra + "."
        
    #Método que compara la entrada del cliente con la secretword
    def adivinar(self, palabra):
        if palabra.lower() == self.palabra: #Utiliza el método lower() para convertir la palabra en minúsculas
            #independientemente de cómo se haya ingresado
            return "¡Felicidades, has ganado!"
        else:
            self.intentos_fallidos += 1
            if self.intentos_fallidos <= 2:
                return "No es la palabra. " + self.obtener_pistas()
            else:
                return self.obtener_pistas()
            
    def reiniciar(self):
        self.intentos_fallidos = 0
   
    def establecer_prin(cls, pistaPrin):
        cls.pistaPrin = pistaPrin

    def obtener_prin(cls):
        return cls.pistaPrin
    
ip = socketutil.getIpAddress('su_ip') #cambiar a la ip del equipo que funcionará como servidor
daemon = Pyro4.Daemon(host=ip)

juego = JuegoAdivinarPalabra()
uri = daemon.register(juego, objectId='juego')

# Obtener la palabra del usuario
palabra = simpledialog.askstring("Adivinar la palabra", "Ingresa la palabra a adivinar:")
pistaPrin = simpledialog.askstring("Pista principal", "Ingresa la pista principal:")
pista1 =  simpledialog.askstring("Pista", "Ingresa una nueva pista:")

# Establecer la palabra y pista en el servidor
# Paso de parametros al cliente
juego.establecer_palabra(palabra)
juego.establecer_prin(pistaPrin)
juego.establecer_pistas(pista1)

messagebox.showinfo("URI del SERVIDOR", f"Servidor listo. URI= {uri}")
print("Servidor listo. URI= ", uri)

daemon.requestLoop()

