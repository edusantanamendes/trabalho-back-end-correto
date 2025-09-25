# API do Consultório Médico

Uma API REST completa para gerenciamento de consultórios médicos, desenvolvida em Python com Flask, incluindo autenticação JWT e operações CRUD para usuários, pacientes e consultas.

## 🚀 Funcionalidades

### ✅ Implementadas
- **Autenticação JWT**: Sistema de login seguro com tokens JWT
- **Gerenciamento de Usuários**: 
  - Criação de usuários (Admin, Médico, Recepcionista)
  - Atualização de dados de usuários
  - Remoção de usuários (soft delete)
  - Listagem de usuários com paginação e filtros
  - Obtenção de usuário específico por ID
- **Gerenciamento de Pacientes**:
  - Cadastro de pacientes com validação de CPF
  - Listagem de pacientes com paginação
  - Atualização de dados de pacientes
  - Remoção de pacientes (soft delete)
  - Obtenção de paciente específico por ID
  - Busca de pacientes por nome ou CPF
- **Gerenciamento de Consultas**:
  - Agendamento de consultas
  - Listagem de consultas com paginação
  - Atualização de consultas
  - Remoção de consultas
  - Obtenção de consulta específica por ID
  - Busca de consultas por data, médico ou status
- **Validações e Segurança**:
  - Validação de CPF brasileiro
  - Controle de acesso baseado em tipo de usuário
  - Soft delete para preservar histórico
- **Banco de Dados SQLite**: Com dados de exemplo pré-carregados

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Flask**: Framework web
- **Flask-SQLAlchemy**: ORM para banco de dados
- **Flask-JWT-Extended**: Autenticação JWT
- **SQLite**: Banco de dados
- **Werkzeug**: Utilitários de segurança

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone ou baixe o projeto**
```bash
# Se usando Git
git clone <url-do-repositorio>
cd consultorio_medico_api

# Ou simplesmente extraia o arquivo ZIP na pasta desejada
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Inicialize o banco de dados**
```bash
python init_db.py
```

4. **Execute a aplicação**
```bash
python app.py
```

A API estará disponível em: `http://localhost:5000`

## 📚 Documentação da API

### Endpoints Disponíveis

#### Autenticação
- `POST /api/auth/login` - Realizar login

#### Usuários
- `GET /api/usuarios` - Listar usuários (com paginação e filtros)
- `POST /api/usuarios` - Criar usuário (apenas admin)
- `GET /api/usuarios/{id}` - Obter usuário específico
- `PUT /api/usuarios/{id}` - Atualizar usuário
- `DELETE /api/usuarios/{id}` - Remover usuário (apenas admin)

#### Pacientes
- `GET /api/pacientes` - Listar pacientes (com paginação)
- `POST /api/pacientes` - Criar paciente (com validação de CPF)
- `GET /api/pacientes/{id}` - Obter paciente específico
- `PUT /api/pacientes/{id}` - Atualizar paciente
- `DELETE /api/pacientes/{id}` - Remover paciente (admin/recepcionista)
- `GET /api/pacientes/buscar` - Buscar pacientes por nome ou CPF

#### Consultas
- `GET /api/consultas` - Listar consultas (com paginação)
- `POST /api/consultas` - Criar consulta
- `GET /api/consultas/{id}` - Obter consulta específica
- `PUT /api/consultas/{id}` - Atualizar consulta
- `DELETE /api/consultas/{id}` - Remover consulta
- `GET /api/consultas/buscar` - Buscar consultas por filtros

#### Sistema
- `GET /api/health` - Verificar saúde da API

### Exemplos de Uso

#### 1. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.silva@consultorio.com",
    "senha": "123456"
  }'
```

#### 2. Criar Usuário (requer token JWT)
```bash
curl -X POST http://localhost:5000/api/usuarios \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_JWT" \
  -d '{
    "nome": "Dr. Novo Médico",
    "email": "novo.medico@consultorio.com",
    "senha": "123456",
    "tipo_usuario": "medico",
    "telefone": "(11) 99999-9999",
    "endereco": "Rua Exemplo, 123"
  }'
```

#### 3. Listar Pacientes com Paginação
```bash
curl -X GET "http://localhost:5000/api/pacientes?pagina=1&por_pagina=10" \
  -H "Authorization: Bearer SEU_TOKEN_JWT"
```

#### 4. Buscar Pacientes
```bash
curl -X GET "http://localhost:5000/api/pacientes/buscar?q=Carlos" \
  -H "Authorization: Bearer SEU_TOKEN_JWT"
```

#### 5. Atualizar Paciente
```bash
curl -X PUT http://localhost:5000/api/pacientes/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_JWT" \
  -d '{
    "telefone": "(11) 99999-0000",
    "email": "novo.email@exemplo.com"
  }'
```

#### 6. Buscar Consultas por Status
```bash
curl -X GET "http://localhost:5000/api/consultas/buscar?status=agendada" \
  -H "Authorization: Bearer SEU_TOKEN_JWT"
```

#### 7. Buscar Consultas por Data
```bash
curl -X GET "http://localhost:5000/api/consultas/buscar?data_inicio=2024-01-01&data_fim=2024-01-31" \
  -H "Authorization: Bearer SEU_TOKEN_JWT"
```

#### 8. Listar Usuários por Tipo
```bash
curl -X GET "http://localhost:5000/api/usuarios?tipo_usuario=medico&pagina=1&por_pagina=5" \
  -H "Authorization: Bearer SEU_TOKEN_JWT"
```

## 👥 Usuários de Exemplo

Após executar `init_db.py`, os seguintes usuários estarão disponíveis:

| Email | Senha | Tipo | Descrição |
|-------|-------|------|-----------|
| joao.silva@consultorio.com | 123456 | admin | Administrador do sistema |
| maria.santos@consultorio.com | 123456 | medico | Médica |
| pedro.costa@consultorio.com | 123456 | medico | Médico |
| ana.oliveira@consultorio.com | 123456 | recepcionista | Recepcionista |

## 🧪 Testes

Execute o script de testes para verificar todas as funcionalidades:

```bash
python test_api.py
```

Este script demonstra:
- Login e autenticação
- Criação, listagem, atualização e remoção de usuários
- Listagem com paginação e filtros
- Criação, listagem, atualização e remoção de pacientes
- Busca de pacientes por nome ou CPF
- Validação de CPF
- Criação, listagem, atualização e remoção de consultas
- Busca de consultas por data, médico ou status
- Controle de acesso baseado em tipo de usuário

## 📁 Estrutura do Projeto

```
consultorio_medico_api/
├── app.py                 # Aplicação principal Flask
├── config.py             # Configurações da aplicação
├── init_db.py           # Script de inicialização do banco
├── test_api.py          # Script de testes
├── database_schema.sql  # Schema SQL do banco
├── requirements.txt     # Dependências Python
└── README.md           # Este arquivo
```

## 🔒 Segurança

- **Senhas**: Armazenadas com hash usando Werkzeug
- **JWT**: Tokens com expiração de 24 horas
- **Autorização**: Controle de acesso baseado em tipo de usuário
- **Validação**: Validação de dados de entrada
- **Soft Delete**: Usuários removidos são marcados como inativos

## 🚀 Deploy em Produção

Para produção, recomenda-se:

1. **Alterar chaves secretas**:
   - `SECRET_KEY`
   - `JWT_SECRET_KEY`

2. **Usar banco de dados robusto**:
   - PostgreSQL ou MySQL
   - Configurar variáveis de ambiente

3. **Usar servidor WSGI**:
   - Gunicorn ou uWSGI

4. **Configurar HTTPS**:
   - Certificado SSL

## 📝 Licença

Este projeto é fornecido como exemplo educacional. Sinta-se livre para usar e modificar conforme necessário.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Adicionar novas funcionalidades
- Melhorar a documentação

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências estão instaladas
2. Execute `init_db.py` antes de usar a API
3. Verifique se a porta 5000 está disponível
4. Consulte os logs de erro para mais detalhes

---

**Desenvolvido com ❤️ para gerenciamento de consultórios médicos**
