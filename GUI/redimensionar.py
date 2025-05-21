import tkinter as tk

class TextoEnRectangulo:
    def __init__(self, root):
        self.root = root
        self.root.title("Texto en Rectángulo")
        
        # Canvas donde dibujaremos el rectángulo y texto
        self.canvas = tk.Canvas(root, width=400, height=200, bg='white')
        self.canvas.pack(pady=20)
        
        # Texto inicial (cadena vacía)
        self.texto = ""
        
        # Coordenadas iniciales del rectángulo
        self.x1, self.y1 = 50, 50
        self.x2, self.y2 = 150, 100  # Dimensiones iniciales
        
        # Dibujar el rectángulo inicial
        self.rectangulo = self.canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2, 
            outline='black', fill='lightblue'
        )
        
        # Texto dentro del rectángulo
        self.texto_obj = self.canvas.create_text(
            self.x1 + 10, self.y1 + 10, 
            text=self.texto, 
            anchor='nw', 
            font=('Arial', 12)
        )
        
        # Botones para agregar palabras
        tk.Button(root, text="Agregar 'hola'", command=lambda: self.agregar_palabra("hola")).pack(side='left', padx=5)
        tk.Button(root, text="Agregar 'mundo'", command=lambda: self.agregar_palabra("mundo")).pack(side='left', padx=5)
        tk.Button(root, text="Agregar 'si'", command=lambda: self.agregar_palabra("si")).pack(side='left', padx=5)
        tk.Button(root, text="Limpiar", command=self.limpiar_texto).pack(side='left', padx=5)
    
    def agregar_palabra(self, palabra):
        # Agregar la palabra al texto existente (con espacio si ya hay texto)
        if self.texto:
            self.texto += " " + palabra
        else:
            self.texto = palabra
        
        # Actualizar el texto en el canvas
        self.canvas.itemconfig(self.texto_obj, text=self.texto)
        
        # Calcular el nuevo tamaño del texto
        ancho_texto = self.canvas.bbox(self.texto_obj)[2] - self.canvas.bbox(self.texto_obj)[0]
        alto_texto = self.canvas.bbox(self.texto_obj)[3] - self.canvas.bbox(self.texto_obj)[1]
        
        # Redimensionar el rectángulo (añadiendo márgenes)
        margen = 20
        nuevo_ancho = ancho_texto + margen
        nuevo_alto = alto_texto + margen
        
        # Actualizar coordenadas del rectángulo (manteniendo esquina superior izquierda fija)
        self.x2 = self.x1 + nuevo_ancho
        self.y2 = self.y1 + nuevo_alto
        
        self.canvas.coords(self.rectangulo, self.x1, self.y1, self.x2, self.y2)
        
        # Reubicar el texto para que quede centrado (opcional)
        self.canvas.coords(self.texto_obj, self.x1 + margen/2, self.y1 + margen/2)
    
    def limpiar_texto(self):
        self.texto = ""
        self.canvas.itemconfig(self.texto_obj, text=self.texto)
        # Restaurar tamaño original del rectángulo
        self.x2 = self.x1 + 100
        self.y2 = self.y1 + 50
        self.canvas.coords(self.rectangulo, self.x1, self.y1, self.x2, self.y2)
        self.canvas.coords(self.texto_obj, self.x1 + 10, self.y1 + 10)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextoEnRectangulo(root)
    root.mainloop()