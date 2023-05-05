import Pyro4
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from tkinter import *

class Interfaz:
    def __init__(self, uri):
        self.juego = Pyro4.Proxy(uri)

        self.root = tk.Tk()
        self.root.title("SECRET WORD!")
        self.root.iconbitmap('secreto.ico')
        self.root.geometry('420x340')

        # Hacer que la ventana no sea redimensionable
        self.root.resizable(False, False)

        self.P = tk.Label(self.root, text="Pista principal:",
                          font=("Courier New", 12))

        self.scrollbar = tk.Scrollbar(self.root, width=13)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, yscrollcommand=self.scrollbar.set, height=8, width=35)
        self.text_area.pack(pady=12)

        # Configurar el Scrollbar para que funcione con el ScrolledText
        self.scrollbar.config(command=self.text_area.yview)

         # Obtener opciones y tema del servidor
        self.temav = self.juego.obtener_prin()
        #self.word = self.juego.obtener_palabra()
        #self.pista1 = self.juego.obtener_pistas()

        # Establecer el contenido del ScrolledText
        self.text_area.insert(tk.INSERT, self.temav)

        self.idk = tk.Label(self.root, text="¡Trata de adivinar la secret word!")
        self.idk.pack(pady=10)

        self.entry = Entry(self.root, width=30)
        self.entry.pack()
        self.entry.focus_set()
        self.button = Button(self.root, text="Adivinar", command=self.adivinar)
        self.button.pack(pady=10)
        
        self.labelR = tk.Label(self.root, text="Puedes reiniciar el juego en cualquier momento. Da click al siguiente botón")
        self.labelR.pack(pady=10)
        self.buttonR = Button(self.root, text="Volver a empezar", command=self.reiniciar)
        self.buttonR.pack(pady=10)

        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    
            
    def adivinar(self):
        palabra = self.entry.get() #Toma el valor del textfield 
        resultado = self.juego.adivinar(palabra) #Devuelve el método remoto "adivinar" del objeto juego
        if resultado.startswith("¡Felicidades"):
            messagebox.showinfo("Ganaste!", resultado)
            self.root.destroy()
        elif resultado.startswith("Lo siento"):
            # Si pierde, mostrar un cuadro de mensaje preguntando si desea reiniciar el juego.
            respuesta = messagebox.askyesno("Perdiste", resultado + " ¿Quieres volver a jugar?")
            self.entry.delete(0, END)
            if respuesta:
                # Si la respuesta es "sí", llamar al método "reiniciar_juego" del objeto "juego".
                self.juego.reiniciar()
                self.entry.delete(0, END)
            else:
                self.root.destroy()
        else:
            messagebox.showwarning("Resultado", resultado)
            self.entry.delete(0, END)
            
    def reiniciar(self):
        self.juego.reiniciar()
        messagebox.showinfo("Juego reiniciado!", "Has reiniciado el juego y obtenido tus intentos nuevamente")
        self.entry.delete(0, END)
            
    def iniciar(self):
        self.root.mainloop()



server_ip = simpledialog.askstring(
    "Dirección IP del servidor", "Ingrese la dirección IP del servidor:")
if server_ip is None:
    # Si el usuario cancela el diálogo, salir del programa
    exit()

server_port = simpledialog.askstring(
    "Dirección IP del servidor", "Ingrese el puerto del servidor:")
if server_port is None:
    # Si el usuario cancela el diálogo, salir del programa
    exit()
uri = f"PYRO:juego@{server_ip}:{server_port}"

messagebox.showinfo("URI del SERVIDOR", uri)
print("URI del SERVIDOR", uri)

messagebox.showinfo("Regla", "Introduce sólo minúsculas", icon="warning")

interfaz = Interfaz(uri)
interfaz.iniciar()

