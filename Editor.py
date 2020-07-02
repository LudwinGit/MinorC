import tkinter as tk
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result   

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class ContenedorEditor(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        # self.text.config(font=("Consolas",12))
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

        # self.text.insert("end", "one\ntwo\nthree\n")
        # self.text.insert("end", "main\n",("bigfont",))
        # self.text.insert("end", "five\n")

    def _on_change(self, event):
        self.linenumbers.redraw()
        self.colorearTexto()

    def colorearTexto(self):
        self.text.tag_add("BOLD", "1.0", "end-1c")        
        t = self.text.get(1.0,'end-1c')
        lineas = t.split('\n')

        reservadas = ['main','goto' ,'unset','print','read' ,'exit' ,'int'  ,'float','char' ,'abs',
                        'array','if'   ]

        palabra = ""
        l =0
        for linea in lineas:
            l += 1
            columna = 0
            linea = linea+" " #Agregamos un espacio para que reconozca la ultima palabra si no hay salto
            while columna < len(linea):
                if 96 < ord(linea[columna]) < 123 :
                    palabra+=linea[columna]
                elif ord(linea[columna]) == 35:
                    index1 = str(l)+"."+str(columna)
                    index2 = str(l)+"."+str(len(linea))
                    self.text.tag_add("comentario", index1, index2)
                    self.text.tag_config("comentario", foreground="#849699")
                    palabra =""
                    columna = len(linea)
                elif ord(linea[columna]) == 36:
                    index1 = str(l)+"."+str(columna)
                    index2 = str(l)+"."+str(columna+1)
                    self.text.tag_add("variable", index1, index2)
                    self.text.tag_config("variable", foreground="#F00019")
                else:
                    if palabra in reservadas:
                        index1 = str(l)+"."+str(columna-len(palabra))
                        index2 = str(l)+"."+str(columna)
                        self.text.tag_add("reservada", index1, index2)
                        # self.text.tag_config("reservada", background="#696962", foreground="#01087C")
                        self.text.tag_config("reservada", foreground="#003B74")
                    palabra = ""
                columna += 1

    def MarcarLinea(self,linea,linea_anterior):
        self.text.tag_add("debug",str(float(linea)),str(float(linea+1)))
        self.text.tag_config("debug",foreground="#fff",background="#003B74")
        self.text.tag_remove("debug",str(float(linea_anterior)),str(float(linea_anterior+1)))
        # self.text.tag_config("resetear",foreground="#000",background="#fff")
        self.colorearTexto()

    def Editor(self):
        return self.text