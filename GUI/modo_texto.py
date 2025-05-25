from tkinter import ttk, StringVar
from tkinter import messagebox

class ModoTexto:
    def __init__(self, app):
        self.app = app
        self.categorias = {
            "Palabra Clave": ["if", "else", "return", "while", "for", "in", "range",
                            "printf", "break", "int", "float", "void", 
                            "double", "char", "const", "true", "false"],
            "Operador": ["+", "-", "*", "/", "=", "<", ">", "!", "_", '"'],
            "Delimitadores": ["(", ")", ",", ";", "{", "}"],
            "Terminal": ["INICIO", "FIN"]
        }
        self.frames_categorias = {}
        self.texto_var = StringVar()
        self.modo_edicion = None  # 'variable', 'valor' o None
        self.figura_destino = None
    
    def mostrar_elementos(self):
        self.app.ocultar_todos_los_elementos()
        
        # Configurar el evento de clic en el canvas específico para este modo
        print("[DEBUG] Configurando binding para clics en el canvas (ModoTexto)")
        self.app.canvas.unbind("<Button-1>")  # Eliminar cualquier binding previo
        self.app.canvas.bind("<Button-1>", self.manejar_clic_texto)
        
        # Resto del código de mostrar_elementos...
        self.crear_seccion_texto_manual()
        frameTexto = ttk.Frame(self.app.scrollable_frame, padding=(5, 2))
        frameTexto.pack(fill="both", expand=True, pady=(10, 0), padx=5)

        # Número de columnas en la cuadrícula
        columnas = 2
        fila = 0
        columna = 0

        for i, (categoria, elementos) in enumerate(self.categorias.items()):
            frame = ttk.Frame(frameTexto, padding=(5, 2), relief="groove", borderwidth=2)
            frame.grid(row=fila, column=columna, padx=5, pady=5, sticky="nsew")
            self.frames_categorias[categoria] = frame

            label = ttk.Label(frame, text=categoria, font=self.app.fuente_titulo)
            label.pack(anchor="w")

            for elemento in elementos:
                btn = ttk.Button(
                    frame,
                    text=elemento,
                    width=10,
                    command=lambda e=elemento, t=categoria: self.seleccionar_elemento(e, t)
                )
                btn.pack(pady=2)

            # Actualizar posición en la cuadrícula
            columna += 1
            if columna >= columnas:
                columna = 0
                fila += 1


    def manejar_clic_texto(self, event):
        print(f"\n[DEBUG] Click en ModoTexto - Coordenadas: x={event.x}, y={event.y}")
        
        # Verificar si estamos en modo edición (variable/valor)
        if hasattr(self, 'modo_edicion') and self.modo_edicion:
            print("[DEBUG] En modo edición, redirigiendo a seleccionar_figura_destino")
            self.seleccionar_figura_destino(event)
            return
        
        # Comportamiento normal para agregar texto
        if not self.app.elemento_seleccionado:
            print("[DEBUG] No hay elemento seleccionado, ignorando clic")
            return
            
        print("[DEBUG] Creando texto con elemento seleccionado")
        self.crear_texto(event.x, event.y)

    def crear_texto(self, x, y):
        print(f"[DEBUG] Buscando figuras en posición x={x}, y={y}")
        
        # Buscar figuras en la posición del clic
        figuras_en_posicion = self.app.canvas.find_overlapping(x-1, y-1, x+1, y+1)
        print(f"[DEBUG] Figuras encontradas: {figuras_en_posicion}")
        
        figura_objetivo = None
        
        for item in figuras_en_posicion:
            tags = self.app.canvas.gettags(item)
            print(f"[DEBUG] Revisando item {item} con tags: {tags}")
            
            if "figura" in tags:
                figura_objetivo = item
                print(f"[DEBUG] Figura objetivo encontrada: {figura_objetivo}")
                break
        
        texto_nuevo = self.app.elemento_seleccionado
        
        if figura_objetivo:
            # Buscar la figura en la estructura de datos
            figura_data = None
            for figura in self.app.figuras:
                if figura["id"] == figura_objetivo:
                    figura_data = figura
                    break
            
            if not figura_data:
                return
                
            # Concatenar el nuevo texto con los existentes (si los hay)
            textos_existentes = [t["texto"] for t in figura_data["textos"]]
            texto_completo = " ".join(textos_existentes + [texto_nuevo])
            
            # Eliminar los textos antiguos
            for texto_info in figura_data["textos"]:
                self.app.canvas.delete(texto_info["id"])
                self.app.textos = [t for t in self.app.textos if t["id"] != texto_info["id"]]
            
            figura_data["textos"] = []  # Limpiar textos de la figura
            
            # Obtener coordenadas actuales de la figura
            coords = self.app.canvas.coords(figura_objetivo)
            if not coords:
                return
                
            # Calcular nuevo tamaño basado en el texto completo
            if len(coords) == 4:  # Rectángulo/Óvalo
                ancho_actual = coords[2] - coords[0]
                alto_actual = coords[3] - coords[1]
                
                # Calcular nuevo tamaño (ancho proporcional al texto)
                margen = 20
                ancho_nuevo = max(60, len(texto_completo) * 10 + margen)
                alto_nuevo = max(40, alto_actual)  # Mantener alto mínimo
                
                # Calcular nuevas coordenadas (centradas en la posición original)
                centro_x = (coords[0] + coords[2]) / 2
                centro_y = (coords[1] + coords[3]) / 2
                x1 = centro_x - ancho_nuevo/2
                y1 = centro_y - alto_nuevo/2
                x2 = centro_x + ancho_nuevo/2
                y2 = centro_y + alto_nuevo/2
                
                # Actualizar figura
                if self.app.canvas.type(figura_objetivo) == "rectangle":
                    self.app.canvas.coords(figura_objetivo, x1, y1, x2, y2)
                elif self.app.canvas.type(figura_objetivo) == "oval":
                    self.app.canvas.coords(figura_objetivo, x1, y1, x2, y2)
                    
            elif len(coords) > 4:  # Rombo (polygon)
                xs = coords[::2]
                ys = coords[1::2]
                ancho = max(xs) - min(xs)
                alto = max(ys) - min(ys)
                centro_x = sum(xs) / len(xs)
                centro_y = sum(ys) / len(ys)
                
                # Para mantener compatibilidad con el resto del código
                ancho_nuevo = ancho
                alto_nuevo = alto

            
            # Calcular tamaño de fuente
            tamaño_fuente = max(8, min(14, int(min(ancho_nuevo, alto_nuevo) / max(1, len(texto_completo)))))
            
            # Crear el nuevo texto
            texto_id = self.app.canvas.create_text(
                centro_x, centro_y,
                text=texto_completo,
                font=(self.app.fuente_normal.actual()['family'], tamaño_fuente),
                fill="black",
                tags="texto"
            )
            
            # Registrar en estructuras de datos
            self.app.textos.append({
                "id": texto_id,
                "texto": texto_completo,
                "tipo": self.app.tipo_seleccionado,
                "x": centro_x,
                "y": centro_y,
                "figura": figura_objetivo,
                "fuente": tamaño_fuente
            })
            
            figura_data["textos"].append({
                "id": texto_id,
                "texto": texto_completo,
                "tipo": self.app.tipo_seleccionado,
                "fuente": tamaño_fuente
            })
            
        else:
            # Para texto libre (sin figura)
            texto_id = self.app.canvas.create_text(
                x, y,
                text=texto_nuevo,
                font=self.app.fuente_normal,
                fill="black",
                tags="texto"
            )
            
            self.app.textos.append({
                "id": texto_id,
                "texto": texto_nuevo,
                "tipo": self.app.tipo_seleccionado,
                "x": x,
                "y": y,
                "figura": None,
                "fuente": self.app.fuente_normal.actual()['size']
            })
        
    def crear_seccion_texto_manual(self):
        frame_edicion = ttk.Frame(self.app.scrollable_frame, padding=(5, 2))
        frame_edicion.pack(fill="x", pady=(10, 0), padx=5)
        
        label = ttk.Label(frame_edicion, text="Texto Manual", font=self.app.fuente_titulo)
        label.pack(anchor="w")
        
        # Botones para modo variable/valor
        ttk.Button(
            frame_edicion,
            text="Ingresar Variable",
            command=self.preparar_ingreso_variable
        ).pack(fill="x", pady=2)
        
        ttk.Button(
            frame_edicion,
            text="Ingresar Valor",
            command=self.preparar_ingreso_valor
        ).pack(fill="x", pady=2)
        
        # Campo de entrada
        self.entrada_texto = ttk.Entry(frame_edicion, textvariable=self.texto_var)
        self.entrada_texto.pack(fill="x", pady=5)
        self.entrada_texto.config(state="disabled")
        
        # Botón de confirmación
        self.btn_confirmar = ttk.Button(
            frame_edicion,
            text="Asignar a Figura",
            command=self.asignar_texto_manual,
            state="disabled"
        )
        self.btn_confirmar.pack(fill="x", pady=2)
    
    def preparar_ingreso_variable(self):
        print("[DEBUG] Preparando ingreso de variable")
        self.modo_edicion = "variable"
        self.entrada_texto.config(state="normal")
        self.texto_var.set("")
        self.btn_confirmar.config(state="normal")
        self.app.canvas.bind("<Button-1>", self.seleccionar_figura_destino)
        messagebox.showinfo("Instrucción", "Escriba el nombre de la variable y luego seleccione la figura destino")
    
    def preparar_ingreso_valor(self):
        print("[DEBUG] Preparando ingreso de valor")
        self.modo_edicion = "valor"
        self.entrada_texto.config(state="normal")
        self.texto_var.set("")
        self.btn_confirmar.config(state="normal")
        self.app.canvas.bind("<Button-1>", self.seleccionar_figura_destino)
        messagebox.showinfo("Instrucción", "Escriba el valor numérico y luego seleccione la figura destino")
    
    def seleccionar_figura_destino(self, event):
        print(f"[DEBUG] Buscando figura destino en x={event.x}, y={event.y}")
        x, y = event.x, event.y
        items = self.app.canvas.find_overlapping(x-1, y-1, x+1, y+1)
        print(f"[DEBUG] Items encontrados: {items}")
        
        # Restaurar bordes de todas las figuras primero
        self.app.restaurar_bordes_figuras()
        
        for item in items:
            tags = self.app.canvas.gettags(item)
            print(f"[DEBUG] Revisando item {item} con tags: {tags}")
            if "figura" in tags:
                self.figura_destino = item
                # Resaltar la figura seleccionada
                self.app.resaltar_figura(item)
                messagebox.showinfo("Selección", f"Figura {item} seleccionada como destino")
                return
        
        messagebox.showerror("Error", "Debe seleccionar una figura válida")
    
    def asignar_texto_manual(self):
        print("[DEBUG] Intentando asignar texto manual")
        if not self.figura_destino:
            messagebox.showerror("Error", "No se ha seleccionado una figura destino")
            return
            
        texto = self.texto_var.get().strip()
        print(f"[DEBUG] Texto a asignar: '{texto}' (modo: {self.modo_edicion})")
        
        # Validaciones según el modo
        if self.modo_edicion == "variable":
            if not texto.isidentifier():
                messagebox.showerror("Error", "Nombre de variable inválido. Solo use letras")
                return
            tipo = "variable"
        elif self.modo_edicion == "valor":
            if not texto.isdigit():
                messagebox.showerror("Error", "Valor inválido. Solo use números")
                return
            tipo = "valor"
        else:
            return

        # Buscar figura
        figura_data = next((f for f in self.app.figuras if f["id"] == self.figura_destino), None)
        if not figura_data:
            return

        # Concatenar con texto existente
        textos_existentes = [t["texto"] for t in figura_data["textos"]]
        texto_completo = " ".join(textos_existentes + [texto])

        # Eliminar textos antiguos
        for texto_info in figura_data["textos"]:
            self.app.canvas.delete(texto_info["id"])
            self.app.textos = [t for t in self.app.textos if t["id"] != texto_info["id"]]
        figura_data["textos"] = []

        # Redimensionar figura al nuevo texto
        self.app.ajustar_figura_a_texto(self.figura_destino, texto_completo)

        # Recalcular posición central
        coords = self.app.canvas.coords(self.figura_destino)
        if len(coords) == 4:
            centro_x = (coords[0] + coords[2]) / 2
            centro_y = (coords[1] + coords[3]) / 2
        else:
            xs = coords[::2]
            ys = coords[1::2]
            centro_x = sum(xs) / len(xs)
            centro_y = sum(ys) / len(ys)

        # Calcular tamaño de fuente
        ancho = max(coords[::2]) - min(coords[::2])
        alto = max(coords[1::2]) - min(coords[1::2])
        tamaño_fuente = max(8, min(14, int(min(ancho, alto) / max(1, len(texto_completo)))))

        # Crear texto unificado
        texto_id = self.app.canvas.create_text(
            centro_x, centro_y,
            text=texto_completo,
            font=(self.app.fuente_normal.actual()['family'], tamaño_fuente),
            fill="black",
            tags="texto"
        )

        # Registrar
        self.app.textos.append({
            "id": texto_id,
            "texto": texto_completo,
            "tipo": tipo,
            "x": centro_x,
            "y": centro_y,
            "figura": self.figura_destino,
            "fuente": tamaño_fuente
        })
        figura_data["textos"].append({
            "id": texto_id,
            "texto": texto_completo,
            "tipo": tipo,
            "fuente": tamaño_fuente
        })

        self.resetear_edicion()
        self.app.restaurar_bordes_figuras()
    
    def resetear_edicion(self):
        print("[DEBUG] Reseteando edición")
        self.texto_var.set("")
        self.entrada_texto.config(state="disabled")
        self.btn_confirmar.config(state="disabled")
        self.modo_edicion = None
        self.figura_destino = None
        self.app.canvas.unbind("<Button-1>")
    
    def seleccionar_elemento(self, elemento, categoria):
        print(f"\n[DEBUG] seleccionar_elemento() - Elemento: {elemento}, Categoría: {categoria}")
        self.app.elemento_seleccionado = elemento
        self.app.tipo_seleccionado = categoria
        print(f"[DEBUG] Valores actualizados - elemento_seleccionado: {self.app.elemento_seleccionado}, tipo_seleccionado: {self.app.tipo_seleccionado}")
        if self.modo_edicion:
            self.resetear_edicion()