import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Criando a janela principal em tela cheia
root = ctk.CTk()
root.attributes('-fullscreen', True)
root.title("Dados da Tuberculose por Países")

# Função para voltar à página anterior
def voltar_pagina(event):
    root.destroy()

# Criando figura e eixos para os gráficos
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Taxas e Totalidades da Tuberculose dos 5 Países Durante 10 Anos", fontsize=16, fontweight="bold", color="black")

# Alterando o fundo da figura para azul claro
fig.patch.set_facecolor("#ADD8E6")

# Adicionando botão dentro do gráfico ao lado do título
botao_voltar = fig.text(0.03, 0.97, "← Voltar", fontsize=12, fontweight="bold", color="black",
                         bbox=dict(facecolor='#B0E0E6', alpha=0.6))

# Capturando cliques no botão
fig.canvas.mpl_connect("button_press_event", voltar_pagina)

# Criando gráficos
anos = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
dados_paises = {
    "Brasil": ([6.9, 7.1, 7.1, 6.3, 6.5, 6, 7.6, 6.7, 6.7, 7, 7], [72, 74, 74, 87, 71.9, 72, 68.4, 65.4, 69, 72, 75], "green"),
    "Rússia": ([35.8, 27.8, 28.8, 25.3, 33.4, 26.8, 15.6, 14.3, 14.3, 14.3, 14.2], [74, 74, 55, 71, 55, 76, 72, 74, 88, 75, 78], "blue"),
    "China": ([4.3, 4.2, 4.2, 4.2, 4, 4.1, 4.6, 4, 4.5, 4, 4], [93, 93, 93, 93, 93, 93, 92, 92, 88, 92, 90], "red"),
    "EUA": ([5.3, 5.3, 5.2, 5.2, 5, 5.1, 7.9, 7.8, 5.4, 5.2, 5.3], [95, 95, 95, 95, 95, 95, 94, 94, 94, 94, 94], "black"),
    "África do Sul": ([19.8, 20.2, 17.8, 19.9, 20.3, 20.3, 18.6, 18.6, 20.3, 20.3, 20.3], [75, 76, 76, 76, 77, 77, 77, 77, 77, 77, 77], "yellow"),
}

total_mortes = [158717, 152068, 143012, 125184, 119726, 108655, 115688, 107193, 104110, 104176, 101868]
total_casos = [1524065, 1479289, 1483474, 1347615, 1302928, 1234080, 1303920, 1280571, 1144395, 1243335, 1182080]

# Alterando o fundo dos gráficos
for ax in axes.flatten():
    ax.set_facecolor("#ADD8E6")

# Função para adicionar todas as linhas aos gráficos de taxa com maior visibilidade
def adicionar_linhas(ax, titulo, tipo):
    for pais, (dados_morte, dados_sucesso, cor) in dados_paises.items():
        dados = dados_morte if tipo == "morte" else dados_sucesso
        ax.plot(anos, dados, color=cor, marker="o", markersize=8, linestyle="-", linewidth=3, alpha=0.9)
    ax.set_xticks(anos)
    ax.set_xticklabels(anos, fontsize=10, color="black")
    ax.set_title(titulo, fontsize=14, fontweight="bold", color="black")
    ax.grid(ls="--", alpha=0.4)

# Adicionando gráficos de linha para taxas
adicionar_linhas(axes[0, 0], "Taxa de Morte", "morte")
adicionar_linhas(axes[0, 1], "Taxa de Sucesso", "sucesso")

# Gráficos de barras para totalidade de mortes e casos com bordas mais destacadas
axes[1, 0].bar(anos, total_mortes, color="gray", edgecolor="black", linewidth=2, alpha=0.8)
axes[1, 0].set_xticks(anos)
axes[1, 0].set_xticklabels(anos, fontsize=10, color="black")
axes[1, 0].set_title("Total de Mortes", fontsize=14, fontweight="bold", color="black")
axes[1, 0].grid(ls="--", alpha=0.4)

axes[1, 1].bar(anos, total_casos, color="orange", edgecolor="black", linewidth=2, alpha=0.8)
axes[1, 1].set_xticks(anos)
axes[1, 1].set_xticklabels(anos, fontsize=10, color="black")
axes[1, 1].set_title("Total de Casos", fontsize=14, fontweight="bold", color="black")
axes[1, 1].grid(ls="--", alpha=0.4)

# Criando legenda abaixo dos gráficos
legendas = [
    plt.Line2D([0], [0], color=cor, linewidth=3, label=pais) for pais, (_, _, cor) in dados_paises.items()
] + [
    plt.Line2D([0], [0], color="gray", linewidth=3, label="Mortes Totais"),
    plt.Line2D([0], [0], color="orange", linewidth=3, label="Casos Totais"),
]
fig.legend(handles=legendas, loc="lower center", fontsize=12, facecolor="white", edgecolor="black", framealpha=0.5, ncol=7)

# Integrando os gráficos com customtkinter para preencher a tela completamente
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Executando o aplicativo
root.mainloop()