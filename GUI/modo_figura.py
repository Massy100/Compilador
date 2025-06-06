from tkinter import ttk

class ModoFigura:
    def __init__(self, app):
        self.app = app
        self.frames_figuras = {}
    
    def mostrar_elementos(self):
        self.app.ocultar_todos_los_elementos()
        
        print("[DEBUG] Configurando binding para clics en el canvas (ModoFigura)")
        self.app.canvas.unbind("<Button-1>")
        self.app.canvas.bind("<Button-1>", self.manejar_clic)
        
        figuras = {
            "Proceso": "rectangulo",
            "Decisión": "rombo",
            "Inicio / Fin": "ovalo", 
            "Entrada/Salida": "entrada_salida",
            "Llamada a Función": "llamada_funcion",
            "Bucle While": "while",
            "Bucle For": "for"
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
        tamaño = 60
        figura_id = None
        
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
        elif self.app.elemento_seleccionado == "proceso":
            figura_id = self.app.canvas.create_rectangle(
                x - tamaño/2, y - tamaño/4,
                x + tamaño/2, y + tamaño/4,
                fill="lightgray", outline="black", width=2,
                tags="figura"
            )
        elif self.app.elemento_seleccionado == "entrada_salida":
            puntos = [
                x - tamaño / 2, y - tamaño / 4,
                x + tamaño / 2, y - tamaño / 4,
                x + tamaño / 3, y + tamaño / 4,
                x - tamaño / 2 - tamaño / 6, y + tamaño / 4
            ]
            figura_id = self.app.canvas.create_polygon(
                puntos,
                fill="lightblue", outline="black", width=2,
                tags="figura"
            )
        elif self.app.elemento_seleccionado == "llamada_funcion":
            figura_id = self.app.canvas.create_rectangle(
                x - tamaño / 2, y - tamaño / 4,
                x + tamaño / 2, y + tamaño / 4,
                fill="lightyellow", outline="black", width=2,
                tags="figura"
            )
        elif self.app.elemento_seleccionado == "while":
            figura_id = self.app.canvas.create_rectangle(
                x - tamaño/2, y - tamaño/4,
                x + tamaño/2, y + tamaño/4,
                fill="lightgreen", outline="black", width=2,
                tags="figura"
            )
        elif self.app.elemento_seleccionado == "for":
            figura_id = self.app.canvas.create_rectangle(
                x - tamaño/2, y - tamaño/4,
                x + tamaño/2, y + tamaño/4,
                fill="lightblue", outline="black", width=2,
                tags="figura"
            )
            # Líneas internas
            self.app.canvas.create_line(
                x - tamaño / 2 + 10, y - tamaño / 4,
                x - tamaño / 2 + 10, y + tamaño / 4,
                fill="black", width=1, tags="figura"
            )
            self.app.canvas.create_line(
                x + tamaño / 2 - 10, y - tamaño / 4,
                x + tamaño / 2 - 10, y + tamaño / 4,
                fill="black", width=1, tags="figura"
            )
        elif self.app.elemento_seleccionado == "terminal":
            figura_id = self.app.canvas.create_rectangle(
                x - tamaño / 2, y - tamaño / 4,
                x + tamaño / 2, y + tamaño / 4,
                fill="white", outline="black", width=2,
                tags="figura"
            )
            texto = "INICIO" if len(self.app.figuras) == 0 else "FIN"
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
        if figura_id:
            figura = {
                "id": figura_id,
                "tipo": self.app.elemento_seleccionado,
                "x": x,
                "y": y,
                "textos": []
            }
            self.app.figuras.append(figura)

            if self.app.elemento_seleccionado == "terminal":
                figura["textos"].append({
                    "id": texto_id,
                    "texto": texto,
                    "tipo": "Terminal",
                    "fuente": tamaño_fuente
                })
            print(f"[DEBUG] Figura creada con ID: {figura_id}")
