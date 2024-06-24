# Estoque api

Siga os passos abaixo para executar a api, estou usando o mysql, então é necessário configurar na sua máquina, pode baixar por este link:
https://dev.mysql.com/downloads/mysql/

Obs: Já deixei um .env.example, basta renomear o arquivo para .env
e alterar de acordo com suas variáveis de ambiente.

## Requisitos

- Python 3.7+
- pip (Python package installer)
- MySQL Community Server

## Instalação

1. Clone o repositório:

```bash
git clone git@github.com:douglas-filipe/estoque-api.git
cd estoque-api
```

2. Configure o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate

# Se estiver usando o PowerShell:
.\venv\Scripts\activate.ps1 
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Baixe e instale o mysql por este link:

https://dev.mysql.com/downloads/mysql/

5. Crie um banco de dados local:

```bash
create database estoque;
```

6. Utilize o .env.example como referência e crie o .env 
com as suas credências do banco de dados:

```bash
DB_URL=mysql+pymysql://user:password@localhost:3306/db
```

7. Utilize as outras variáveis de ambiente:

```bash
SECRET_KEY=sua_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Execução do projeto

1. Após todos os processos acima, execute este comando
para rodar a sua aplicação local.

```bash
uvicorn app.main:app --reload
```

Estará disponível no link a documentação: http://127.0.0.1:8000/docs

## Execução do testes

1. Crie um banco de teste

```bash
create database estoque_test;
```

2. Adicione no .env o banco de teste

```bash
DB_URL_TEST=mysql+pymysql://root:1234@localhost:3306/estoque_test
```

3. Execute no terminal o comando

```bash
pytest
```