import tkinter as tk
from tkinter import ttk, font, messagebox
from modo_texto import ModoTexto
from modo_figura import ModoFigura
from modo_conexion import ModoConexion
import os
import sys

ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ruta_base)

import analizador 

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
        self.origen_conexion = None
        self.modo_actual = None
        
        # Instancias de los modos
        self.modo_texto = ModoTexto(self)
        self.modo_figura = ModoFigura(self)
        self.modo_conexion = ModoConexion(self)
        
        # Fuentes
        self.fuente_normal = font.Font(family="Arial", size=10)
        self.fuente_titulo = font.Font(family="Arial", size=10, weight="bold")
        
        # Crear interfaz
        self.crear_barra_menu()
        self.crear_panel_con_scroll()
        self.crear_area_dibujo()
        self.crear_controles_inferiores()
        
        # Configurar eventos
        self.canvas.bind("<Button-1>", self.manejar_clic)
        self.canvas.bind("<Button-3>", self.borrar_elemento)
        self.canvas.bind("<B1-Motion>", self.arrastrar_elemento)
        self.canvas.bind("<ButtonRelease-1>", self.soltar_elemento)
        
        # Inicializar modos
        self.ocultar_todos_los_elementos()
    
    def crear_barra_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Modos
        menu_modos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modos", menu=menu_modos)
        
        menu_modos.add_command(
            label="Modo Figura", 
            command=self.activar_modo_figura
        )
        menu_modos.add_command(
            label="Modo Conexión", 
            command=self.activar_modo_conexion
        )
        menu_modos.add_command(
            label="Modo Texto", 
            command=self.activar_modo_texto
        )
        menu_modos.add_separator()
        menu_modos.add_command(
            label="Salir de Modo", 
            command=self.salir_modo
        )
    
    def activar_modo_figura(self):
        self.modo_actual = "figura"
        self.modo_figura.mostrar_elementos()
    
    def activar_modo_conexion(self):
        self.modo_actual = "conexion"
        self.modo_conexion.mostrar_elementos()
    
    def activar_modo_texto(self):
        self.modo_actual = "texto"
        self.modo_texto.mostrar_elementos()
    
    def salir_modo(self):
        self.modo_actual = None
        self.ocultar_todos_los_elementos()
        self.elemento_seleccionado = None
        self.tipo_seleccionado = None
    
    def crear_panel_con_scroll(self):
        self.panel_frame = ttk.Frame(self.root, width=250)
        self.panel_frame.pack(side="left", fill="y")
        self.panel_frame.pack_propagate(False)
        
        self.panel_canvas = tk.Canvas(self.panel_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.panel_frame, orient="vertical", command=self.panel_canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.panel_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.panel_canvas.configure(
                scrollregion=self.panel_canvas.bbox("all")
            )
        )
        
        self.panel_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.panel_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.panel_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.panel_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.panel_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def ocultar_todos_los_elementos(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.pack_forget()
    
    def crear_area_dibujo(self):
        dibujo_frame = ttk.Frame(self.root)
        dibujo_frame.pack(side="right", expand=True, fill="both", padx=5, pady=5)
        
        self.canvas = tk.Canvas(dibujo_frame, bg="white", bd=2, relief="ridge")
        self.canvas.pack(expand=True, fill="both")
    
    def crear_controles_inferiores(self):
        style = ttk.Style()
        style.configure("Blanco.TFrame", background="white")

        controles_frame = ttk.Frame(
            self.root,
            padding=(5, 2),
            style="Blanco.TFrame"
        )
        controles_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-9, y=10)
        
        ttk.Button(
            controles_frame,
            text="Limpiar Todo",
            command=self.limpiar_canvas
        ).pack(side="left", padx=5)
        
        ttk.Button(
            controles_frame,
            text="Borrar Elemento",
            command=self.borrar_elemento_manual
        ).pack(side="left", padx=5)
        
        ttk.Button(
            controles_frame, 
            text="Generar salida txt", 
            command=self.mostrar_en_consola
        ).pack(side="left", padx=5)
        
        ttk.Button(
            controles_frame,
            text="Compilar",
            command=self.compilar_codigo
        ).pack(side="left", padx=5)
        
    def compilar_codigo(self):
        print("[DEBUG] compilar_codigo() se ejecutó")
        resultado = analizador.analizar_codigo()  # Usa la nueva función

        if resultado["success"]:
            messagebox.showinfo("Compilación Exitosa", resultado["message"])
        else:
            self.mostrar_ventana_errores(resultado["message"])

    def mostrar_ventana_errores(self, mensaje):
        ventana_errores = tk.Toplevel(self.root)
        ventana_errores.title("Errores de Compilación")
        
        # Frame principal con scroll
        frame_principal = ttk.Frame(ventana_errores)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Etiqueta de título
        ttk.Label(
            frame_principal, 
            text="Errores encontrados:", 
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))
        
        # Área de texto con scroll
        frame_texto = ttk.Frame(frame_principal)
        frame_texto.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        texto = tk.Text(
            frame_texto,
            wrap="word",
            height=15,
            width=80,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10)  # Fuente monoespaciada para mejor lectura
        )
        texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=texto.yview)
        
        # Insertar mensaje de error
        texto.insert("1.0", mensaje)
        texto.config(state="disabled")
        
        # Botón de cerrar
        ttk.Button(
            frame_principal,
            text="Cerrar",
            command=ventana_errores.destroy
        ).pack(pady=(10, 0))

    
    def manejar_clic(self, event):
        # Si estamos en modo texto y en modo edición, dejar que ModoTexto maneje el clic
        if self.modo_actual == "texto" and hasattr(self.modo_texto, 'modo_edicion') and self.modo_texto.modo_edicion:
            return
        
        # Si estamos en modo figura, dejar que ModoFigura maneje el clic
        elif self.modo_actual == "figura":
            self.modo_figura.manejar_clic(event)
            return
        
        # Si estamos en modo conexión, dejar que ModoConexion maneje el clic
        elif self.modo_actual == "conexion":
            self.modo_conexion.manejar_clic(event)
            return
        
        # Comportamiento por defecto (para cuando no hay modo activo)
        x, y = event.x, event.y
        items = self.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        
        if items:
            item = items[-1]
            tags = self.canvas.gettags(item)
            if "figura" in tags:
                self.resaltar_figura(item)

    def resaltar_figura(self, figura_id):
        """Resalta una figura cambiando su borde a rojo"""
        tags = self.canvas.gettags(figura_id)
        
        if "figura" in tags:
            # Guardar el color original del borde
            if not hasattr(self, 'colores_originales'):
                self.colores_originales = {}
            self.colores_originales[figura_id] = self.canvas.itemcget(figura_id, "outline")
            
            # Cambiar el borde a rojo y aumentar el grosor
            self.canvas.itemconfig(figura_id, outline="red", width=3)

    def restaurar_bordes_figuras(self):
        """Restaura todos los bordes de figuras a su estado original"""
        if hasattr(self, 'colores_originales'):
            for figura_id, color in self.colores_originales.items():
                if self.canvas.type(figura_id):  # Verificar que el item aún existe
                    self.canvas.itemconfig(figura_id, outline=color, width=2)
            self.colores_originales = {}
    
    def arrastrar_elemento(self, event):
        pass
    
    def soltar_elemento(self, event):
        pass
    
    def borrar_elemento(self, event):
        x, y = event.x, event.y
        items = self.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        
        if items:
            item = items[-1]
            self.eliminar_elemento(item)
    
    def borrar_elemento_manual(self):
        print("Seleccione el elemento a borrar en el canvas (clic derecho)")
    
    def eliminar_elemento(self, item_id):
        tags = self.canvas.gettags(item_id)
        
        if "figura" in tags:
            for figura in self.figuras[:]:
                if figura["id"] == item_id:
                    for texto in figura["textos"]:
                        self.canvas.delete(texto["id"])
                        self.textos = [t for t in self.textos if t["id"] != texto["id"]]
                    
                    self.eliminar_conexiones_relacionadas(item_id)
                    self.figuras.remove(figura)
                    break
            
        elif "texto" in tags:
            for texto in self.textos[:]:
                if texto["id"] == item_id:
                    if texto["figura"]:
                        for figura in self.figuras:
                            if figura["id"] == texto["figura"]:
                                figura["textos"] = [t for t in figura["textos"] if t["id"] != item_id]
                                break
                    self.textos.remove(texto)
                    break
        
        elif "flecha" in tags:
            self.conexiones = [c for c in self.conexiones if c["id"] != item_id]
        
        self.canvas.delete(item_id)
    
    def eliminar_conexiones_relacionadas(self, figura_id):
        for conexion in self.conexiones[:]:
            if conexion["origen"] == figura_id or conexion["destino"] == figura_id:
                self.canvas.delete(conexion["id"])
                self.conexiones.remove(conexion)
    
    def mostrar_en_consola(self):
        archivo = open("salida.txt", "w")
        
        # Identificar nodos importantes
        inicio = None
        finales = []
        bucles = {}  # {id_figura: tipo_bucle}
        decisiones = []
        archivo.write("#include <stdio.h>")
        for figura in self.figuras:
            textos = [t["texto"] for t in figura["textos"]]
            texto_completo = " ".join(textos)
            
            if texto_completo.startswith("INICIO"):
                inicio = figura["id"]
            elif texto_completo.startswith("FIN"):
                finales.append(figura["id"])
            elif texto_completo.startswith("while"):
                bucles[figura["id"]] = "while"
            elif texto_completo.startswith("for"):
                bucles[figura["id"]] = "for"
            elif texto_completo.startswith("if"):
                decisiones.append(figura["id"])
        
        if not inicio:
            archivo.write("// No se encontró nodo INICIO\n")
            archivo.close()
            return
        
        # Estructuras para manejar el flujo
        visitados = set()
        stack = []
        current = inicio
        indentacion = 0
        bloques_abiertos = []  # Para llevar registro de bloques abiertos
        
        while current:
            if current in visitados:
                # Manejo de bucles
                if current in bucles:
                    # Cerramos el bucle si volvemos al inicio
                    if bloques_abiertos and bloques_abiertos[-1] == current:
                        indentacion -= 4
                        archivo.write(" " * indentacion + "}\n")
                        bloques_abiertos.pop()
                current = None
                continue
                
            visitados.add(current)
            figura = next((f for f in self.figuras if f["id"] == current), None)
            if not figura:
                break
                
            textos = [t["texto"] for t in figura["textos"]]
            texto_completo = " ".join(textos)
            
            # Escribir el código según el tipo de figura
            if texto_completo.startswith("INICIO"):
                archivo.write("\n")
            elif texto_completo.startswith("FIN"):
                # Cerramos todos los bloques abiertos antes del FIN
                while bloques_abiertos:
                    indentacion -= 4
                    archivo.write(" " * indentacion + "}\n")
                    bloques_abiertos.pop()
                archivo.write("\n")
            elif current in bucles:
                tipo_bucle = bucles[current]
                archivo.write(" " * indentacion + f"{texto_completo} {{\n")
                indentacion += 4
                bloques_abiertos.append(current)
            elif current in decisiones:
                archivo.write(" " * indentacion + f"{texto_completo} {{\n")
                indentacion += 4
                bloques_abiertos.append(current)
            else:
                # Comandos normales
                if texto_completo:
                    archivo.write(" " * indentacion + f"{texto_completo}\n")
            
            # Manejo de conexiones
            conexiones = [c for c in self.conexiones if c["origen"] == current]
            
            if not conexiones:
                current = None
            elif len(conexiones) == 1:
                current = conexiones[0]["destino"]
            else:
                # Para decisiones o bucles con múltiples salidas
                if current in decisiones or current in bucles:
                    # Conexión "Sí" (primera) y "No" (segunda)
                    current = conexiones[0]["destino"]
                    stack.append((conexiones[1]["destino"], indentacion, current in decisiones))
                else:
                    current = conexiones[0]["destino"]
            
            # Si no hay más conexiones pero hay bloques pendientes
            if not current and stack:
                next_node, next_indent, is_decision = stack.pop()
                if is_decision:
                    indentacion = next_indent - 4
                    archivo.write(" " * indentacion + "} else {\n")
                    indentacion += 4
                current = next_node
        
        # Cerramos cualquier bloque que haya quedado abierto
        while bloques_abiertos:
            indentacion -= 4
            archivo.write(" " * indentacion + "}\n")
            bloques_abiertos.pop()
        
        archivo.close()
        print("[OK] Diagrama convertido a salida.txt")
    
    def buscar_bloque(self,id_bloque):
        for figura in self.figuras:
            if figura["id"] == id_bloque:
                textos_en_figura = " ".join([t["texto"] for t in figura["textos"]])
                if textos_en_figura == "FIN":
                    return "}\n"
                elif textos_en_figura == "if":
                    return textos_en_figura + " {\n"
                return textos_en_figura + "\n"
        return "//Error en busqueda"
            

    def limpiar_canvas(self):
        self.canvas.delete("all")
        self.figuras = []
        self.conexiones = []
        self.textos = []
        self.origen_conexion = None
        self.modo_actual = None
        self.ocultar_todos_los_elementos()
        
    def ajustar_texto_a_figura(self, figura_id):
        """Ajusta todos los textos de una figura a su tamaño actual"""
        figura = next((f for f in self.figuras if f["id"] == figura_id), None)
        if not figura:
            return
        
        coords = self.canvas.coords(figura_id)
        if len(coords) == 4:  # Rectángulo/Óvalo
            ancho = coords[2] - coords[0]
            alto = coords[3] - coords[1]
        else:  # Rombo (polygon)
            xs = coords[::2]
            ys = coords[1::2]
            ancho = max(xs) - min(xs)
            alto = max(ys) - min(ys)
        
        for texto_info in figura["textos"]:
            texto = texto_info["texto"]
            tamaño_fuente = max(8, min(14, int(min(ancho, alto) / len(texto))))
            
            # Actualizar el texto en el canvas
            self.canvas.itemconfig(texto_info["id"], 
                                font=(self.fuente_normal.actual()['family'], tamaño_fuente))
            
            # Actualizar en la estructura de datos
            texto_info["fuente"] = tamaño_fuente
            for t in self.textos:
                if t["id"] == texto_info["id"]:
                    t["fuente"] = tamaño_fuente
                    break
                
    def ajustar_figura_a_texto(self, figura_id, texto_completo):
        figura = next((f for f in self.figuras if f["id"] == figura_id), None)
        if not figura:
            return

        coords = self.canvas.coords(figura_id)
        if not coords:
            return

        margen = 20
        ancho_nuevo = max(60, len(texto_completo) * 10 + margen)
        alto_nuevo = 40  # altura fija

        tipo = figura["tipo"]

        # Calcular centro
        if len(coords) == 4:
            x1, y1, x2, y2 = coords
            centro_x = (x1 + x2) / 2
            centro_y = (y1 + y2) / 2
        else:
            xs = coords[::2]
            ys = coords[1::2]
            centro_x = sum(xs) / len(xs)
            centro_y = sum(ys) / len(ys)

        x1 = centro_x - ancho_nuevo / 2
        y1 = centro_y - alto_nuevo / 2
        x2 = centro_x + ancho_nuevo / 2
        y2 = centro_y + alto_nuevo / 2

        if tipo in ["rectangulo", "proceso", "llamada_funcion"]:
            self.canvas.coords(figura_id, x1, y1, x2, y2)

            # Si es llamada a función, eliminar y redibujar líneas internas
            if tipo == "llamada_funcion":
                for item in self.canvas.find_withtag("figura"):
                    if self.canvas.type(item) == "line":
                        bbox = self.canvas.bbox(item)
                        if bbox and x1 <= bbox[0] <= x2 and y1 <= bbox[1] <= y2:
                            self.canvas.delete(item)
                # Redibujar líneas internas
                self.canvas.create_line(
                    x1 + 10, y1, x1 + 10, y2, fill="black", width=1, tags="figura"
                )
                self.canvas.create_line(
                    x2 - 10, y1, x2 - 10, y2, fill="black", width=1, tags="figura"
                )

        elif tipo == "ovalo":
            self.canvas.coords(figura_id, x1, y1, x2, y2)

        elif tipo == "rombo":
            puntos = [
                centro_x, y1,
                x2, centro_y,
                centro_x, y2,
                x1, centro_y
            ]
            self.canvas.coords(figura_id, *puntos)

        elif tipo == "entrada_salida":
            puntos = [
                x1, y1,
                x2, y1,
                x2 - ancho_nuevo / 6, y2,
                x1 - ancho_nuevo / 6, y2
            ]
            self.canvas.coords(figura_id, *puntos)

        # Recentrar textos con nuevo tamaño de fuente
        for texto_info in figura["textos"]:
            tamaño_fuente = max(8, min(14, int(min(ancho_nuevo, alto_nuevo) / max(1, len(texto_completo)))))
            self.canvas.coords(texto_info["id"], centro_x, centro_y)
            self.canvas.itemconfig(
                texto_info["id"],
                font=(self.fuente_normal.actual()['family'], tamaño_fuente)
            )

            for t in self.textos:
                if t["id"] == texto_info["id"]:
                    t["fuente"] = tamaño_fuente
                    break

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagramaFlujoApp(root)
    root.mainloop()