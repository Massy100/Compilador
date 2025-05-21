from tkinter import ttk, messagebox
import tkinter as tk

class ModoConexion:
    def __init__(self, app):
        self.app = app
        self.frame_conexiones = None
        self.origen_conexion = None  # Mover esta variable del app a la clase
    
    def mostrar_elementos(self):
        self.app.ocultar_todos_los_elementos()
        
        # Configurar el evento de clic específico para este modo
        print("[DEBUG] Configurando binding para clics en el canvas (ModoConexion)")
        self.app.canvas.unbind("<Button-1>")  # Eliminar cualquier binding previo
        self.app.canvas.bind("<Button-1>", self.manejar_clic_conexion)
        
        # Crear interfaz de conexiones
        self.frame_conexiones = ttk.Frame(self.app.scrollable_frame, padding=(5, 2))
        self.frame_conexiones.pack(fill="x", pady=(10, 0), padx=5)
        
        label = ttk.Label(self.frame_conexiones, text="Conexiones", font=self.app.fuente_titulo)
        label.pack(anchor="w")
        
        btn = ttk.Button(
            self.frame_conexiones, 
            text="Flecha", 
            width=20,
            command=self.seleccionar_conexion
        )
        btn.pack(fill="x", pady=2)
    
    def seleccionar_conexion(self):
        print("[DEBUG] Conexión seleccionada")
        self.app.elemento_seleccionado = "Flecha"
        self.app.tipo_seleccionado = "Conexiones"
        self.origen_conexion = None  # Resetear origen al seleccionar nueva conexión
    
    def manejar_clic_conexion(self, event):
        print(f"\n[DEBUG] Click en ModoConexion - Coordenadas: x={event.x}, y={event.y}")
        
        x, y = event.x, event.y
        items = self.app.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        
        # Filtrar solo figuras (no textos)
        figuras = [item for item in items if "figura" in self.app.canvas.gettags(item)]
        
        if not figuras:
            print("[DEBUG] No se encontraron figuras en la posición del clic")
            return
        
        figura = figuras[0]  # Tomar la figura superior
        
        if not self.origen_conexion:
            print(f"[DEBUG] Estableciendo figura origen: {figura}")
            self.origen_conexion = figura
            self.app.resaltar_figura(figura)  # Resaltar figura origen
        else:
            if figura == self.origen_conexion:
                print("[DEBUG] Misma figura seleccionada, ignorando")
                return
                
            print(f"[DEBUG] Estableciendo figura destino: {figura}")
            self.crear_flecha(self.origen_conexion, figura)
            
            # Restaurar aspecto original de la figura origen
            self.app.restaurar_bordes_figuras()
            self.origen_conexion = None
    
    def crear_flecha(self, origen, destino):
        print(f"[DEBUG] Creando flecha de {origen} a {destino}")
        
        try:
            coords_origen = self.app.canvas.coords(origen)
            coords_destino = self.app.canvas.coords(destino)

            # Centro y límites de origen
            if len(coords_origen) == 4:
                x1, y1, x2, y2 = coords_origen
                centro_origen_x = (x1 + x2) / 2
                centro_origen_y = (y1 + y2) / 2
            else:
                xs = coords_origen[::2]
                ys = coords_origen[1::2]
                x1, x2 = min(xs), max(xs)
                y1, y2 = min(ys), max(ys)
                centro_origen_x = sum(xs) / len(xs)
                centro_origen_y = sum(ys) / len(ys)

            # Centro y límites de destino
            if len(coords_destino) == 4:
                x1_d, y1_d, x2_d, y2_d = coords_destino
                centro_destino_x = (x1_d + x2_d) / 2
                centro_destino_y = (y1_d + y2_d) / 2
            else:
                xs_d = coords_destino[::2]
                ys_d = coords_destino[1::2]
                x1_d, x2_d = min(xs_d), max(xs_d)
                y1_d, y2_d = min(ys_d), max(ys_d)
                centro_destino_x = sum(xs_d) / len(xs_d)
                centro_destino_y = sum(ys_d) / len(ys_d)

            
            # Calcular punto de inicio en el borde de la figura origen
            start_x, start_y = self.calcular_punto_borde(
                centro_origen_x, centro_origen_y,
                centro_destino_x, centro_destino_y,
                x1, y1, x2, y2
            )
            
            # Calcular punto final en el borde de la figura destino
            end_x, end_y = self.calcular_punto_borde(
                centro_destino_x, centro_destino_y,
                centro_origen_x, centro_origen_y,
                x1_d, y1_d, x2_d, y2_d
            )
            
            # Crear la flecha
            flecha = self.app.canvas.create_line(
                start_x, start_y,
                end_x, end_y,
                arrow=tk.LAST, 
                fill="black", 
                width=2,
                tags=("flecha", f"origen_{origen}", f"destino_{destino}")
            )
            
            # Registrar la conexión
            self.app.conexiones.append({
                "id": flecha,
                "origen": origen,
                "destino": destino,
                "puntos": [(start_x, start_y), (end_x, end_y)]
            })
            
            print(f"[DEBUG] Flecha creada con ID: {flecha}")
            
        except Exception as e:
            print(f"[ERROR] Error al crear flecha: {e}")
            messagebox.showerror("Error", f"No se pudo crear la conexión: {str(e)}")
    
    def calcular_punto_borde(self, centro_x, centro_y, objetivo_x, objetivo_y, x1, y1, x2, y2):
        """
        Calcula el punto de intersección entre el borde de la figura y la línea
        que va desde el centro hasta el objetivo
        """
        # Vector dirección desde el centro al objetivo
        dx = objetivo_x - centro_x
        dy = objetivo_y - centro_y
        
        # Calcular ángulo
        if dx == 0:  # Evitar división por cero
            if dy > 0:
                return centro_x, y2
            else:
                return centro_x, y1
        
        pendiente = dy / dx
        
        # Calcular intersección con los bordes
        # Bordes izquierdo/derecho
        if dx > 0:
            x_inter = x2
        else:
            x_inter = x1
        
        y_inter = centro_y + pendiente * (x_inter - centro_x)
        
        # Verificar si la intersección está dentro de los límites verticales
        if y1 <= y_inter <= y2:
            return x_inter, y_inter
        
        # Si no, usar bordes superior/inferior
        if dy > 0:
            y_inter = y2
        else:
            y_inter = y1
        
        x_inter = centro_x + (y_inter - centro_y) / pendiente
        
        return x_inter, y_inter
    
    def limpiar_seleccion(self):
        """Limpia la selección actual de conexión"""
        if self.origen_conexion:
            self.app.restaurar_bordes_figuras()
            self.origen_conexion = None