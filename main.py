import tkinter as tk
from urna_eletronica import *

if __name__ == '__main__':
    root = tk.Tk()
    urna = UrnaEletronica(root)
    def ao_fechar():
        urna.salvar_votos_em_pkl()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", ao_fechar)
    root.mainloop()
