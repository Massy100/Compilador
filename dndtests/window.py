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
        self.lines = []  

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
#        Button(self.elements_frame, text="Codigo", command=).grid(row=len(btnTxts), column=0, sticky="ew")

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
                shape = self.canvas.create_polygon(points, fill="grey", tags=[tag, "terminal"], smooth=True)
                textFunction = 4
            self.canvas.addtag_withtag("shape", shape)

            tag_text = [tag, "text"]
            addText_bind = lambda e: self.shape_addText(f"{tag}&&text", self.dlg(textFunction))
                
            self.shapes.append(tag) 
            
            self.canvas.tag_bind(tag, "<Double-Button-1>", addText_bind)
            self.canvas.tag_bind(shape, "<1>", lambda e: self.savePosn(e, tag))
            self.canvas.tag_bind(tag, "<ButtonRelease-1>", lambda e: self.release_btn(e, tag))
            self.canvas.tag_bind(tag, "<Double-Button-3>", lambda e: self.delete_shape(tag))
            
            text = self.canvas.create_text(e.x, e.y, text="", fill="black", tags=tag_text)
            self.canvas.lift(text, tag)
            self.texts.append(text) 

            #if len(self.shapes) > 1:
            #    self.connect_shape(self.shapes[-2], self.shapes[-1])  

    def delete_shape(self, tag):
        self.canvas.delete(tag)
        self.shapes.remove(tag)
        
        print(self.canvas.find_all())
        print(self.shapes)

    def savePosn(self, e, tag):
        if self.selection_mode:
            self.lastx, self.lasty = e.x, e.y
        elif self.conecction_mode:
            self.lastx, self.lasty = self.getCenter(tag)

    def getCenter(self, tag):
        coords = self.canvas.coords(f"{tag}&&shape")
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
        secondTag = self.canvas.find_closest(e.x, e.y)[0]
        secondTag = self.canvas.gettags(secondTag)[0]
        choiceTag = ""
        if "cond" in tag:
            lines = self.canvas.find_withtag(tag+"&&0&&line")
            choiceTag = "0" if len(lines) == 0 else "1"

                
        self.connect_shape(tag, secondTag, choiceTag)

    def connect_shape(self, tag1, tag2, choicetag=None):
        tag1_coords = self.getCenter(tag1)
        tag2_coords = self.getCenter(tag2)

        height_offset = shape_height

        if tag1_coords[1] < tag2_coords[1]:
            height_offset *= -1

        tags = [tag1, tag2]
        if choicetag:
            tags.append(choicetag)

        tags.append("line")
        line = self.canvas.create_line(tag1_coords[0], tag1_coords[1], tag2_coords[0], tag2_coords[1] + height_offset, fill="black", width=2, tags=tags, arrow=LAST)
        self.canvas.lower(line)
        print(self.canvas.gettags(line))

    def move_shape(self, event, tag):
        self.canvas.move(tag, event.x - self.lastx, event.y - self.lasty)
        self.canvas.move(tag+"_text", event.x - self.lastx, event.y - self.lasty)
        self.move_line(tag)

    def move_line(self, tag):
        ids = self.canvas.find_withtag(f"{tag}&&line")
        for id in ids:
            tag1 = self.canvas.gettags(id)[0]
            tag2 = self.canvas.gettags(id)[1]

            tag1_coords = self.getCenter(tag1)
            tag2_coords = self.getCenter(tag2)

            height_offset = shape_height

            if tag1_coords[1] < tag2_coords[1]:
                height_offset *= -1

            self.canvas.coords(id, tag1_coords[0], tag1_coords[1], tag2_coords[0], tag2_coords[1]+height_offset)
            self.canvas.tag_lower(id)
        
    def shape_addText(self, tag, text=""):
        self.canvas.itemconfig(tag, text=text) 

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
                addCombo(dlg, typeVar, types, 0, 0)
                
                idVar = StringVar()
                addEntry(dlg, idVar, self.check_identifier_wrapper, 0, 1)

                lbl = ttk.Label(dlg, text="=")
                lbl.grid(row=0, column=2, sticky="ew")

                valueVar = StringVar()
                addEntry(dlg, valueVar, self.check_value_wrapper, 0, 3)
                
            case 1:
                title = "Condición"
                
                typeVar = StringVar()
                types = ["if", "while", "for"]
                addCombo(dlg, typeVar, types, 0, 0)

                conditionVar = StringVar()
                txtCondition = addEntry(dlg, conditionVar, self.check_condition_wrapper, 0, 1)
                txtCondition.focus_set()

            case 2:
                title = "Entrada/Salida"

                lblMsg = ttk.Label(dlg, text="Mensaje entre comillas")
                lblMsg.grid(row=0, column=0, sticky="ew")

                msgVar = StringVar()
                txtMsg = addEntry(dlg, msgVar, self.check_string_wrapper, 0, 1)
                txtMsg.focus_set()
 
                typeVar = StringVar()
                types = ["Escribir", "Leer"]
                addCombo(dlg, typeVar, types, 1, 0)

                idVar = StringVar()
                addEntry(dlg, idVar, self.check_identifier_wrapper, 1, 1)
                
            case 3:
                title = "Función"
                lblCall = ttk.Label(dlg, text="Función")
                lblCall.grid(row=0, column=0, sticky="ew")

                idVar = StringVar()
                txtId = addEntry(dlg, idVar, self.check_identifier_wrapper, 0, 1)
                txtId.focus_set()

                lblParam = ttk.Label(dlg, text="Parámetros")
                lblParam.grid(row=1, column=0, sticky="ew")
                
                paramVar = StringVar()
                addEntry(dlg, paramVar, self.check_param_wrapper, 1, 1)
                

            case 4:
                title = "Terminal"
                idVar = StringVar()
                txtId = addEntry(dlg, idVar, self.check_identifier_wrapper, 0, 0)
                txtId.focus_set()

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
                result = f"{typeVar.get()} ({conditionVar.get()})"
            case 2:
                result = f"{msgVar.get()}\n{typeVar.get()} {idVar.get()}"
            case 3:
                result = f"{idVar.get()}({paramVar.get()});"
            case 4:
                result = f"{idVar.get()}"
        return result
    
def addEntry(parent, trackVar, validateCommand, row, col):
    entry = ttk.Entry(parent, textvariable=trackVar, validatecommand=validateCommand)
    entry.grid(row=row, column=col, sticky="ew")
    return entry

def addCombo(parent, trackVar, values, row, col):
    combo = ttk.Combobox(parent, textvariable=trackVar, values=values, state="readonly")
    combo.grid(row=row, column=col, sticky="ew")
    return combo


if __name__ == "__main__":
    root = Tk()
    app = Window(root)
    root.mainloop()