# Ingressos Morumbi(s)

Protótipo de uma aplicação desktop para venda de ingressos nos totens do Estádio do Morumbi. O sistema permite visualizar jogos disponíveis, selecionar a quantidade de ingressos, informar os nomes dos compradores e escolher a forma de pagamento. Também possui uma área administrativa para cadastro e remoção de jogos.

## Tecnologias utilizadas

- Python
- Tkinter
- CustomTkinter
- SQLite

## Como rodar o projeto

### 1. Acesse a pasta do projeto

```powershell
cd ingressos-morumbi
```

### 2. Crie o ambiente virtual

```powershell
python -m venv .venv
```

### 3. Ative o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instale as dependências

```powershell
python -m pip install customtkinter
```

### 5. Execute a aplicação

```powershell
python main.py
```

O projeto utiliza o arquivo `morumbi.db` como banco de dados SQLite local.

## Acesso administrativo

As credenciais de administrador definidas no código são:

```text
usuário: admin
senha: 1234
```