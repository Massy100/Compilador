from tkinter import *
from tkinter import ttk

import re

texto = ["Cursor", "B", "C", "D", "E", "F", "Ovalo", "Rectangulo", "I", "J"]

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

        self.create_frames()
        self.fill_frames()

        self.check_identifier_wrapper = (self.root.register(self.check_identifier), '%P', '%d', '%i')
        self.check_number_wrapper = (self.root.register(self.check_num), '%P')
        self.check_string_wrapper = (self.root.register(self.check_string), '%P')
        self.check_value_wrapper = (self.root.register(self.check_value), '%P')

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
        for i in range(10):
            btn = Button(self.elements_frame, text=texto[i], command=lambda i=i: self.canvas_mode(texto[i]))
            btn.grid(row=i, column=0, sticky="ew")
            self.elements_frame.rowconfigure(i, weight=1)

        self.canvas.bind("<Button-1>", lambda e: self.on_click(e))
    
    def canvas_mode(self, text):
        self.selection_mode = text == "Cursor"
        self.current_element = text
        print(self.current_element)    

    def on_click(self, e):
        if self.selection_mode:
            return
        else:
            tag = f"shape{len(self.shapes)}"
            tag_text = f"{tag}_text"
            if self.current_element == "Ovalo":
                shape = self.canvas.create_oval(e.x-25, e.y-25, e.x + 25, e.y + 25, fill="blue", tags=tag)
            elif self.current_element == "Rectangulo":
                shape = self.canvas.create_rectangle(e.x-25, e.y-25, e.x + 25, e.y + 25, fill="green", tags=tag)    
            
            self.shapes.append(shape) 
            self.canvas.tag_bind(shape, "<Double-Button-1>", lambda e: self.shape_addText( tag_text))
            self.canvas.tag_bind(shape, "<Button-1>", lambda e: self.canvas.itemconfig(shape, fill="red"))
            x1, y1, x2, y2 = self.canvas.coords(shape)
            text = self.canvas.create_text((x2+x1)/2, (y2+y1)/2, text="", fill="black", tags=tag_text)
            self.canvas.lift(text, shape)
            self.texts.append(text)

    def shape_addText(self, tag):
        self.canvas.itemconfig(tag, text=self.assign_dlg()) 
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
    
    def check_value(self, newval):
        # Check if the new value matches the pattern
        return re.fullmatch("[^?!\n]*", newval) is not None

    def declare_dlg(self):

        def dismiss():
            dlg.grab_release()
            dlg.destroy()

        dlg = Toplevel(self.root)

        typeVar = StringVar()
        commboType = ttk.Combobox(dlg, textvariable=typeVar, values=["int", "float", "char", "double"], state="readonly")
        commboType.grid(row=0, column=0, sticky="ew")
        commboType.focus_set()

        idVar = StringVar()
        txtid = ttk.Entry(dlg, textvariable=idVar, validate='key', validatecommand=self.check_identifier_wrapper)
        txtid.grid(row=0, column=1, sticky="ew")
        txtid.bind("<Return>", lambda e: dismiss())

        return typeVar.get() + " " + idVar.get() + ";"


        dlg.protocol("WM_DELETE_WINDOW",  dismiss)
        dlg.transient(root)

    def assign_dlg(self):
        sentence = ""
        def dismiss():
            dlg.grab_release()
            dlg.destroy()

        dlg = Toplevel(self.root)

        typeVar = StringVar()
        commboType = ttk.Combobox(dlg, textvariable=typeVar, values=["int", "float", "char", "double"], state="readonly")
        commboType.grid(row=0, column=0, sticky="ew")
        commboType.focus_set()


        lbl = ttk.Label(dlg, text=" = ")
        lbl.grid(row=0, column=2, sticky="ew")

        idVar = StringVar()
        txtid = ttk.Entry(dlg, textvariable=idVar, validate='key', validatecommand=self.check_identifier_wrapper)
        txtid.grid(row=0, column=1, sticky="ew")

        valVar = StringVar()
        txtval = ttk.Entry(dlg, textvariable=valVar, validate='key', validatecommand=self.check_value_wrapper)
        txtval.grid(row=0, column=3, sticky="ew")
        txtval.bind("<Return>", lambda e: dismiss())

        dlg.protocol("WM_DELETE_WINDOW",  dismiss)
        dlg.transient(root)   # dialog window is related to main
        dlg.wait_visibility() # can't grab until window appears, so we wait
        dlg.grab_set()        # ensure all input goes to our window
        dlg.wait_window()     # block until window is destroyed

        return typeVar.get() + " " + idVar.get() + " = " + valVar.get() + ";"



if __name__ == "__main__":
    root = Tk()
    app = Window(root)
    root.mainloop()