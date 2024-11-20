import pickle
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

class UrnaEletronica:
    def __init__(self, root):
        self.root = root
        self.root.title("Urna Eletrônica")
        self.frm = ttk.Frame(self.root, padding=20)
        self.frm.grid()

        self.style = ttk.Style()
        self.configura_style()
        
        self.titulos_usados = set()
        self.resultados = {"BRANCO": 0, "NULO": 0}

        self.candidatos = self.carregar_candidatos()

        for numero, candidato in self.candidatos.items():
            self.resultados[f"{candidato["nome"]} ({candidato["partido"]})"] = 0
        
        self.numero_digitado = ""  

        self.solicitar_titulo()

    def configura_style(self):
        self.style.configure("Black.TButton", background="black", foreground="black", font=("Arial", 12))
        self.style.configure("White.TButton", background="white", foreground="black", font=("Arial", 12))
        self.style.configure("Red.TButton", background="red", foreground="black", font=("Arial", 12))
        self.style.configure("Green.TButton", background="green", foreground="black", font=("Arial", 12))


    def carregar_candidatos(self):
        try:
            with open("candidatos.pkl", "rb") as arquivo:
                return pickle.load(arquivo)
        except FileNotFoundError:
            print("Arquivo 'candidatos.pkl' não encontrado.")
            return {}

    def solicitar_titulo(self):
        while True:
            titulo = simpledialog.askstring("Título de Eleitor", "Digite seu título de eleitor:")
            if not titulo:
                print("Título de eleitor não informado. Encerrando urna...")
                self.salvar_votos_em_txt()
                quit()
            if self.validar_titulo(titulo):
                if titulo in self.titulos_usados:
                    self.exibir_mensagem("Este título já votou!")
                else:
                    print(f"Título válido e autorizado: {titulo}")
                    self.titulos_usados.add(titulo)
                    self.cria_interface()  # Continuar para criar a interface
                    break
            else:
                self.exibir_mensagem("Título inválido! Tente novamente.")

    def validar_titulo(self, titulo):
        return titulo.isdigit()

    def exibir_mensagem(self, mensagem):
        top = Toplevel(self.root)
        top.title("Mensagem")
        Label(top, text=mensagem, padx=20, pady=10).pack()
        Button(top, text="OK", command=top.destroy).pack(pady=10)

    def cria_interface(self):
        # Parte esquerda: Teclado numérico
        teclado_frame = ttk.Frame(self.frm)
        teclado_frame.grid(row=0, column=0, padx=10)

        ttk.Label(teclado_frame, text="JUSTIÇA ELEITORAL").grid(row=0, column=0, columnspan=4, pady=(0, 10))
        botoes_num = [
            ("1", 1, 0), ("2", 2, 0), ("3", 3, 0),
            ("4", 1, 1), ("5", 2, 1), ("6", 3, 1),
            ("7", 1, 2), ("8", 2, 2), ("9", 3, 2),
            ("0", 2, 3)
        ]

        for (nrs, coluna, lin) in botoes_num:
            self.criar_botao(teclado_frame, text=nrs, estilo="Black.TButton", col=coluna, row=lin)

        self.criar_botao(teclado_frame, text="BRANCO", estilo="White.TButton", col=1, row=4, comando=self.apertou_branco)
        self.criar_botao(teclado_frame, text="CORRIGE", estilo="Red.TButton", col=2, row=4, comando=self.apertou_corrige)
        self.criar_botao(teclado_frame, text="CONFIRMA", estilo="Green.TButton", col=3, row=4, comando=self.apertou_confirma)

        # Parte direita: Tela para exibir informações do candidato
        self.tela_frame = ttk.Frame(self.frm, relief="ridge", padding=10)
        self.tela_frame.grid(row=0, column=1, padx=10, sticky="nsew")
        self.atualizar_tela()

    def criar_botao(self, parent, text, estilo, col, row, comando=None):
        comando = comando if comando else lambda: self.apertou_numero(text)
        ttk.Button(parent, text=text, style=estilo, command=comando).grid(column=col, row=row)

    def atualizar_tela(self):
        for widget in self.tela_frame.winfo_children():
            widget.destroy()

        # Exibir informações do candidato ou voto branco
        if self.numero_digitado == "BRANCO":
            ttk.Label(self.tela_frame, text="Votar Branco", font=("Arial", 16), foreground="blue").grid(row=0, column=0, pady=10)
        elif self.numero_digitado in self.candidatos:
            candidato = self.candidatos[self.numero_digitado]
            ttk.Label(self.tela_frame, text=f"Candidato: {candidato['nome']}", font=("Arial", 16)).grid(row=0, column=0, pady=10)
            ttk.Label(self.tela_frame, text=f"Partido: {candidato['partido']}", font=("Arial", 14)).grid(row=1, column=0, pady=5)
        elif self.numero_digitado:
            ttk.Label(self.tela_frame, text="Número inválido! Votará nulo.", font=("Arial", 16), foreground="red").grid(row=0, column=0, pady=10)
        else:
            ttk.Label(self.tela_frame, text="Digite o número do candidato.", font=("Arial", 14)).grid(row=0, column=0, pady=10)

    def apertou_numero(self, numero):
        self.numero_digitado += numero
        self.atualizar_tela()

    def apertou_branco(self):
        self.numero_digitado = "BRANCO"
        self.atualizar_tela()

    def apertou_corrige(self):
        self.numero_digitado = ""
        self.atualizar_tela()
        print('Corrigindo...')

    def apertou_confirma(self):
        if self.numero_digitado == "BRANCO":
            print("Voto em BRANCO confirmado!")
            self.resultados["BRANCO"] += 1
        elif self.numero_digitado in self.candidatos:
            candidato = self.candidatos[self.numero_digitado]
            print(f"Voto confirmado: {candidato['nome']}")
            self.resultados[f"{candidato["nome"]} ({candidato["partido"]})"] += 1
        else:
            print("Voto NULO!")
            self.resultados["NULO"] += 1

        self.numero_digitado = ""
        self.atualizar_tela()
        self.solicitar_titulo()

    def salvar_votos_em_txt(self):
        with open("resultado_votacao.txt", "w") as arquivo:
            for key, value in self.resultados.items():
                arquivo.write(f"{key}: {value}\n")
        print("Resultados salvos no arquivo 'resultado_votacao.txt'.")

