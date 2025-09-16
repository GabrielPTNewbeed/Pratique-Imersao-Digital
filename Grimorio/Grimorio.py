import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import json
import os
import sys 
import random
from tkinter import filedialog
from PIL import Image, ImageTk

# ---------------- Caminho do arquivo ----------------
def resource_path(relative_path):
    """ Pega o caminho correto para arquivos no .py e no .exe """
    try:
        base_path = sys._MEIPASS  # PyInstaller cria uma pasta temporária
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ARQUIVO = resource_path("grimorio.json")

# ---------------- Utilidades ----------------
def carregar_grimorio():
    try:
        if os.path.exists(ARQUIVO):
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar grimório: {e}")
        return {}  # SEMPRE retorna um dicionário, nunca None

def salvar_grimorio(grimorio):
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(grimorio, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar grimório: {e}")

def mostrar_feiticos(ordenar_por="nome"):
    lista.delete(0, tk.END)

    # transforma em lista para ordenar
    feiticos = list(grimorio.items())
    
    if ordenar_por == "nome":
        # ordena pelo nome do feitiço (case-insensitive)
        feiticos.sort(key=lambda x: x[0].lower())
    elif ordenar_por == "nível":
        # ordena pelo nível, convertendo para inteiro (se vazio vira 0)
        feiticos.sort(key=lambda x: int(x[1].get("nível", 0)) if str(x[1].get("nível", "0")).isdigit() else 0)

    # insere na lista
    for nome, d in feiticos:
        lista.insert(tk.END, f"{nome} (Nível {d['nível']} • {d['escola']})")

def pedir_campo(titulo, prompt, valor=""):
    """Função auxiliar para pedir entradas de texto"""
    return simpledialog.askstring(titulo, prompt, initialvalue=valor) or valor

# ---------------- Operações ----------------
def adicionar():
    nome = pedir_campo("Novo Feitiço", "Nome do feitiço:")
    if not nome:
        return
    if nome in grimorio and not messagebox.askyesno("Aviso", f"'{nome}' já existe. Deseja sobrescrever?"):
        return
    
    grimorio[nome] = {
        "nível": pedir_campo("Nível", "Nível do feitiço:", grimorio[nome]["nível"] if nome in grimorio else ""),
        "escola": pedir_campo("Escola", "Escola de magia:", grimorio[nome]["escola"] if nome in grimorio else ""),
        "tempo": pedir_campo("Tempo", "Tempo de conjuração:", grimorio[nome]["tempo"] if nome in grimorio else ""),
        "alcance": pedir_campo("Alcance", "Alcance:", grimorio[nome]["alcance"] if nome in grimorio else ""),
        "componentes": pedir_campo("Componentes", "Componentes:", grimorio[nome]["componentes"] if nome in grimorio else ""),
        "duração": pedir_campo("Duração", "Duração:", grimorio[nome]["duração"] if nome in grimorio else ""),
        "descrição": pedir_campo("Descrição", "Descrição do feitiço:", grimorio[nome]["descrição"] if nome in grimorio else ""),
    }
    salvar_grimorio(grimorio)
    mostrar_feiticos()
    messagebox.showinfo("Sucesso", f"O feitiço '{nome}' foi adicionado!")
    atualizar_status()

def editar():
    selecao = lista.curselection()
    if not selecao:
        messagebox.showwarning("Aviso", "Selecione um feitiço para editar!")
        return
    nome = lista.get(selecao[0]).split(" (")[0]
    d = grimorio[nome]

    grimorio[nome] = {
        "nível": pedir_campo("Editar", "Nível:", d["nível"]),
        "escola": pedir_campo("Editar", "Escola:", d["escola"]),
        "tempo": pedir_campo("Editar", "Tempo:", d["tempo"]),
        "alcance": pedir_campo("Editar", "Alcance:", d["alcance"]),
        "componentes": pedir_campo("Editar", "Componentes:", d["componentes"]),
        "duração": pedir_campo("Editar", "Duração:", d["duração"]),
        "descrição": pedir_campo("Editar", "Descrição:", d["descrição"]),
    }
    salvar_grimorio(grimorio)
    mostrar_feiticos()
    messagebox.showinfo("Sucesso", f"O feitiço '{nome}' foi atualizado!")

def remover():
    selecao = lista.curselection()
    if not selecao:
        messagebox.showwarning("Aviso", "Selecione um feitiço para remover!")
        return
    nome = lista.get(selecao[0]).split(" (")[0]
    if messagebox.askyesno("Confirmação", f"Remover '{nome}' do grimório?"):
        del grimorio[nome]
        salvar_grimorio(grimorio)
        mostrar_feiticos()
        messagebox.showinfo("Sucesso", f"'{nome}' removido!")
        atualizar_status()

def consultar():
    selecao = lista.curselection()
    if not selecao:
        messagebox.showwarning("Aviso", "Selecione um feitiço na lista!")
        return
    nome = lista.get(selecao[0]).split(" (")[0]
    d = grimorio[nome]
    
    # Criar uma nova janela para mostrar os detalhes
    detalhes_janela = tk.Toplevel(root)
    detalhes_janela.title(f"Detalhes: {nome}")
    detalhes_janela.geometry("600x500")
    detalhes_janela.resizable(True, True)
    
    # Frame principal com scroll
    main_frame = tk.Frame(detalhes_janela)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Texto com scroll
    texto_frame = tk.Frame(main_frame)
    texto_frame.pack(fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(texto_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    texto = tk.Text(texto_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, padx=10, pady=10)
    texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=texto.yview)
    
    # Inserir conteúdo
    conteudo = (
        f"Nome: {nome}\n\n"
        f"Nível: {d['nível']}\n"
        f"Escola: {d['escola']}\n"
        f"Tempo: {d['tempo']}\n"
        f"Alcance: {d['alcance']}\n"
        f"Componentes: {d['componentes']}\n"
        f"Duração: {d['duração']}\n\n"
        f"Descrição:\n{d['descrição']}"
    )
    
    texto.insert(tk.END, conteudo)
    texto.config(state=tk.DISABLED)  # Tornar o texto somente leitura
    
    # Botão de fechar
    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(fill=tk.X, pady=5)
    
    tk.Button(btn_frame, text="Fechar", command=detalhes_janela.destroy).pack()

def listar():
    mostrar_feiticos()

def filtrar():
    escola = simpledialog.askstring("Filtro", "Digite a escola de magia:")
    if not escola:
        return
    lista.delete(0, tk.END)
    encontrados = {n:d for n,d in grimorio.items() if escola.lower() in d['escola'].lower()}
    if not encontrados:
        messagebox.showinfo("Resultado", f"Nenhum feitiço encontrado da escola '{escola}'.")
        mostrar_feiticos()
        return
    for nome, d in encontrados.items():
        lista.insert(tk.END, f"{nome} (Nível {d['nível']} • {d['escola']})")

def buscar():
    termo = simpledialog.askstring("Buscar", "Digite o nome do feitiço:")
    if not termo:
        return
    lista.delete(0, tk.END)
    encontrados = {n:d for n,d in grimorio.items() if termo.lower() in n.lower()}
    if not encontrados:
        messagebox.showinfo("Resultado", f"Nenhum feitiço encontrado com '{termo}'.")
        mostrar_feiticos()
        return
    for nome, d in encontrados.items():
        lista.insert(tk.END, f"{nome} (Nível {d['nível']} • {d['escola']})")

def sair():
    if messagebox.askyesno("Sair", "Tem certeza que deseja sair?"):
        root.destroy()

def caixa_de_pandora():
    if not grimorio:
        messagebox.showwarning("Aviso", "Não há feitiços no grimório ainda!")
        return
    
    nomes = list(grimorio.keys())
    campos = ["nível", "escola", "tempo", "alcance", "componentes", "duração", "descrição"]

    # Sorteia um nome para o "novo feitiço" + " Caótico"
    nome_base = random.choice(nomes)
    nome_novo = nome_base + " Caótico"

    # Cria a versão caótica
    feitico_caotico = {}
    for campo in campos:
        feitico_caotico[campo] = grimorio[random.choice(nomes)][campo]

    # Salva no grimório
    grimorio[nome_novo] = feitico_caotico
    salvar_grimorio(grimorio)
    mostrar_feiticos()

    # Exibe em uma nova janela
    detalhes_janela = tk.Toplevel(root)
    detalhes_janela.title("🌀 Feitiço da Caixa de Pandora")
    detalhes_janela.geometry("500x400")
    
    texto = scrolledtext.ScrolledText(detalhes_janela, wrap=tk.WORD, width=60, height=20)
    texto.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    detalhes = (
        f"{nome_novo}\n\n"
        f"Nível: {feitico_caotico['nível']}\n"
        f"Escola: {feitico_caotico['escola']}\n"
        f"Tempo: {feitico_caotico['tempo']}\n"
        f"Alcance: {feitico_caotico['alcance']}\n"
        f"Componentes: {feitico_caotico['componentes']}\n"
        f"Duração: {feitico_caotico['duração']}\n\n"
        f"Descrição:\n{feitico_caotico['descrição']}"
    )
    
    texto.insert(tk.END, detalhes)
    texto.config(state=tk.DISABLED)
    
    tk.Button(detalhes_janela, text="Fechar", command=detalhes_janela.destroy).pack(pady=5)
    atualizar_status()

def exportar_feiticos_txt():
    caminho = filedialog.asksaveasfilename(
        title="Exportar feitiços",
        defaultextension=".txt",
        filetypes=[("Arquivos de texto", "*.txt")]
    )
    if not caminho:
        return

    try:
        with open(caminho, "w", encoding="utf-8") as f:
            for nome, d in grimorio.items():
                linha = f"{nome};{d['nível']};{d['escola']};{d['tempo']};{d['alcance']};{d['componentes']};{d['duração']};{d['descrição']}\n"
                f.write(linha)

        messagebox.showinfo("Sucesso", f"Feitiços exportados para:\n{caminho}")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível exportar:\n{e}")

def importar_feiticos_txt():
    caminho = filedialog.askopenfilename(
        title="Importar lista de feitiços",
        filetypes=[("Arquivos de texto", "*.txt")]
    )
    if not caminho:
        return

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        adicionados = 0
        ignorados = 0
        atualizados = 0

        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue

            partes = linha.split(";")  # formato esperado: nome;nível;escola;tempo;alcance;componentes;duração;descrição
            if len(partes) < 3:
                continue  # ignora linhas inválidas

            nome = partes[0]
            nivel = partes[1] if len(partes) > 1 else ""
            escola = partes[2] if len(partes) > 2 else ""

            if nome in grimorio:  # já existe → pergunta se quer atualizar
                if messagebox.askyesno("Feitiço Existente", f"O feitiço '{nome}' já existe. Deseja atualizá-lo?"):
                    grimorio[nome] = {
                        "nível": nivel,
                        "escola": escola,
                        "tempo": partes[3] if len(partes) > 3 else "",
                        "alcance": partes[4] if len(partes) > 4 else "",
                        "componentes": partes[5] if len(partes) > 5 else "",
                        "duração": partes[6] if len(partes) > 6 else "",
                        "descrição": partes[7] if len(partes) > 7 else "",
                    }
                    atualizados += 1
                else:
                    ignorados += 1
                continue

            grimorio[nome] = {
                "nível": nivel,
                "escola": escola,
                "tempo": partes[3] if len(partes) > 3 else "",
                "alcance": partes[4] if len(partes) > 4 else "",
                "componentes": partes[5] if len(partes) > 5 else "",
                "duração": partes[6] if len(partes) > 6 else "",
                "descrição": partes[7] if len(partes) > 7 else "",
            }

            adicionados += 1

        salvar_grimorio(grimorio)
        listar()  # atualiza a lista na tela

        messagebox.showinfo(
            "Importação concluída",
            f"Foram adicionados {adicionados} novos feitiços.\n"
            f"Foram atualizados {atualizados} feitiços.\n"
            f"Foram ignorados {ignorados} feitiços."
        )
        atualizar_status()

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível importar feitiços:\n{e}")

def sobre():
    messagebox.showinfo("Sobre", "Grimório Mágico\n\nUm aplicativo para gerenciar seus feitiços de RPG!\n\nDesenvolvido com Python e Tkinter.")

def atualizar_status():
    status_bar.config(text=f"Total de feitiços: {len(grimorio)}")

# ---------------- Interface ----------------
root = tk.Tk()
root.title("📜 Grimório Mágico")

# CARREGAR O GRIMÓRIO ANTES DE CRIAR A INTERFACE
grimorio = carregar_grimorio()

# ---------- Configuração da Janela ----------
largura, altura = 800, 600  # tamanho inicial
root.geometry(f"{largura}x{altura}")  # janela abre no tamanho certo
root.minsize(600, 400)  # tamanho mínimo, evita distorcer muito

# Tentar carregar a imagem de fundo, usar cor sólida se não encontrar
try:
    imagem_original = Image.open(resource_path("pergaminho.png"))
    bg_imagem = ImageTk.PhotoImage(imagem_original.resize((largura, altura), Image.LANCZOS))

    fundo_label = tk.Label(root, image=bg_imagem)
    fundo_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Atualiza o fundo quando redimensionar a janela
    def redimensionar_fundo(event):
        nova_imagem = imagem_original.resize((event.width, event.height), Image.LANCZOS)
        novo_bg = ImageTk.PhotoImage(nova_imagem)
        fundo_label.config(image=novo_bg)
        fundo_label.image = novo_bg  # evitar garbage collector

    root.bind("<Configure>", redimensionar_fundo)
except:
    # Se não conseguir carregar a imagem, usar uma cor de fundo
    root.configure(bg="#2E2E3A")

# ---------- Conteúdo ----------
conteudo = tk.Frame(root, bg="", padx=10, pady=10)
conteudo.place(relx=0.5, rely=0.5, anchor="center")  # centralizado

# Frame para a lista e scrollbar
lista_frame = tk.Frame(conteudo)
lista_frame.pack(pady=10)

# Lista de feitiços com scrollbar
scrollbar = tk.Scrollbar(lista_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista = tk.Listbox(
    lista_frame,
    width=60,
    height=15,
    bg="#1E1E2F",
    fg="white",
    selectbackground="#6A0DAD",
    yscrollcommand=scrollbar.set
)
lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=lista.yview)

# Frame para os botões
botoes_frame = tk.Frame(conteudo)
botoes_frame.pack(pady=10)

# Botões principais
botoes = [
    ("Adicionar", adicionar),
    ("Editar", editar),
    ("Remover", remover),
    ("Consultar", consultar),
    ("Listar Todos", listar),
    ("Filtrar por Escola", filtrar),
    ("Buscar", buscar),
    ("Ordenar por Nome", lambda: mostrar_feiticos("nome")),
    ("Ordenar por Nível", lambda: mostrar_feiticos("nível")),                       
    ("Sair", sair)
]

# Organizar botões em duas colunas
for i, (texto, cmd) in enumerate(botoes):
    btn = tk.Button(botoes_frame, text=texto, width=15, command=cmd)
    btn.grid(row=i//2, column=i%2, padx=5, pady=2)

# Botão especial "Caixa de Pandora"
pandora_btn = tk.Button(root, text="🎭 Caixa de Pandora", command=caixa_de_pandora,
                        bg="#6A0DAD", fg="white", font=("Arial", 10, "bold"))
pandora_btn.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

# Menu
menu = tk.Menu(root)
root.config(menu=menu)

# Menu Arquivo
arquivo_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Feitiços", menu=arquivo_menu)
arquivo_menu.add_command(label="Adicionar", command=adicionar)
arquivo_menu.add_command(label="Editar", command=editar)
arquivo_menu.add_command(label="Remover", command=remover)
arquivo_menu.add_command(label="Consultar", command=consultar)
arquivo_menu.add_separator()
arquivo_menu.add_command(label="Importar", command=importar_feiticos_txt)
arquivo_menu.add_command(label="Exportar", command=exportar_feiticos_txt)
arquivo_menu.add_separator()
arquivo_menu.add_command(label="Sair", command=sair)

# Menu Exibir
exibir_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Exibir", menu=exibir_menu)
exibir_menu.add_command(label="Listar Todos", command=listar)
exibir_menu.add_command(label="Filtrar por Escola", command=filtrar)
exibir_menu.add_command(label="Buscar", command=buscar)
exibir_menu.add_separator()
exibir_menu.add_command(label="Ordenar por Nome", command=lambda: mostrar_feiticos("nome"))
exibir_menu.add_command(label="Ordenar por Nível", command=lambda: mostrar_feiticos("nível"))

# Menu Ajuda
ajuda_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Ajuda", menu=ajuda_menu)
ajuda_menu.add_command(label="Sobre", command=sobre)

# Status bar - AGORA COM VERIFICAÇÃO DE SEGURANÇA
status_bar = tk.Label(root, text=f"Total de feitiços: {len(grimorio) if grimorio else 0}", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Iniciar
mostrar_feiticos("nome")
root.mainloop()