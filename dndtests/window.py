from tkinter import *
from tkinter import ttk

import re

shape_height = 25
shape_width = 50

btnTxts = ["Cursor", "Conexión", "Proceso", "Condición", "Entrada/Salida", "Llamada a Función", "Terminal"]

token_patron = {
    "PREPROCESSOR": r'\#include\b',  
    "HEADER": r'<[a-zA-Z0-9_.]+>',  
    "KEYWORD": r'\b(if|else|while|switch|case|return|print|break|for|int|float|void|double|char|const)\b',
    "LIB_FUNCTION": r'\b(printf|scanf)\b',
    "IDENTIFIER": r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
    "NUMBER": r'\b\d+(\.\d+)?f?\b',
    "OPERATOR": r'[\+\-\*\/\=\<\>\!\_]',
    "DELIMITER": r'[(),;{}]',
    "WHITESPACE": r'\s+',
    "STRING": r'"[^"]*"',  
}

value_pattern = f"(?:(?:{token_patron['IDENTIFIER']}|{token_patron['NUMBER']}|{token_patron['STRING']})(?: *[-+*/] *)?)+" 
logical_pattern = fr"(?:(?:{token_patron['IDENTIFIER']}|{token_patron['NUMBER']}|{token_patron['STRING']})(?: *(?:==|<|>|<=|>=|!|&&|\|\|) *)?)+" 
parameter_pattern = f"(?:(?:{token_patron['IDENTIFIER']}|{token_patron['NUMBER']}|{token_patron['STRING']})(?:, *)?)+"

class Window:
    def __init__(self, root:Tk):
        self.root = root
        self.root.title("Canvas test")
        self.root.geometry("600x400")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=5)

        self.current_element = None
        self.shapes = []
        self.texts = []

        self.selection_mode = True 
        self.connection_mode = True 

        self.create_frames()
        self.fill_frames()

        self.check_identifier_wrapper = (self.root.register(self.check_identifier), '%P', '%d', '%i')
        self.check_number_wrapper = (self.root.register(self.check_num), '%P')
        self.check_string_wrapper = (self.root.register(self.check_string), '%P')
        self.check_value_wrapper = (self.root.register(self.check_value), '%P')
        self.check_condition_wrapper = (self.root.register(self.check_condition), '%P')
        self.check_param_wrapper = (self.root.register(self.check_param), '%P')

        self.lastx = 0
        self.lasty = 0

    def create_frames(self):
        self.canvas_frame = Frame(self.root)
        self.canvas_frame.grid(row=1, column=1, sticky="nsew")
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.elements_frame = Frame(self.root)
        self.elements_frame.grid(row=1, column=0, sticky="nsew")

    def fill_frames(self):
        self.canvas = Canvas(self.canvas_frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.columnconfigure(0, weight=1)    
        self.canvas.rowconfigure(0, weight=1)

        self.elements_frame.columnconfigure(0, weight=1)
        for i in range(len(btnTxts)):
            btn = Button(self.elements_frame, text=btnTxts[i], command=lambda i=i: self.canvas_mode(btnTxts[i]))
            btn.grid(row=i, column=0, sticky="ew")
            self.elements_frame.rowconfigure(i, weight=1)

        self.canvas.bind("<Button-1>", lambda e: self.on_click(e))
    
    def canvas_mode(self, text):
        self.selection_mode = text == "Cursor"
        self.conecction_mode = text == "Conexión"
        self.current_element = text
        print(self.current_element)    

    def on_click(self, e):
        if self.selection_mode or self.conecction_mode:
            return
        else:
            if self.current_element == "Proceso":
                tag = f"sent{len(self.shapes)}"
                shape = self.canvas.create_rectangle(e.x-shape_width, e.y-shape_height, e.x + shape_width, e.y + shape_height, fill="grey", tags=tag, outline="")  
                textFunction = 0  
            elif self.current_element == "Condición":
                tag = f"cond{len(self.shapes)}"
                shape = self.canvas.create_polygon([(e.x, e.y+shape_height), (e.x+shape_width, e.y), (e.x, e.y-shape_height),(e.x-shape_width, e.y)], fill="grey", tags=tag)
                textFunction = 1
            elif self.current_element == "Entrada/Salida":
                tag = f"io{len(self.shapes)}"
                shape = self.canvas.create_polygon([(e.x-shape_width , e.y-shape_height), (e.x+(2*shape_width), e.y-shape_height), (e.x+shape_width, e.y+shape_height), (e.x-(2*shape_width),e.y+shape_height)], fill="grey", tags=tag)
                textFunction = 2
            elif self.current_element == "Llamada a Función":
                tag = f"func{len(self.shapes)}"
                shape = self.canvas.create_rectangle(e.x-shape_width, e.y-shape_height, e.x + shape_width, e.y + shape_height, fill="grey", tags=tag, outline="")
                self.canvas.create_line(e.x-(shape_width-10), e.y-shape_height, e.x - (shape_width-10), e.y + shape_height, fill="black", width=1, tags=tag)
                self.canvas.create_line(e.x+(shape_width-10), e.y-shape_height, e.x + (shape_width-10), e.y + shape_height, fill="black", width=1, tags=tag)
                textFunction = 3
            elif self.current_element == "Terminal":
                tag = f"terminal{len(self.shapes)}"
                points = [
                    (e.x-30 , e.y), 
                    (e.x-20 , e.y-12),
                    (e.x , e.y-12),
                    (e.x+20, e.y-12),
                    (e.x+30, e.y),
                    (e.x+20,e.y+12),
                    (e.x , e.y+12),
                    (e.x-20,e.y+12)
                    
                ]
                shape = self.canvas.create_polygon(points, fill="grey", tags=tag, smooth=True)
                textFunction = 4
            addText_bind = lambda e: self.shape_addText(tag_text, self.dlg(textFunction))
                
            tag_text = f"{tag}_text"
            self.shapes.append(tag) 
            
            self.canvas.tag_bind(tag, "<Double-Button-1>", addText_bind)
            self.canvas.tag_bind(shape, "<1>", lambda e: self.savePosn(e, tag))
            self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e: self.release_btn(e, tag))
            
            text = self.canvas.create_text(e.x, e.y, text="", fill="black", tags=tag_text)
            self.canvas.lift(text, tag)
            self.texts.append(text) 

    def savePosn(self, e, tag):
        if self.selection_mode:
            self.lastx, self.lasty = e.x, e.y
        elif self.conecction_mode:
            self.lastx, self.lasty = self.getCenter(tag)

    def getCenter(self, tag):
        coords = self.canvas.coords(tag)
        x_cords = coords[::2]
        y_cords = coords[1::2]

        center_x = (max(x_cords) + min(x_cords)) / 2
        center_y = (max(y_cords) + min(y_cords)) / 2

        return center_x, center_y        

    def release_btn(self, e, tag):
        if self.selection_mode:
            self.move_shape(e, tag)
        elif self.conecction_mode:
            self.connection(e, tag)
    
    def connection(self, e, tag):
        secondTag = self.canvas.find_closest(e.x, e.y,start=tag+"_line")[0]
        secondTag = self.canvas.gettags(secondTag)[0]
        centerCoords = self.getCenter(secondTag)
        self.canvas.create_line(self.lastx, self.lasty, centerCoords[0], centerCoords[1], fill="black", width=2, tags=[tag+"_line", secondTag+"_line", tag+"_"+secondTag])

        self.canvas.tag_lower(tag +"_line")
        self.canvas.tag_lower(secondTag +"_line")

    def move_shape(self, event, tag):
        self.canvas.move(tag, event.x - self.lastx, event.y - self.lasty)
        self.canvas.move(tag+"_text", event.x - self.lastx, event.y - self.lasty)
        self.move_line(tag)

    def move_line(self, tag):
        ids = self.canvas.find_withtag(tag+"_line")
        if len(ids) == 0:
            return
        for id in ids:
            tag2 = self.canvas.gettags(id)[2].replace(tag, "").replace("_", "")
            tag1_coords = self.getCenter(tag)
            tag2_coords = self.getCenter(tag2)
            self.canvas.coords(id, tag1_coords[0], tag1_coords[1], tag2_coords[0], tag2_coords[1])
            self.canvas.tag_lower(tag+"_line")
            self.canvas.tag_lower(tag2+"_line")
        

    def shape_addText(self, tag, text=""):
        print(text)
        self.canvas.itemconfig(tag, text=text) 
        print(self.canvas.itemcget(tag, "text")) 

    def check_identifier(self, newval, action, index):
        # Check if the new value matches the pattern
        if action == "0" and index == "0":
            return True
        return re.fullmatch(token_patron["IDENTIFIER"], newval) is not None
    
    def check_num(self, newval):
        # Check if the new value matches the pattern
        return re.fullmatch(token_patron["NUMBER"], newval) is not None
    
    def check_string(self, newval):
        # Check if the new value matches the pattern
        return re.fullmatch(token_patron["STRING"], newval) is not None
    
    def check_value(self, newval:str):
        # Check if the new value matches the pattern
        if newval == "":
            return True
        if newval.endswith(("+", "-", "*", "/")):
            return False
        return re.fullmatch(value_pattern, newval) is not None

    def check_condition(self, newval:str):
        # Check if the new value matches the pattern
        if newval.endswith(("&&", "||", "==", "<", ">", "<=", ">=", "!")):
            return False
        return re.fullmatch(logical_pattern, newval) is not None
    
    def check_param(self, newval:str):
        # Check if the new value matches the pattern
        if newval.endswith(","):
            return False
        return re.fullmatch(parameter_pattern, newval) is not None

    def dlg(self, type:int):
        def dismiss():
            for widget in dlg.winfo_children():
                if isinstance(widget, ttk.Entry):
                    if not widget.validate():
                        widget.focus_set()
                        return
            dlg.grab_release()
            dlg.destroy()

        dlg = Toplevel(self.root)
        result = ""
        match type:
            case 0:
                typeVar = StringVar()
                types = ["","int", "float", "char", "double"]
                commboType = ttk.Combobox(dlg,textvariable=typeVar, values=types, state="readonly")
                commboType.grid(row=0, column=0, sticky="ew")
                commboType.focus_set()
                
                idVar = StringVar()
                txtid = ttk.Entry(dlg, textvariable=idVar, validatecommand=self.check_identifier_wrapper)
                txtid.grid(row=0, column=1, sticky="ew")

                lbl = ttk.Label(dlg, text="=")
                lbl.grid(row=0, column=2, sticky="ew")

                valueVar = StringVar()
                txtvalue = ttk.Entry(dlg, textvariable=valueVar, validatecommand=self.check_value_wrapper)
                txtvalue.grid(row=0, column=3, sticky="ew")
                
                
            case 1:
                title = "Condición"
                
                conditionVar = StringVar()
                txtcondition = ttk.Entry(dlg, textvariable=conditionVar, validatecommand=self.check_condition_wrapper)
                txtcondition.grid(row=0, column=0, sticky="ew")
                txtcondition.focus_set()

            case 2:
                title = "Entrada/Salida"

                lblMsg = ttk.Label(dlg, text="Mensaje entre comillas")
                lblMsg.grid(row=0, column=0, sticky="ew")

                msgVar = StringVar()
                txtmsg = ttk.Entry(dlg, textvariable=msgVar, validatecommand=self.check_string_wrapper)
                txtmsg.grid(row=0, column=1, sticky="ew")
                txtmsg.focus_set()

                typeVar = StringVar()
                types = ["Escribir", "Leer"]
                commboType = ttk.Combobox(dlg,textvariable=typeVar, values=types, state="readonly")
                commboType.grid(row=1, column=0, sticky="ew")

                idVar = StringVar()
                txtid = ttk.Entry(dlg, textvariable=idVar, validatecommand=self.check_identifier_wrapper)
                txtid.grid(row=1, column=1, sticky="ew")
                
            case 3:
                title = "Función"
                lblCall = ttk.Label(dlg, text="Función")
                lblCall.grid(row=0, column=0, sticky="ew")

                idVar = StringVar()
                txtid = ttk.Entry(dlg, textvariable=idVar, validatecommand=self.check_identifier_wrapper)
                txtid.grid(row=0, column=1, sticky="ew")
                txtid.focus_set()

                lblParam = ttk.Label(dlg, text="Parámetros")
                lblParam.grid(row=1, column=0, sticky="ew")
                paramVar = StringVar()
                txtparam = ttk.Entry(dlg, textvariable=paramVar, validatecommand=self.check_param_wrapper)
                txtparam.grid(row=1, column=1, sticky="ew")

            case 4:
                title = "Terminal"
                idVar = StringVar()
                txtid = ttk.Entry(dlg, textvariable=idVar, validatecommand=self.check_identifier_wrapper)
                txtid.grid(row=0, column=0, sticky="ew")
                txtid.focus_set()

        doneBtn = ttk.Button(dlg, text="Done", command=dismiss)
        doneBtn.grid(row=2, column=0, columnspan=4, sticky="ew")
        doneBtn.columnconfigure(0, weight=5)
        dlg.rowconfigure(1, weight=5)

        dlg.protocol("WM_DELETE_WINDOW",  dismiss)
        dlg.transient(root)
        dlg.wait_visibility() 
        dlg.grab_set()        
        dlg.wait_window()

        match type:
            case 0:
                result = f"{typeVar.get()} {idVar.get()}{' = '+ valueVar.get() if valueVar.get() else ''};"
            case 1:
                result = f"{conditionVar.get()}"
            case 2:
                result = f"{msgVar.get()}\n{typeVar.get()} {idVar.get()}"
            case 3:
                result = f"{idVar.get()}({paramVar.get()});"
            case 4:
                result = f"{idVar.get()}"
        return result

if __name__ == "__main__":
    root = Tk()
    app = Window(root)
    root.mainloop()