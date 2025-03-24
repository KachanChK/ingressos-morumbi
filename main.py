import customtkinter as ctk
import tkinter as tk 
import sqlite3
import datetime
import locale
from sql import *

conexao = sqlite3.connect("morumbi.db")
cursor = conexao.cursor()

criarTabelas(conexao, cursor)

# Função para abrir a janela de compra de ingressos
def abrir_janela_compra(competicao, time1, time2, data, horario, jogo_id):
    janela_compra = ctk.CTkToplevel()  # Cria uma nova janela
    janela_compra.title("Compra de Ingresso")
    janela_compra.geometry("1200x800")
    
    # Exibir informações do jogo selecionado
    info_label = ctk.CTkLabel(janela_compra, text=f"Competição: {competicao}\n{time1} x {time2}\nData: {data}\nHorário: {horario}", font=("Arial", 14))
    info_label.pack(pady=20)
    
    # Seleção da quantidade de ingressos
    quantidade_label = ctk.CTkLabel(janela_compra, text="Quantidade de ingressos:", font=("Arial", 12))
    quantidade_label.pack(pady=5)
    
    quantidade_var = tk.IntVar(value=1)  # Quantidade de ingressos inicial
    quantidade_entry = ctk.CTkEntry(janela_compra, textvariable=quantidade_var)
    quantidade_entry.pack(pady=5)
    
    nomes_ingressos_frame = ctk.CTkFrame(janela_compra)
    nomes_ingressos_frame.pack(pady=10)

    nomes_ingressos_vars = []

    # Função para atualizar os campos de nome conforme a quantidade de ingressos
    def atualizar_campos_nomes(*args):
        for widget in nomes_ingressos_frame.winfo_children():
            widget.destroy()

        nomes_ingressos_vars.clear()
        
        for i in range(quantidade_var.get()):
            nome_label = ctk.CTkLabel(nomes_ingressos_frame, text=f"Nome para o ingresso {i+1}:", font=("Arial", 12))
            nome_label.pack(pady=2)
            nome_var = tk.StringVar()
            nome_entry = ctk.CTkEntry(nomes_ingressos_frame, textvariable=nome_var)
            nome_entry.pack(pady=2)
            nomes_ingressos_vars.append(nome_var)

    # Atualizar campos de nome quando a quantidade mudar
    quantidade_var.trace_add('write', atualizar_campos_nomes)

    # Inicializar os campos com 1 ingresso
    atualizar_campos_nomes()

    # Adicionar opções de forma de pagamento
    pagamento_label = ctk.CTkLabel(janela_compra, text="Selecione a forma de pagamento:", font=("Arial", 12))
    pagamento_label.pack(pady=10)
    
    forma_pagamento_var = tk.StringVar(value="PIX")  # Valor padrão é PIX
    
    opcoes_pagamento_frame = ctk.CTkFrame(janela_compra)
    opcoes_pagamento_frame.pack(pady=5)
    
    pix_radio = ctk.CTkRadioButton(opcoes_pagamento_frame, text="PIX", variable=forma_pagamento_var, value="PIX")
    pix_radio.pack(side="left", padx=10)

    debito_radio = ctk.CTkRadioButton(opcoes_pagamento_frame, text="Cartão de Débito", variable=forma_pagamento_var, value="Débito")
    debito_radio.pack(side="left", padx=10)

    credito_radio = ctk.CTkRadioButton(opcoes_pagamento_frame, text="Cartão de Crédito", variable=forma_pagamento_var, value="Crédito")
    credito_radio.pack(side="left", padx=10)

    # Função para salvar a compra de cada ingresso
    def confirmar_compra():
        forma_pagamento = forma_pagamento_var.get()
        valor_ingresso = 20  # Valor do ingresso definido
        data_venda = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for nome_var in nomes_ingressos_vars:
            nome_ingresso = nome_var.get()
            cursor.execute(
                '''
                INSERT INTO ingressos (jogo, forma_pagamento, valor, data_venda)
                VALUES (?, ?, ?, ?)
                ''', 
                (jogo_id, forma_pagamento, valor_ingresso, data_venda)  # Use o jogo_id aqui
            )
            conexao.commit()

        # Fechar a janela de compra
        janela_compra.destroy()

        # Exibir uma janela de sucesso
        janela_sucesso = ctk.CTkToplevel()
        janela_sucesso.title("Sucesso")
        janela_sucesso.geometry("300x200")
        sucesso_label = ctk.CTkLabel(janela_sucesso, text="Compra realizada com sucesso!", font=("Arial", 16))
        sucesso_label.pack(pady=20)

        botao_ok = ctk.CTkButton(janela_sucesso, text="OK", command=janela_sucesso.destroy)
        botao_ok.pack(pady=10)

    # Botão para confirmar a compra
    botao_comprar = ctk.CTkButton(janela_compra, text="Confirmar Compra", command=confirmar_compra)
    botao_comprar.pack(pady=10)

# Função para abrir a janela de login do administrador
def abrir_janela_login_admin():
    global janela_login
    janela_login = ctk.CTkToplevel()
    janela_login.title("Login do Administrador")
    janela_login.geometry("400x300")

    # Label de instrução
    login_label = ctk.CTkLabel(janela_login, text="Área de Administrador", font=("Arial", 18))
    login_label.pack(pady=20)

    # Campo para o nome de usuário
    usuario_label = ctk.CTkLabel(janela_login, text="Usuário")
    usuario_label.pack(pady=5)
    entrada_usuario = ctk.CTkEntry(janela_login)
    entrada_usuario.pack(pady=5)

    # Campo para a senha
    senha_label = ctk.CTkLabel(janela_login, text="Senha")
    senha_label.pack(pady=5)
    entrada_senha = ctk.CTkEntry(janela_login, show="*")  # 'show="*"' para ocultar a senha
    entrada_senha.pack(pady=5)

    # Botão para confirmar o login
    botao_confirmar = ctk.CTkButton(janela_login, text="Confirmar", command=lambda: confirmar_login(entrada_usuario.get(), entrada_senha.get()))
    botao_confirmar.pack(pady=20)

# Função para abrir a janela de gerenciamento de jogos (após login bem-sucedido)
def abrir_janela_admin():
    janela_admin = ctk.CTkToplevel()
    janela_admin.title("Área do Administrador - Gerenciar Jogos")
    janela_admin.geometry("600x700")

    # Label de título
    titulo_label = ctk.CTkLabel(janela_admin, text="Gerenciar Jogos", font=("Arial", 18))
    titulo_label.pack(pady=20)

    # Função para cadastrar um novo jogo
    def cadastrar_jogo():
        competicao_nome = competicao_var.get()
        time1_nome = time1_var.get()
        time2_nome = time2_var.get()
        data_jogo = entrada_data.get()
        horario_jogo = entrada_horario.get()

        # Mapeia os nomes para os respectivos IDs
        cursor.execute('SELECT id FROM competicoes WHERE competicao = ?', (competicao_nome,))
        competicao_id = cursor.fetchone()[0]

        cursor.execute('SELECT id FROM times WHERE time = ?', (time1_nome,))
        time1_id = cursor.fetchone()[0]

        cursor.execute('SELECT id FROM times WHERE time = ?', (time2_nome,))
        time2_id = cursor.fetchone()[0]

        # Inserir o novo jogo no banco de dados
        cursor.execute('''
            INSERT INTO jogos (competicao, time_1, time_2, data, horario)
            VALUES (?, ?, ?, ?, ?)
        ''', (competicao_id, time1_id, time2_id, data_jogo, horario_jogo))
        conexao.commit()

        # Exibir uma mensagem de sucesso
        ctk.CTkLabel(janela_admin, text="Jogo cadastrado com sucesso!", font=("Arial", 14)).pack(pady=5)

    # Função para remover um jogo
    def remover_jogo():
        jogo_id = entrada_jogo_id.get()

        # Remover o jogo do banco de dados
        cursor.execute('DELETE FROM jogos WHERE id = ?', (jogo_id,))
        conexao.commit()

        # Exibir uma mensagem de sucesso
        ctk.CTkLabel(janela_admin, text="Jogo removido com sucesso!", font=("Arial", 14)).pack(pady=5)

    # Dropdown para selecionar a competição (somente os nomes)
    cursor.execute('SELECT competicao FROM competicoes')
    competicoes = cursor.fetchall()
    competicao_var = tk.StringVar()
    competicao_dropdown = ctk.CTkOptionMenu(janela_admin, variable=competicao_var, values=[c[0] for c in competicoes])
    competicao_dropdown.pack(pady=10)

    # Dropdown para selecionar time 1 (somente os nomes)
    cursor.execute('SELECT time FROM times')
    times = cursor.fetchall()
    time1_var = tk.StringVar()
    time1_dropdown = ctk.CTkOptionMenu(janela_admin, variable=time1_var, values=[t[0] for t in times])
    time1_dropdown.pack(pady=10)

    # Dropdown para selecionar time 2 (somente os nomes)
    time2_var = tk.StringVar()
    time2_dropdown = ctk.CTkOptionMenu(janela_admin, variable=time2_var, values=[t[0] for t in times])
    time2_dropdown.pack(pady=10)

    # Campos de data e horário
    ctk.CTkLabel(janela_admin, text="Data (AAAA-MM-DD):", font=("Arial", 12)).pack(pady=5)
    entrada_data = ctk.CTkEntry(janela_admin)
    entrada_data.pack(pady=5)

    ctk.CTkLabel(janela_admin, text="Horário (HH:MM):", font=("Arial", 12)).pack(pady=5)
    entrada_horario = ctk.CTkEntry(janela_admin)
    entrada_horario.pack(pady=5)

    # Botão para cadastrar o jogo
    botao_cadastrar = ctk.CTkButton(janela_admin, text="Cadastrar Jogo", command=cadastrar_jogo)
    botao_cadastrar.pack(pady=10)

    # Campo para remover jogo pelo ID
    ctk.CTkLabel(janela_admin, text="ID do jogo a remover:", font=("Arial", 12)).pack(pady=5)
    entrada_jogo_id = ctk.CTkEntry(janela_admin)
    entrada_jogo_id.pack(pady=5)

    botao_remover = ctk.CTkButton(janela_admin, text="Remover Jogo", command=remover_jogo)
    botao_remover.pack(pady=10)

# Função de validação de login (atualizada para abrir a janela de admin)
def confirmar_login(usuario, senha):
    admin_usuario = "admin"
    admin_senha = "1234"

    if usuario == admin_usuario and senha == admin_senha:
        print("Login bem-sucedido")
        # Fecha a janela de login
        janela_login.destroy()
        # Abre a janela de administração
        abrir_janela_admin()
    else:
        print("Usuário ou senha incorretos")

# Função para criar o catálogo de jogos
def criar_catalogo_jogos(mes_selecionado):
    for widget in frame_jogos.winfo_children():
        widget.destroy()

    query = '''
        SELECT jogos.id, competicoes.competicao, times1.time, times2.time, jogos.data, jogos.horario
        FROM jogos
        INNER JOIN times AS times1 ON jogos.time_1 = times1.id
        INNER JOIN times AS times2 ON jogos.time_2 = times2.id
        INNER JOIN competicoes ON jogos.competicao = competicoes.id
        WHERE strftime('%m', jogos.data) = ?
    '''

    meses_numeros = {
        "Janeiro": "01", "Fevereiro": "02", "Março": "03", "Abril": "04", 
        "Maio": "05", "Junho": "06", "Julho": "07", "Agosto": "08", 
        "Setembro": "09", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
    }
    
    numero_mes = meses_numeros.get(mes_selecionado, None)
    if numero_mes is None:
        print(f"Mês selecionado '{mes_selecionado}' não é válido.")
        return
    
    print(f"Selecionado mês: {mes_selecionado}, Número do mês: {numero_mes}")
    cursor.execute(query, (numero_mes,))
    jogos = cursor.fetchall()
    
    print(f"Jogos encontrados: {jogos}")
    if not jogos:
        print(f"Não há jogos para o mês {mes_selecionado}.")
        return
    
    for jogo in jogos:
        jogo_id, competicao, time1, time2, data, horario = jogo  # Desestruture incluindo o ID do jogo
        jogo_frame = ctk.CTkFrame(frame_jogos)
        jogo_frame.pack(pady=10, padx=20, fill="x")
        
        detalhes = f"{competicao} | {data} - {horario}"
        detalhes_label = ctk.CTkLabel(jogo_frame, text=detalhes, font=("Arial", 14))
        detalhes_label.pack(side="top", anchor="w", padx=10, pady=5)
        
        jogo_label = ctk.CTkLabel(jogo_frame, text=f"{time1} x {time2}", font=("Arial", 16, "bold"))
        jogo_label.pack(side="top", anchor="w", padx=10, pady=5)
        
        # Botão para abrir a janela de compra de ingressos
        botao_compra = ctk.CTkButton(jogo_frame, text="Comprar Ingresso", command=lambda c=competicao, t1=time1, t2=time2, d=data, h=horario, j=jogo_id: abrir_janela_compra(c, t1, t2, d, h, j))
        botao_compra.place(relx=0.5, rely=0.5, anchor="center")
        botao_compra.place(relx=0.5, rely=0.5, anchor="center")

# Interface principal
janela = ctk.CTk()
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
janela.geometry(f"{largura_tela}x{altura_tela}+0+0")
janela.title("Ingressos Morumbi")

navbar = ctk.CTkFrame(janela, height=80, corner_radius=0, fg_color='white')
navbar.pack(side=tk.TOP, fill=tk.X)

frame_botoes = ctk.CTkFrame(navbar, fg_color='white')
frame_botoes.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

frame_jogos = ctk.CTkFrame(janela, fg_color='white')
frame_jogos.pack(fill="both", expand=True, padx=20, pady=20)

# Adicionando o botão de "Área de Administrador" na navbar
botao_admin = ctk.CTkButton(navbar, text="Área de Administrador", width=150, height=50, command=abrir_janela_login_admin)
botao_admin.pack(side=tk.RIGHT, padx=10, pady=10)

meses = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

for mes in meses:
    botao_mes = ctk.CTkButton(frame_botoes, text=mes, width=100, height=60, command=lambda m=mes: criar_catalogo_jogos(m))
    botao_mes.pack(side=tk.LEFT, padx=2, pady=5)

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
mes_atual = datetime.datetime.now().strftime("%B")
criar_catalogo_jogos(mes_atual.capitalize())

janela.mainloop()