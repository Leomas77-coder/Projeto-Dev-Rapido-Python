import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from collections import defaultdict
import csv
import subprocess
import sys

# Configuração inicial
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Dicionários de tradução e filtros
nomes_em_portugues = {
    "Country": "País",
    "Region": "Continente",
    "Year": "Ano",
    "TB_Cases": "Casos de TB",
    "TB_Deaths": "Mortes por TB",
    "TB_Incidence_Rate": "Taxa de incidência (%)",
    "TB_Mortality_Rate": "Taxa de Mortalidade (%)",
    "TB_Treatment_Success_Rate": "Taxa de Sucesso de tratamento(%)"
}

continentes_corretos = {
    'Brazil': 'América do Sul',
    'China': 'Ásia',
    'South Africa': 'África',
    'USA': 'América do Norte',
    'Russia': 'Europa'
}

colunas_desejadas = list(nomes_em_portugues.keys())

paises_filtrados = {
    'Brazil': 'Brasil',
    'USA': 'Estados Unidos',
    'South Africa': 'África do Sul',
    'Russia': 'Rússia',
    'China': 'China'
}

# Funções principais
def carregar_dados_csv(caminho_arquivo, colunas_desejadas, coluna_ordenacao):
    with open(caminho_arquivo, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        agrupados = defaultdict(lambda: [0] * len(colunas_desejadas))
        for linha in leitor:
            pais = linha.get("Country")
            if pais in paises_filtrados:
                try:
                    linha["Region"] = continentes_corretos.get(pais, linha.get("Region"))
                    linha["Country"] = paises_filtrados[pais]
                    chave = (linha["Country"], linha["Year"])

                    linha_formatada = []
                    for col in colunas_desejadas:
                        valor = linha[col]
                        if col in ["Country", "Region", "Year"]:
                            linha_formatada.append(valor)
                        else:
                            try:
                                valor_float = float(valor)
                                if col in ["TB_Cases", "TB_Deaths"]:
                                    linha_formatada.append(int(round(valor_float)))
                                else:
                                    linha_formatada.append(round(valor_float, 2))
                            except ValueError:
                                linha_formatada.append(0 if col in ["TB_Cases", "TB_Deaths"] else 0.0)

                    if agrupados[chave][0] == 0:
                        agrupados[chave] = linha_formatada
                    else:
                        for i in range(len(colunas_desejadas)):
                            if colunas_desejadas[i] in ["Country", "Region", "Year"]:
                                continue
                            agrupados[chave][i] += linha_formatada[i]

                except KeyError:
                    continue

        dados_agrupados = list(agrupados.values())
        indice_ano = colunas_desejadas.index(coluna_ordenacao)
        return sorted(dados_agrupados, key=lambda x: int(x[indice_ano]), reverse=True)

def preencher_tabela(lista_dados):
    tree.delete(*tree.get_children())
    for linha in lista_dados:
        linha_formatada = []
        for i, valor in enumerate(linha):
            coluna = colunas_desejadas[i]
            if coluna in ["TB_Cases", "TB_Deaths"]:
                linha_formatada.append(str(int(round(valor))))
            elif coluna in ["TB_Incidence_Rate", "TB_Mortality_Rate", "TB_Treatment_Success_Rate"]:
                linha_formatada.append(f"{valor:.2f}")
            else:
                linha_formatada.append(valor)
        tree.insert("", "end", values=linha_formatada)

def filtrar_dados():
    termo_pais = entry_pais_var.get().strip().lower()
    termo_ano = entry_ano.get()
    filtrados = []
    for linha in dados:
        pais = linha[0].strip().lower()
        ano = linha[2].strip()
        if (termo_pais in pais if termo_pais else True) and (termo_ano == ano if termo_ano else True):
            filtrados.append(linha)
    preencher_tabela(filtrados)

def limpar_filtro():
    entry_pais_var.set('')
    entry_ano.set('')
    preencher_tabela(dados)

# Janela principal
root = ctk.CTk()
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", font=("Arial", 12))
style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#3ce298", foreground="black")
root.title("Dados de Tuberculose")
root.geometry("900x500")

def abrir_janela_crud():
    crud = ctk.CTkToplevel(root)
    crud.title("Gerenciar Dados")
    crud.geometry("1000x400")

    crud.transient(root)  
    crud.grab_set()       
    crud.focus()          

    frame_inputs = ctk.CTkFrame(crud)
    frame_inputs.pack(pady=10)

    labels = colunas_desejadas
    entries = {}

    for i, label in enumerate(labels):
        nome_pt = nomes_em_portugues.get(label, label)
        lbl = ctk.CTkLabel(frame_inputs, text=nome_pt)
        lbl.grid(row=0, column=i)
        entry = ctk.CTkEntry(frame_inputs, width=90)
        entry.grid(row=1, column=i, padx=2)
        entries[label] = entry

    tree_crud = ttk.Treeview(crud, columns=labels, show="headings", height=8)
    for col in labels:
        nome_pt = nomes_em_portugues.get(col, col)
        tree_crud.heading(col, text=nome_pt)
        tree_crud.column(col, width=90, anchor="center")
    tree_crud.pack(expand=True, fill="both", padx=10, pady=10)

    def adicionar():
        valores = [entries[col].get().strip().title() for col in labels]
        if all(valores):
            tree_crud.insert("", "end", values=valores)
            for entry in entries.values():
                entry.delete(0, ctk.END)
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

    def deletar():
        sel = tree_crud.selection()
        if sel:
            tree_crud.delete(sel)
        else:
            messagebox.showwarning("Aviso", "Selecione um item para deletar.")

    def editar():
        sel = tree_crud.selection()
        if sel:
            valores = [entries[col].get().strip().title() for col in labels]
            if all(valores):
                tree_crud.item(sel, values=valores)
                for entry in entries.values():
                    entry.delete(0, ctk.END)
            else:
                messagebox.showwarning("Aviso", "Preencha todos os campos.")
        else:
            messagebox.showwarning("Aviso", "Selecione um item para editar.")

    def carregar_para_edicao():
        sel = tree_crud.selection()
        if sel:
            valores = tree_crud.item(sel, "values")
            for i, col in enumerate(labels):
                entries[col].delete(0, ctk.END)
                entries[col].insert(0, valores[i])

    frame_botoes = ctk.CTkFrame(crud)
    frame_botoes.pack(pady=5)

    ctk.CTkButton(frame_botoes, text="Adicionar", command=adicionar).grid(row=0, column=0, padx=5)
    ctk.CTkButton(frame_botoes, text="Editar", command=editar).grid(row=0, column=1, padx=5)
    ctk.CTkButton(frame_botoes, text="Deletar", command=deletar).grid(row=0, column=2, padx=5)
    ctk.CTkButton(frame_botoes, text="Carregar Selecionado", command=carregar_para_edicao).grid(row=0, column=3, padx=5)

# Frame de busca
frame_busca = ctk.CTkFrame(root)
frame_busca.pack(pady=10)

def voltar_para_overview():
    root.destroy()
    subprocess.Popen([sys.executable, "overview.py"])

# Botão Voltar (na mesma linha da barra de pesquisa, à esquerda)
ctk.CTkButton(frame_busca, text="Voltar", command=voltar_para_overview, width=80).grid(row=0, column=0, padx=5)

# Filtros de busca
ctk.CTkLabel(frame_busca, text="País:").grid(row=0, column=1, padx=5)
entry_pais_var = ctk.StringVar()
entry_pais = ctk.CTkComboBox(frame_busca, width=200, values=list(paises_filtrados.values()), variable=entry_pais_var)
entry_pais.grid(row=0, column=2, padx=5)

ctk.CTkLabel(frame_busca, text="Ano:").grid(row=0, column=3, padx=5)
anos_disponiveis = sorted(list(set([linha[2] for linha in carregar_dados_csv("tuberculosis_Trends.csv", colunas_desejadas, "Year")])), reverse=True)
entry_ano = ctk.CTkComboBox(frame_busca, values=anos_disponiveis, width=80)
entry_ano.grid(row=0, column=4, padx=5)

# Botões de ação
ctk.CTkButton(frame_busca, text="Buscar", command=filtrar_dados).grid(row=0, column=5, padx=5)
ctk.CTkButton(frame_busca, text="Limpar", command=limpar_filtro).grid(row=0, column=6, padx=5)
ctk.CTkButton(frame_busca, text="Cadastrar/Editar", command=abrir_janela_crud).grid(row=0, column=7, padx=5)

# Tabela principal
tree = ttk.Treeview(root, columns=colunas_desejadas, show="headings", height=15)
tree.tag_configure("destaque", background="#3ce298", foreground="black") 

for col in colunas_desejadas:
    tree.heading(col, text=nomes_em_portugues.get(col, col))
    tree.column(col, anchor="center", width=90)
tree.pack(side="left", expand=True, fill="both", padx=10, pady=10)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Dados
dados = carregar_dados_csv("tuberculosis_Trends.csv", colunas_desejadas, "Year")
preencher_tabela(dados)

root.mainloop()