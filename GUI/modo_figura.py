from tkinter import ttk

class ModoFigura:
    def __init__(self, app):
        self.app = app
        self.frames_figuras = {}
    
    def mostrar_elementos(self):
        self.app.ocultar_todos_los_elementos()
        
        # Configurar el evento de clic específico para este modo
        print("[DEBUG] Configurando binding para clics en el canvas (ModoFigura)")
        self.app.canvas.unbind("<Button-1>")  # Eliminar cualquier binding previo
        self.app.canvas.bind("<Button-1>", self.manejar_clic)
        
        # Crear interfaz de figuras
        figuras = {
            "Rectángulo": "rectangulo",
            "Rombo": "rombo",
            "Óvalo": "ovalo"
        }
        
        for nombre, tipo in figuras.items():
            frame = ttk.Frame(self.app.scrollable_frame, padding=(5, 2))
            frame.pack(fill="x", pady=(10, 0), padx=5)
            self.frames_figuras[tipo] = frame
            
            label = ttk.Label(frame, text=nombre, font=self.app.fuente_titulo)
            label.pack(anchor="w")
            
            btn = ttk.Button(
                frame, 
                text=nombre, 
                width=20,
                command=lambda t=tipo: self.seleccionar_figura(t)
            )
            btn.pack(fill="x", pady=2)
    
    def seleccionar_figura(self, tipo):
        print(f"[DEBUG] Figura seleccionada: {tipo}")
        self.app.elemento_seleccionado = tipo
        self.app.tipo_seleccionado = "figura"
    
    def manejar_clic(self, event):
        print(f"\n[DEBUG] Click en ModoFigura - Coordenadas: x={event.x}, y={event.y}")
        
        if not self.app.elemento_seleccionado:
            print("[DEBUG] No hay figura seleccionada, ignorando clic")
            return
        
        x, y = event.x, event.y
        tamaño = 60  # Tamaño predeterminado de las figuras
        
        if self.app.elemento_seleccionado == "rectangulo":
            figura_id = self.app.canvas.create_rectangle(
                x - tamaño/2, y - tamaño/4,
                x + tamaño/2, y + tamaño/4,
                fill="white", outline="black", width=2,
                tags="figura"
            )
        elif self.app.elemento_seleccionado == "rombo":
            puntos = [
                x, y - tamaño/3,
                x + tamaño/2, y,
                x, y + tamaño/3,
                x - tamaño/2, y
            ]
            figura_id = self.app.canvas.create_polygon(
                puntos,
                fill="white", outline="black", width=2,
                tags="figura"
            )
        elif self.app.elemento_seleccionado == "ovalo":
            figura_id = self.app.canvas.create_oval(
                x - tamaño/2, y - tamaño/4,
                x + tamaño/2, y + tamaño/4,
                fill="white", outline="black", width=2,
                tags="figura"
            )
        elif self.app.elemento_seleccionado == "terminal":
            figura_id = self.app.canvas.create_rectangle(
                x - tamaño/2, y - tamaño/4,
                x + tamaño/2, y + tamaño/4,
                fill="white", outline="black", width=2,
                tags="figura"
            )
            # Agregar texto "INICIO" o "FIN" si es terminal
            texto = "INICIO" if len(self.app.figuras) == 0 else "FIN"
            
            # Calcular tamaño de fuente basado en el tamaño de la figura
            tamaño_fuente = max(8, min(14, int(tamaño / len(texto))))
            
            texto_id = self.app.canvas.create_text(
                x, y,
                text=texto,
                font=(self.app.fuente_normal.actual()['family'], tamaño_fuente),
                fill="black",
                tags="texto"
            )
            self.app.textos.append({
                "id": texto_id,
                "texto": texto,
                "tipo": "Terminal",
                "x": x,
                "y": y,
                "figura": figura_id,
                "fuente": tamaño_fuente
            })
        
        # Registrar la figura en la estructura de datos
        self.app.figuras.append({
            "id": figura_id,
            "tipo": self.app.elemento_seleccionado,
            "x": x,
            "y": y,
            "textos": []
        })
        
        if self.app.elemento_seleccionado == "terminal":
            self.app.figuras[-1]["textos"].append({
                "id": texto_id,
                "texto": texto,
                "tipo": "Terminal",
                "fuente": tamaño_fuente
            })
        
        print(f"[DEBUG] Figura creada con ID: {figura_id}")