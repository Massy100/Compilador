from tkinter import ttk, StringVar
from tkinter import messagebox

class ModoTexto:
    def __init__(self, app):
        self.app = app
        self.categorias = {
            "Palabra Clave": ["if", "else", "while", "switch", "case", "return", 
                            "print", "break", "for", "int", "float", "void", 
                            "double", "char", "const"],
            "Operador": ["+", "-", "*", "/", "=", "<", ">", "!", "_"],
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
        
        for categoria, elementos in self.categorias.items():
            frame = ttk.Frame(self.app.scrollable_frame, padding=(5, 2))
            frame.pack(fill="x", pady=(10, 0), padx=5)
            self.frames_categorias[categoria] = frame
            
            label = ttk.Label(frame, text=categoria, font=self.app.fuente_titulo)
            label.pack(anchor="w")
            
            for elemento in elementos:
                btn = ttk.Button(
                    frame, 
                    text=elemento, 
                    width=20,
                    command=lambda e=elemento, t=categoria: self.seleccionar_elemento(e, t)
                )
                btn.pack(fill="x", pady=2)

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
        
        texto = self.app.elemento_seleccionado
        if figura_objetivo:
            coords = self.app.canvas.coords(figura_objetivo)
            print(f"[DEBUG] Coordenadas figura: {coords}")
            
            if len(coords) == 4:  # Rectángulo/Óvalo
                ancho = coords[2] - coords[0]
                alto = coords[3] - coords[1]
                centro_x = (coords[0] + coords[2]) / 2
                centro_y = (coords[1] + coords[3]) / 2
            else:  # Rombo (polygon)
                xs = coords[::2]
                ys = coords[1::2]
                ancho = max(xs) - min(xs)
                alto = max(ys) - min(ys)
                centro_x = sum(xs) / len(xs)
                centro_y = sum(ys) / len(ys)
                
            print(f"[DEBUG] Centro calculado: x={centro_x}, y={centro_y}")
            
            # Calcular tamaño de fuente en base al tamaño de la figura
            tamaño_fuente = max(8, min(14, int(min(ancho, alto) / len(texto))))
            
            texto_id = self.app.canvas.create_text(
                centro_x, centro_y,
                text=texto,
                font=(self.app.fuente_normal.actual()['family'], tamaño_fuente),
                fill="black",
                tags="texto"
            )
            print(f"[DEBUG] Texto creado con ID: {texto_id}")
            
            self.app.canvas.tag_raise(texto_id)
            
            self.app.textos.append({
                "id": texto_id,
                "texto": texto,
                "tipo": self.app.tipo_seleccionado,
                "x": centro_x,
                "y": centro_y,
                "figura": figura_objetivo,
                "fuente": tamaño_fuente
            })
            
            # Actualizar la figura con este texto
            for figura in self.app.figuras:
                if figura["id"] == figura_objetivo:
                    figura["textos"].append({
                        "id": texto_id,
                        "texto": texto,
                        "tipo": self.app.tipo_seleccionado,
                        "fuente": tamaño_fuente
                    })
                    break
        else:
            # Para texto libre (sin figura), usar tamaño de fuente normal
            texto_id = self.app.canvas.create_text(
                x, y,
                text=texto,
                font=self.app.fuente_normal,
                fill="black",
                tags="texto"
            )
            
            self.app.textos.append({
                "id": texto_id,
                "texto": texto,
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
        
        # Obtener posición de la figura
        coords = self.app.canvas.coords(self.figura_destino)
        if not coords:
            return
            
        # Calcular posición central y tamaño de fuente
        if len(coords) == 4:  # Rectángulo/Óvalo
            ancho = coords[2] - coords[0]
            alto = coords[3] - coords[1]
            x = (coords[0] + coords[2]) / 2
            y = (coords[1] + coords[3]) / 2
        else:  # Rombo (polygon)
            xs = coords[::2]
            ys = coords[1::2]
            ancho = max(xs) - min(xs)
            alto = max(ys) - min(ys)
            x = sum(xs) / len(xs)
            y = sum(ys) / len(ys)
        
        tamaño_fuente = max(8, min(14, int(min(ancho, alto) / max(1, len(texto)))))
        
        print(f"[DEBUG] Posición calculada para texto: x={x}, y={y}, tamaño fuente: {tamaño_fuente}")
        
        # Crear el texto en el canvas
        texto_id = self.app.canvas.create_text(
            x, y,
            text=texto,
            font=(self.app.fuente_normal.actual()['family'], tamaño_fuente),
            fill="black",
            tags="texto"
        )
        print(f"[DEBUG] Texto creado con ID: {texto_id}")
        
        # Registrar en la estructura de datos
        self.app.textos.append({
            "id": texto_id,
            "texto": texto,
            "tipo": tipo,
            "x": x,
            "y": y,
            "figura": self.figura_destino,
            "fuente": tamaño_fuente
        })
        
        # Actualizar la figura con este texto
        for figura in self.app.figuras:
            if figura["id"] == self.figura_destino:
                figura["textos"].append({
                    "id": texto_id,
                    "texto": texto,
                    "tipo": tipo,
                    "fuente": tamaño_fuente
                })
                break
        
        # Resetear el estado y restaurar bordes
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