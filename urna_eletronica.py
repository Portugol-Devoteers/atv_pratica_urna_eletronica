from tkinter import *
from tkinter import ttk

class UrnaEletronica:
    def __init__(self, root):
        self.root = root
        self.root.title("Urna Eletrônica")
        self.frm = ttk.Frame(self.root, padding=60)
        self.frm.grid()

        self.style = ttk.Style()
        self.configura_style()
        self.cria_interface()


    def configura_style(self):
        self.style.configure("Black.TButton", background="black", foreground="white")
        self.style.configure("White.TButton", background="white", foreground="black")
        self.style.configure("Red.TButton", background="red", foreground="black")
        self.style.configure("Green.TButton", background="green", foreground="black")

    def cria_interface(self):
        ttk.Label(self.frm, text="JUSTIÇA ELEITORAL").grid(row=0, column=0, columnspan=4, pady=(0, 10))
        ttk.Label(self.frm).grid(row=1, column=0, columnspan=4)

        botoes_num = [
            ("1", 1, 0), ("2", 2, 0), ("3", 3, 0),
            ("4", 1, 1), ("5", 2, 1), ("6", 3, 1),
            ("7", 1, 2), ("8", 2, 2), ("9", 3, 2),
            ("0", 2, 3)
        ]

        for(nrs, coluna, lin) in botoes_num:
            self.criar_botao(text=nrs, estilo="Black.TButton", col=coluna, row=lin)

        self.criar_botao(text="BRANCO", estilo="White.TButton", col=1, row=4, comando=self.apertou_branco)
        self.criar_botao(text="CORRIGE", estilo="Red.TButton", col=2, row=4, comando=self.apertou_corrige)
        self.criar_botao(text="CONFIRMA", estilo="Green.TButton", col=3, row=4, comando=self.apertou_confirma)

    def criar_botao(self, text, estilo, col, row, comando=None):
        comando = comando if comando else lambda: self.apertou_numero(text)
        ttk.Button(self.frm, text=text, style=estilo, command=comando).grid(column=col, row=row)

    def apertou_numero(self, numero):
        print(f'Apertou {numero}')

    def apertou_branco(self):
        print('Apertou BRANCO')

    def apertou_corrige(self):
        print('Apertou CORRIGE')

    def apertou_confirma(self):
        print('Apertou CONFIRMA')