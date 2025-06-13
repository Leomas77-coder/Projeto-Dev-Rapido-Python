import customtkinter as ctk
from PIL import Image, ImageTk

# Tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Funções de navegação
def abrir_mapa():
    import mapa_interativo2

def abrir_grafico():
    import grafico_completo

def abrir_tabelas():
    import tabelas

# Compatibilidade com versões do Pillow
try:
    resample = Image.Resampling.LANCZOS
except:
    resample = Image.LANCZOS

# Redimensionar imagem ao alterar janela
def redimensionar_imagem(event):
    largura = event.width // 2
    altura = event.height - 40
    imagem = imagem_original.resize((largura, altura), resample)
    app.imagem_tk = ImageTk.PhotoImage(imagem)
    label_imagem.configure(image=app.imagem_tk)

# Janela principal
app = ctk.CTk()
app.title("Tuberculose Global - Overview")
app.geometry("900x600")
app.minsize(700, 500)

# Frame principal com grid
frame_principal = ctk.CTkFrame(app)
frame_principal.pack(expand=True, fill="both", padx=0, pady=0)

frame_principal.columnconfigure(0, weight=1)
frame_principal.columnconfigure(1, weight=1)
frame_principal.rowconfigure(0, weight=1)

# Frame de conteúdo (painel de botões)
frame_conteudo = ctk.CTkFrame(frame_principal)
frame_conteudo.grid(row=0, column=0, sticky="nsew", padx=(20, 5), pady=20)
frame_conteudo.columnconfigure(0, weight=1)

# Título
titulo = ctk.CTkLabel(frame_conteudo, text="Painel Geral de Acesso", font=ctk.CTkFont(size=22, weight="bold"))
titulo.pack(pady=(10, 20), padx=10)

# Botões
botao_mapa = ctk.CTkButton(frame_conteudo, text="📊 Mapa Interativo", command=abrir_mapa)
botao_mapa.pack(pady=10, fill="x", padx=10)

botao_grafico = ctk.CTkButton(frame_conteudo, text="📈 Gráfico Completo", command=abrir_grafico)
botao_grafico.pack(pady=10, fill="x", padx=10)

botao_tabelas = ctk.CTkButton(frame_conteudo, text="📑 Tabela Tuberculose", command=abrir_tabelas)
botao_tabelas.pack(pady=10, fill="x", padx=10)

botao_sair = ctk.CTkButton(frame_conteudo, text="❌ Sair", command=app.destroy,
                           fg_color="red", hover_color="#aa0000")
botao_sair.pack(pady=10, fill="x", padx=10)

# Imagem à direita
imagem_original = Image.open("img/imagem_medico.png")
label_imagem = ctk.CTkLabel(frame_principal, text="")
label_imagem.grid(row=0, column=1, sticky="nsew", padx=(5, 20), pady=20)

# Redimensionar imagem dinamicamente
frame_principal.bind("<Configure>", redimensionar_imagem)

# Executar
app.mainloop()