def criarTabelas(conexao, cursor):
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS times (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   time TEXT NOT NULL
                   )''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS competicoes(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   competicao TEXT NOT NULL
                   )''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS jogos (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   competicao INTEGER NOT NULL,
                   time_1 INTEGER NOT NULL,
                   time_2 INTEGER NOT NULL,
                   data TEXT NOT NULL,
                   horario TEXT NOT NULL
                   )''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS administrador (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   usuario TEXT NOT NULL,
                   senha TEXT NOT NULL
                   )''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS ingressos (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   jogo INTEGER NOT NULL,
                   forma_pagamento INTEGER NOT NULL,
                   valor NUMERIC NOT NULL,
                   data_venda TEXT NOT NULL
                   )''')
    
    conexao.commit()

def popularTabelas(conexao, cursor):
    cursor.execute('''INSERT INTO times (time) VALUES
    ('São Paulo'),
    ('Palmeiras'),
    ('Corinthians'),
    ('Santos'),
    ('Flamengo'),
    ('Vasco'),
    ('Botafogo'),
    ('Fluminense'),
    ('Grêmio'),
    ('Internacional'),
    ('Atlético-MG'),
    ('Cruzeiro'),
    ('Bahia'),
    ('Sport'),
    ('Fortaleza'),
    ('Ceará'),
    ('Atlético-PR'),
    ('Goiás'),
    ('Coritiba'),
    ('Chapecoense');''')

    cursor.execute('''INSERT INTO competicoes (competicao) VALUES
    ('Campeonato Brasileiro Série A'),
    ('Copa do Brasil'),
    ('Campeonato Paulista'),
    ('Copa Libertadores'),
    ('Copa Sul-Americana'),
    ('Supercopa do Brasil');''')

    cursor.execute('''INSERT INTO jogos (competicao, time_1, time_2, data, horario) VALUES
    (4, 1, 3, '2024-01-20', '16:00'),
    (4, 2, 4, '2024-01-21', '18:30'),
    (3, 5, 8, '2024-02-15', '21:00'),
    (3, 6, 7, '2024-02-16', '19:00'),
    (1, 1, 9, '2024-03-10', '16:00'),
    (1, 5, 10, '2024-03-12', '21:00'),
    (4, 1, 3, '2024-04-05', '21:00'),
    (4, 2, 4, '2024-04-06', '19:00'),
    (2, 13, 14, '2024-05-01', '16:00'),
    (2, 18, 19, '2024-05-02', '18:00'),
    (6, 1, 16, '2024-06-15', '19:00'),
    (6, 6, 15, '2024-06-16', '21:30'),
    (1, 7, 12, '2024-07-10', '16:00'),
    (1, 2, 11, '2024-07-11', '18:30'),
    (3, 6, 10, '2024-08-10', '19:00'),
    (3, 5, 7, '2024-08-12', '21:30'),
    (4, 1, 4, '2024-09-01', '16:00'),
    (4, 2, 3, '2024-09-02', '18:00'),
    (6, 9, 6, '2024-10-15', '21:30'),
    (6, 3, 8, '2024-10-16', '19:30'),
    (1, 5, 10, '2024-11-05', '21:00'), 
    (1, 6, 12, '2024-11-06', '19:00'),
    (5, 2, 16, '2024-12-10', '19:00'),
    (5, 7, 15, '2024-12-12', '21:30');
    ''')

    conexao.commit()