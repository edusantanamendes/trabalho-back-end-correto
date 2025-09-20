# API do Consultório Médico

Uma API REST completa para gerenciamento de consultórios médicos, desenvolvida em Python com Flask, incluindo autenticação JWT e operações CRUD para usuários, pacientes e consultas.

## 🚀 Funcionalidades

### ✅ Implementadas
- **Autenticação JWT**: Sistema de login seguro com tokens JWT
- **Gerenciamento de Usuários**: 
  - Criação de usuários (Admin, Médico, Recepcionista)
  - Atualização de dados de usuários
  - Remoção de usuários (soft delete)
  - Listagem de usuários
- **Gerenciamento de Pacientes**:
  - Cadastro de pacientes
  - Listagem de pacientes
- **Gerenciamento de Consultas**:
  - Agendamento de consultas
  - Listagem de consultas
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
- `GET /api/usuarios` - Listar usuários
- `POST /api/usuarios` - Criar usuário (apenas admin)
- `GET /api/usuarios/{id}` - Obter usuário específico
- `PUT /api/usuarios/{id}` - Atualizar usuário
- `DELETE /api/usuarios/{id}` - Remover usuário (apenas admin)

#### Pacientes
- `GET /api/pacientes` - Listar pacientes
- `POST /api/pacientes` - Criar paciente

#### Consultas
- `GET /api/consultas` - Listar consultas
- `POST /api/consultas` - Criar consulta

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

#### 3. Listar Pacientes
```bash
curl -X GET http://localhost:5000/api/pacientes \
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
- Criação, listagem e atualização de usuários
- Criação e listagem de pacientes
- Criação e listagem de consultas
- Remoção de usuários

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
