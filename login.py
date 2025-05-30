import customtkinter as ctk
import json
import os

# - Aparência
ctk.set_appearance_mode("dark")

# Arquivo onde os dados serão salvos
ARQUIVO_USUARIOS = "usuarios.json"

# Função para carregar os usuários do arquivo
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r") as f:
            return json.load(f)
    return {}

# Função para salvar os usuários no arquivo
def salvar_usuarios():
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f)

# Carregar usuários ao iniciar
usuarios = carregar_usuarios()

# - Funções
def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()

    if usuario in usuarios and usuarios[usuario] == senha:
        resultado_login.configure(text="Login feito com sucesso", text_color="green")
    else:
        resultado_login.configure(text="Login incorreto", text_color="red")

def alternar_senha():
    if mostrar_senha_var.get() == 1:
        campo_senha.configure(show="")
    else:
        campo_senha.configure(show="*")

def abrir_tela_cadastro():
    janela_cadastro = ctk.CTkToplevel(app)
    janela_cadastro.title("Cadastro")
    janela_cadastro.geometry("300x350")

    label_novo_usuario = ctk.CTkLabel(janela_cadastro, text="Novo Usuário")
    label_novo_usuario.pack(pady=10)

    entrada_novo_usuario = ctk.CTkEntry(janela_cadastro, placeholder_text="Digite o nome de usuário")
    entrada_novo_usuario.pack(pady=10)

    label_nova_senha = ctk.CTkLabel(janela_cadastro, text="Nova Senha")
    label_nova_senha.pack(pady=10)

    entrada_nova_senha = ctk.CTkEntry(janela_cadastro, placeholder_text="Digite a senha", show="*")
    entrada_nova_senha.pack(pady=10)

    # Mostrar senha (checkbox)
    var_mostrar_senha_cadastro = ctk.IntVar()
    def alternar_senha_cadastro():
        if var_mostrar_senha_cadastro.get() == 1:
            entrada_nova_senha.configure(show="")
        else:
            entrada_nova_senha.configure(show="*")

    check_mostrar_senha_cadastro = ctk.CTkCheckBox(
        janela_cadastro, text="Mostrar senha",
        variable=var_mostrar_senha_cadastro,
        command=alternar_senha_cadastro
    )
    check_mostrar_senha_cadastro.pack(pady=5)

    resultado_cadastro = ctk.CTkLabel(janela_cadastro, text="")
    resultado_cadastro.pack(pady=10)

    def cadastrar_usuario():
        novo_usuario = entrada_novo_usuario.get()
        nova_senha = entrada_nova_senha.get()

        if novo_usuario in usuarios:
            resultado_cadastro.configure(text="Usuário já existe!", text_color="red")
        elif novo_usuario and nova_senha:
            usuarios[novo_usuario] = nova_senha
            salvar_usuarios()
            resultado_cadastro.configure(text="Usuário cadastrado!", text_color="green")
        else:
            resultado_cadastro.configure(text="Preencha todos os campos", text_color="orange")

    botao_confirmar = ctk.CTkButton(janela_cadastro, text="Cadastrar", command=cadastrar_usuario)
    botao_confirmar.pack(pady=10)

# - Janela principal
app = ctk.CTk()
app.title("Sistema de Login")
app.geometry("300x400")

# Label
label_usuario = ctk.CTkLabel(app, text="Usuário")
label_usuario.pack(pady=10)
# Entry
campo_usuario = ctk.CTkEntry(app, placeholder_text="Digite seu usuário")
campo_usuario.pack(pady=10)
# Label senha
label_senha = ctk.CTkLabel(app, text="Senha")
label_senha.pack(pady=10)
# Entry senha
campo_senha = ctk.CTkEntry(app, placeholder_text="Digite sua senha", show="*")
campo_senha.pack(pady=10)
# Mostra senha
mostrar_senha_var = ctk.IntVar()
check_mostrar_senha = ctk.CTkCheckBox(app, text="Mostrar senha", variable=mostrar_senha_var, command=alternar_senha)
check_mostrar_senha.pack(pady=5)
# Button login
botao_login = ctk.CTkButton(app, text="Login", command=validar_login)
botao_login.pack(pady=10)
# Button cadastro
botao_cadastro = ctk.CTkButton(app, text="Cadastre-se", command=abrir_tela_cadastro)
botao_cadastro.pack(pady=5)
# Feedback login
resultado_login = ctk.CTkLabel(app, text="")
resultado_login.pack(pady=10)

# - Iniciar aplicação
app.mainloop()
