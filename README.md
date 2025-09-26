# 🐾 Busca Pet API

API REST para gerenciamento de pets perdidos desenvolvida com Flask e SQLAlchemy.

## 📋 Funcionalidades

- ✅ Cadastro de pets perdidos com endereço de desaparecimento
- ✅ Busca de pets com filtros (nome, tipo, cidade, data)
- ✅ Paginação de resultados
- ✅ Atualização completa de dados do pet e endereço
- ✅ Exclusão de pets
- ✅ Documentação automática com Swagger UI
- ✅ Logs estruturados
- ✅ Validação de dados com Marshmallow

## 🛠️ Tecnologias

- **Python 3.13+**
- **Flask** - Framework web
- **Flask-RESTX** - Extensão para APIs REST e Swagger
- **SQLAlchemy** - ORM
- **Marshmallow** - Serialização e validação
- **Flask-CORS** - Suporte a CORS
- **SQLite** - Banco de dados (padrão)

## 📦 Instalação

### 1. Pré-requisitos

- Python 3.13 ou superior
- pip (gerenciador de pacotes Python)

### 2. Clone o repositório

```bash
git clone https://github.com/NatanMeira/busca-pet-api.git
cd busca-pet-api
```

### 3. Crie um ambiente virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No macOS/Linux:
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🚀 Execução

### Desenvolvimento

```bash
# Definir modo desenvolvimento
export FLASK_ENV=development

# Executar aplicação
python app.py
```

A API estará disponível em: **http://localhost:5000**

### Produção

```bash
# Definir modo produção
export FLASK_ENV=production

# Executar aplicação
python app.py
```

## 📚 Documentação da API

### Swagger UI

Acesse a documentação interativa em: **http://localhost:5000/api/docs/**

### Endpoints Principais

| Método   | Endpoint         | Descrição                         |
| -------- | ---------------- | --------------------------------- |
| `GET`    | `/api/pets`      | Lista todos os pets com paginação |
| `POST`   | `/api/pets`      | Cadastra um novo pet              |
| `GET`    | `/api/pets/{id}` | Busca pet por ID                  |
| `PUT`    | `/api/pets/{id}` | Atualiza pet e/ou endereço        |
| `DELETE` | `/api/pets/{id}` | Remove pet                        |

### Parâmetros de Busca

| Parâmetro     | Tipo     | Descrição                                     |
| ------------- | -------- | --------------------------------------------- |
| `nome`        | string   | Filtrar por nome do pet                       |
| `tipo`        | string   | Filtrar por tipo (Cachorro, Gato, Ave, Outro) |
| `cidade`      | string   | Filtrar por cidade                            |
| `start_date`  | datetime | Data inicial (ISO format)                     |
| `end_date`    | datetime | Data final (ISO format)                       |
| `page_number` | integer  | Número da página (padrão: 1)                  |
| `page_size`   | integer  | Itens por página (padrão: 20, máx: 100)       |

## 📝 Exemplos de Uso

### 1. Cadastrar um Pet

```bash
curl -X POST "http://localhost:5000/api/pets" \
-H "Content-Type: application/json" \
-d '{
  "tipo": "Cachorro",
  "nome": "Rex",
  "idade": "Adulto",
  "porte": "Medio",
  "raca": "Labrador",
  "info_contato": "joao@email.com",
  "sexo": "Macho",
  "descricao": "Cachorro marrom com coleira azul",
  "data_desaparecimento": "2025-09-20T10:00:00",
  "endereco_desaparecimento": {
    "cep": "12345-678",
    "rua": "Rua das Flores, 123",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "estado": "SP"
  }
}'
```

### 2. Buscar Pets com Filtros

```bash
# Buscar por nome
curl "http://localhost:5000/api/pets?nome=Rex"

# Buscar por tipo com paginação
curl "http://localhost:5000/api/pets?tipo=Cachorro&page_number=1&page_size=10"

# Buscar por cidade
curl "http://localhost:5000/api/pets?cidade=São Paulo"
```

### 3. Atualizar Pet

```bash
curl -X PUT "http://localhost:5000/api/pets/1" \
-H "Content-Type: application/json" \
-d '{
  "nome": "Rex Atualizado",
  "endereco_desaparecimento": {
    "cidade": "Rio de Janeiro",
    "estado": "RJ"
  }
}'
```

## 🗂️ Estrutura do Projeto

```
api/
├── app.py                 # Arquivo principal da aplicação
├── db.py                  # Configuração do banco de dados
├── logger.py              # Configuração de logs
├── swagger_models.py      # Modelos Swagger
├── requirements.txt       # Dependências Python
├── controllers/           # Controladores REST
│   ├── __init__.py
│   └── pet_controller.py
├── models/               # Modelos de dados
│   ├── __init__.py
│   ├── base.py
│   ├── endereco.py
│   └── pet.py
├── schemas/              # Esquemas de validação
│   ├── __init__.py
│   ├── endereco.py
│   ├── error.py
│   └── pet.py
├── services/             # Lógica de negócio
│   ├── __init__.py
│   ├── endereco_service.py
│   └── pet_service.py
└── instance/             # Banco SQLite (criado automaticamente)
    └── pets.db
```

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável       | Descrição             | Padrão              |
| -------------- | --------------------- | ------------------- |
| `FLASK_ENV`    | Ambiente de execução  | `development`       |
| `DATABASE_URL` | URL do banco de dados | `sqlite:///pets.db` |
| `PORT`         | Porta do servidor     | `5000`              |

## 📊 Modelo de Dados

### Pet

```python
{
    "id": 1,
    "tipo": "Cachorro",
    "nome": "Rex",
    "idade": "Adulto",
    "porte": "Medio",
    "raca": "Labrador",
    "info_contato": "joao@email.com",
    "sexo": "Macho",
    "descricao": "Cachorro marrom",
    "observacoes": "Muito dócil",
    "data_desaparecimento": "2025-09-20T10:00:00",
    "endereco_id": 1,
    "endereco": { ... },
    "created_at": "2025-09-20T10:00:00",
    "updated_at": "2025-09-20T10:00:00"
}
```

### Endereço

```python
{
    "id": 1,
    "cep": "12345678",
    "rua": "Rua das Flores",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "estado": "SP",
    "pais": "Brasil",
    "created_at": "2025-09-20T10:00:00",
    "updated_at": "2025-09-20T10:00:00"
}
```

## 🔍 Logs

Os logs são estruturados e salvos em `app.log`. Níveis disponíveis:

- **INFO**: Operações normais
- **WARNING**: Situações de atenção
- **ERROR**: Erros de operação

## 🧪 Testes

Para testar a API:

1. **Swagger UI**: http://localhost:5000/api/docs/
2. **cURL**: Exemplos fornecidos acima
3. **Postman**: Importe a documentação Swagger

## 📄 Licença

Este projeto está sob a licença MIT.
