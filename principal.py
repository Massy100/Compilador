import tkinter as tk
from tkinter import ttk, font

class DiagramaFlujoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Diagramas de Flujo")
        self.root.geometry("1200x700")
        
        # Variables de estado
        self.elemento_seleccionado = None
        self.tipo_seleccionado = None
        self.figuras = []
        self.conexiones = []
        self.textos = []
        self.modo_conexion = False
        self.origen_conexion = None
        
        # Fuentes
        self.fuente_normal = font.Font(family="Arial", size=10)
        self.fuente_titulo = font.Font(family="Arial", size=10, weight="bold")
        
        # Crear interfaz
        self.crear_panel_con_scroll()
        self.crear_area_dibujo()
        self.crear_controles_inferiores()
        
        # Configurar eventos
        self.canvas.bind("<Button-1>", self.colocar_elemento)
        self.canvas.bind("<B1-Motion>", self.arrastrar_elemento)
        self.canvas.bind("<ButtonRelease-1>", self.soltar_elemento)
        
        # Cargar elementos en el panel
        self.cargar_elementos_panel()
    
    def crear_panel_con_scroll(self):
        # Frame principal del panel
        panel_frame = ttk.Frame(self.root, width=250)
        panel_frame.pack(side="left", fill="y")
        panel_frame.pack_propagate(False)
        
        # Canvas y scrollbar
        self.panel_canvas = tk.Canvas(panel_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel_frame, orient="vertical", command=self.panel_canvas.yview)
        
        # Frame scrollable
        self.scrollable_frame = ttk.Frame(self.panel_canvas)
        
        # Configurar el sistema de scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.panel_canvas.configure(
                scrollregion=self.panel_canvas.bbox("all")
            )
        )
        
        # Crear ventana en el canvas
        self.panel_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configurar scrollbar
        self.panel_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar elementos
        self.panel_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con rueda del mouse
        self.panel_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.panel_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def cargar_elementos_panel(self):
        # Categorías y elementos
        categorias = {
            "Palabra Clave": ["if", "else", "while", "switch", "case", "return", 
                            "print", "break", "for", "int", "float", "void", 
                            "double", "char", "const"],
            "Letra": [chr(i) for i in range(ord('A'), ord('Z')+1)],
            "Número": [str(i) for i in range(10)],
            "Operador": ["+", "-", "*", "/", "=", "<", ">", "!", "_"],
            "Delimitadores": ["(", ")", ",", ";", "{", "}"],
            "Terminal": ["INICIO", "FIN"],
            "Figuras": ["Óvalo", "Rectángulo", "Rombo"],
            "Conexiones": ["Flecha"]
        }
        
        for categoria, elementos in categorias.items():
            self.crear_seccion_categoria(categoria, elementos)
    
    def crear_seccion_categoria(self, titulo, elementos):
        frame = ttk.Frame(self.scrollable_frame, padding=(5, 2))
        frame.pack(fill="x", pady=(10, 0), padx=5)
        
        label = ttk.Label(frame, text=titulo, font=self.fuente_titulo)
        label.pack(anchor="w")
        
        for elemento in elementos:
            btn = ttk.Button(
                frame, 
                text=elemento, 
                width=20,
                command=lambda e=elemento, t=titulo: self.seleccionar_elemento(e, t)
            )
            btn.pack(fill="x", pady=2)
    
    def crear_area_dibujo(self):
        # Frame principal del área de dibujo
        dibujo_frame = ttk.Frame(self.root)
        dibujo_frame.pack(side="right", expand=True, fill="both", padx=5, pady=5)
        
        # Canvas para dibujar (solo uno)
        self.canvas = tk.Canvas(dibujo_frame, bg="white", bd=2, relief="ridge")
        self.canvas.pack(expand=True, fill="both")
    
    def crear_controles_inferiores(self):
        # Frame para controles
        controles_frame = ttk.Frame(self.root)
        controles_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        
        # Botones de control
        ttk.Button(
            controles_frame, 
            text="Mostrar en Consola", 
            command=self.mostrar_en_consola
        ).pack(side="left", padx=5)
        
        ttk.Button(
            controles_frame,
            text="Limpiar Todo",
            command=self.limpiar_canvas
        ).pack(side="left", padx=5)
        
        ttk.Button(
            controles_frame,
            text="Modo Conexión",
            command=self.toggle_modo_conexion
        ).pack(side="right", padx=5)
    
    def seleccionar_elemento(self, elemento, categoria):
        self.elemento_seleccionado = elemento
        self.tipo_seleccionado = categoria
        print(f"Seleccionado: {elemento} ({categoria})")
    
    def colocar_elemento(self, event):
        if not self.elemento_seleccionado:
            return
            
        x, y = event.x, event.y
        
        if self.modo_conexion:
            self.manejar_conexion(x, y)
            return
            
        if self.tipo_seleccionado == "Figuras":
            self.crear_figura(x, y)
        elif self.tipo_seleccionado == "Conexiones":
            pass  # Se maneja en modo conexión
        else:
            self.crear_texto(x, y)
    
    def crear_figura(self, x, y):
        figura = None
        tamaño = 80
        
        # Crear figura con tag "figura" para identificarla
        if self.elemento_seleccionado == "Óvalo":
            figura = self.canvas.create_oval(
                x-tamaño/2, y-tamaño/2, x+tamaño/2, y+tamaño/2,
                fill="lightblue", outline="black", width=2,
                tags="figura"
            )
        elif self.elemento_seleccionado == "Rectángulo":
            figura = self.canvas.create_rectangle(
                x-tamaño/2, y-tamaño/2, x+tamaño/2, y+tamaño/2,
                fill="lightgreen", outline="black", width=2,
                tags="figura"
            )
        elif self.elemento_seleccionado == "Rombo":
            puntos = [
                x, y-tamaño/2,
                x+tamaño/2, y,
                x, y+tamaño/2,
                x-tamaño/2, y
            ]
            figura = self.canvas.create_polygon(
                puntos,
                fill="lightyellow", outline="black", width=2,
                tags="figura"
            )
        
        if figura:
            # Mover la figura al fondo para que no tape el texto
            self.canvas.tag_lower(figura)
            
            self.figuras.append({
                "id": figura,
                "tipo": self.elemento_seleccionado,
                "x": x,
                "y": y,
                "textos": []
            })
    
    def crear_texto(self, x, y):
        # Verificar si el clic fue dentro de una figura
        figuras_en_posicion = self.canvas.find_overlapping(x-1, y-1, x+1, y+1)
        figura_objetivo = None
        
        for item in figuras_en_posicion:
            if "figura" in self.canvas.gettags(item):
                figura_objetivo = item
                break
        
        if figura_objetivo:
            # Obtener coordenadas de la figura para centrar el texto
            x1, y1, x2, y2 = self.canvas.coords(figura_objetivo)
            centro_x = (x1 + x2) / 2
            centro_y = (y1 + y2) / 2
            
            texto = self.canvas.create_text(
                centro_x, centro_y,
                text=self.elemento_seleccionado,
                font=self.fuente_normal,
                fill="black",
                tags="texto"
            )
            
            # Asegurar que el texto esté sobre la figura
            self.canvas.tag_raise(texto)
            
            # Guardar texto y asociarlo a la figura
            self.textos.append({
                "id": texto,
                "texto": self.elemento_seleccionado,
                "tipo": self.tipo_seleccionado,
                "x": centro_x,
                "y": centro_y,
                "figura": figura_objetivo
            })
            
            # Actualizar la figura con este texto
            for figura in self.figuras:
                if figura["id"] == figura_objetivo:
                    figura["textos"].append({
                        "id": texto,
                        "texto": self.elemento_seleccionado,
                        "tipo": self.tipo_seleccionado
                    })
                    break
        else:
            # Crear texto suelto si no hay figura
            texto = self.canvas.create_text(
                x, y,
                text=self.elemento_seleccionado,
                font=self.fuente_normal,
                fill="black",
                tags="texto"
            )
            
            self.textos.append({
                "id": texto,
                "texto": self.elemento_seleccionado,
                "tipo": self.tipo_seleccionado,
                "x": x,
                "y": y,
                "figura": None
            })
    
    def arrastrar_elemento(self, event):
        # Implementar lógica de arrastre si es necesario
        pass
    
    def soltar_elemento(self, event):
        # Implementar lógica al soltar si es necesario
        pass
    
    def toggle_modo_conexion(self):
        self.modo_conexion = not self.modo_conexion
        print(f"Modo conexión: {'activado' if self.modo_conexion else 'desactivado'}")
    
    def manejar_conexion(self, x, y):
        items = self.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        figuras = [item for item in items if "figura" in self.canvas.gettags(item) or "texto" in self.canvas.gettags(item)]
        
        if figuras:
            if not self.origen_conexion:
                self.origen_conexion = figuras[0]
                # Solo cambiar color si es una figura
                if "figura" in self.canvas.gettags(figuras[0]):
                    self.canvas.itemconfig(self.origen_conexion, outline="red", width=3)
            else:
                destino = figuras[0]
                if destino != self.origen_conexion:  # Evitar conectar consigo mismo
                    self.crear_flecha(self.origen_conexion, destino)
                    # Restaurar apariencia original si es una figura
                    if "figura" in self.canvas.gettags(self.origen_conexion):
                        self.canvas.itemconfig(self.origen_conexion, outline="black", width=2)
                self.origen_conexion = None

    def crear_flecha(self, origen, destino):
        try:
            # Función para calcular el centro de cualquier figura
            def obtener_centro(item):
                coords = self.canvas.coords(item)
                tags = self.canvas.gettags(item)
                
                if "figura" in tags:
                    if len(coords) == 4:  # Rectángulo u óvalo
                        x1, y1, x2, y2 = coords
                        return (x1 + x2) / 2, (y1 + y2) / 2
                    else:  # Rombo (polygon con 8 coordenadas)
                        # Calcular centro del polígono
                        xs = coords[::2]  # Todas las coordenadas x
                        ys = coords[1::2]  # Todas las coordenadas y
                        return sum(xs)/len(xs), sum(ys)/len(ys)
                else:  # Texto u otros
                    return coords[0], coords[1]
            
            # Obtener centros
            centro_origen_x, centro_origen_y = obtener_centro(origen)
            centro_destino_x, centro_destino_y = obtener_centro(destino)
            
            # Crear la flecha
            flecha = self.canvas.create_line(
                centro_origen_x, centro_origen_y,
                centro_destino_x, centro_destino_y,
                arrow=tk.LAST, fill="black", width=2,
                tags="flecha"
            )
            
            self.conexiones.append({
                "id": flecha,
                "origen": origen,
                "destino": destino
            })
            
        except Exception as e:
            print(f"Error al crear flecha: {e}")
            # Mostrar información de depuración
            print(f"Origen coords: {self.canvas.coords(origen)}")
            print(f"Destino coords: {self.canvas.coords(destino)}")
            print(f"Origen tags: {self.canvas.gettags(origen)}")
            print(f"Destino tags: {self.canvas.gettags(destino)}")
        
    def mostrar_en_consola(self):
        print("\n=== Resumen del Diagrama ===")
        
        # Mostrar textos con su categoría y figura asociada
        print("\nTextos:")
        for texto in self.textos:
            figura_info = "Ninguna"
            if texto["figura"]:
                for figura in self.figuras:
                    if figura["id"] == texto["figura"]:
                        figura_info = f"{figura['tipo']} (ID: {figura['id']})"
                        break
            
            print(f"Texto: {texto['texto']}, Categoría: {texto['tipo']}, Figura: {figura_info}")
        
        # Mostrar figuras con sus textos
        print("\nFiguras:")
        for figura in self.figuras:
            textos_en_figura = ", ".join([t["texto"] for t in figura["textos"]])
            print(f"ID: {figura['id']}, Tipo: {figura['tipo']}, Textos: [{textos_en_figura}]")
        
        # Mostrar conexiones
        print("\nConexiones:")
        for conexion in self.conexiones:
            print(f"De figura {conexion['origen']} a figura {conexion['destino']}")
    
    def limpiar_canvas(self):
        self.canvas.delete("all")
        self.figuras = []
        self.conexiones = []
        self.textos = []
        self.origen_conexion = None
        self.modo_conexion = False

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagramaFlujoApp(root)
    root.mainloop()