import tkinter as tk
from tkinter import font

class TextoArrastrableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Figuras con Texto Arrastrable")
        self.root.geometry("800x600")
        
        # Lista para almacenar los elementos y sus posiciones
        self.elementos = []
        
        # Canvas para dibujar
        self.canvas = tk.Canvas(root, bg="white", bd=2, relief="ridge")
        self.canvas.pack(expand=True, fill="both")
        
        # Fuente para el texto
        self.fuente = font.Font(family="Arial", size=12)
        
        # Crear figura base (rectángulo)
        self.figura_base = self.canvas.create_rectangle(
            200, 150, 600, 450,
            fill="lightblue", outline="black", width=2
        )
        
        # Botones para agregar texto
        self.crear_controles()
        
        # Eventos para arrastrar
        self.canvas.bind("<ButtonPress-1>", self.inicio_arrastre)
        self.canvas.bind("<B1-Motion>", self.arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self.fin_arrastre)
        
        # Elemento actualmente arrastrado
        self.elemento_arrastrando = None
    
    def crear_controles(self):
        frame_controles = tk.Frame(self.root)
        frame_controles.pack(fill="x", padx=5, pady=5)
        
        # Entrada para texto personalizado
        tk.Label(frame_controles, text="Texto:").pack(side="left")
        self.entrada_texto = tk.Entry(frame_controles, width=15)
        self.entrada_texto.pack(side="left", padx=5)
        
        # Botones para agregar diferentes tipos de texto
        tk.Button(frame_controles, text="Agregar Letra", command=lambda: self.agregar_texto("A")).pack(side="left", padx=5)
        tk.Button(frame_controles, text="Agregar Número", command=lambda: self.agregar_texto("1")).pack(side="left", padx=5)
        tk.Button(frame_controles, text="Agregar Personalizado", command=self.agregar_texto_personalizado).pack(side="left", padx=5)
        tk.Button(frame_controles, text="Mostrar en Consola", command=self.mostrar_en_consola).pack(side="right", padx=5)
    
    def agregar_texto(self, texto):
        # Crear texto en posición inicial
        texto_id = self.canvas.create_text(
            50, 50,
            text=texto,
            font=self.fuente,
            fill="black",
            tags="texto_arrastrable"
        )
        
        # Guardar en la lista de elementos
        self.elementos.append({
            "id": texto_id,
            "texto": texto,
            "x": 50,
            "y": 50,
            "en_figura": False
        })
    
    def agregar_texto_personalizado(self):
        texto = self.entrada_texto.get()
        if texto:
            self.agregar_texto(texto)
            self.entrada_texto.delete(0, tk.END)
    
    def inicio_arrastre(self, event):
        # Buscar si se hizo clic en un texto arrastrable
        items = self.canvas.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5)
        for item in items:
            if "texto_arrastrable" in self.canvas.gettags(item):
                self.elemento_arrastrando = item
                self.posicion_inicial = (event.x, event.y)
                break
    
    def arrastrar(self, event):
        if self.elemento_arrastrando:
            # Calcular desplazamiento
            dx = event.x - self.posicion_inicial[0]
            dy = event.y - self.posicion_inicial[1]
            
            # Mover el texto
            self.canvas.move(self.elemento_arrastrando, dx, dy)
            
            # Actualizar posición inicial para el próximo movimiento
            self.posicion_inicial = (event.x, event.y)
            
            # Actualizar posición en la lista de elementos
            for elemento in self.elementos:
                if elemento["id"] == self.elemento_arrastrando:
                    elemento["x"] += dx
                    elemento["y"] += dy
                    
                    # Verificar si está dentro de la figura base
                    x1, y1, x2, y2 = self.canvas.coords(self.figura_base)
                    if (x1 < elemento["x"] < x2 and y1 < elemento["y"] < y2):
                        elemento["en_figura"] = True
                    else:
                        elemento["en_figura"] = False
                    break
    
    def fin_arrastre(self, event):
        self.elemento_arrastrando = None
    
    def mostrar_en_consola(self):
        print("\nContenido dentro de la figura:")
        for elemento in self.elementos:
            if elemento["en_figura"]:
                print(f"Texto: {elemento['texto']}, Posición: ({elemento['x']}, {elemento['y']})")
        
        print("\nTodos los elementos:")
        for elemento in self.elementos:
            estado = "Dentro" if elemento["en_figura"] else "Fuera"
            print(f"Texto: {elemento['texto']}, Posición: ({elemento['x']}, {elemento['y']}), Estado: {estado}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextoArrastrableApp(root)
    root.mainloop()