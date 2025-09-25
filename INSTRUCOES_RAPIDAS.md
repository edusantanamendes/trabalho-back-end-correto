# 🚀 INSTRUÇÕES RÁPIDAS - CONSULTÓRIO MÉDICO API

## ⚡ Inicialização Rápida

### Opção 1: Script Automático (Recomendado)
```bash
python run.py
```

### Opção 2: Manual
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Inicializar banco de dados
python init_db.py

# 3. Executar aplicação
python app.py
```

## 🔑 Credenciais de Acesso

| Tipo | Email | Senha |
|------|-------|-------|
| **Admin** | joao.silva@consultorio.com | 123456 |
| **Médico** | maria.santos@consultorio.com | 123456 |
| **Recepcionista** | ana.oliveira@consultorio.com | 123456 |

## 📡 Endpoints Principais

### Autenticação
- `POST /api/auth/login` - Login

### Usuários (requer autenticação)
- `GET /api/usuarios` - Listar usuários
- `POST /api/usuarios` - Criar usuário (apenas admin)
- `PUT /api/usuarios/{id}` - Atualizar usuário
- `DELETE /api/usuarios/{id}` - Remover usuário (apenas admin)

### Pacientes (requer autenticação)
- `GET /api/pacientes` - Listar pacientes
- `POST /api/pacientes` - Criar paciente

### Consultas (requer autenticação)
- `GET /api/consultas` - Listar consultas
- `POST /api/consultas` - Criar consulta

### Sistema
- `GET /api/health` - Verificar status da API

## 🧪 Teste Rápido

```bash
# Executar testes automatizados
python test_api.py
```

## 📱 Teste com cURL

### 1. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "joao.silva@consultorio.com", "senha": "123456"}'
```

### 2. Listar Usuários (substitua TOKEN pelo token retornado no login)
```bash
curl -X GET http://localhost:5000/api/usuarios \
  -H "Authorization: Bearer TOKEN"
```

## 🔧 Solução de Problemas

### Erro: "Module not found"
```bash
pip install -r requirements.txt
```

### Erro: "Database not found"
```bash
python init_db.py
```

### Erro: "Port already in use"
- Pare outros serviços na porta 5000
- Ou altere a porta no arquivo `app.py`

### Erro: "Permission denied"
- Execute como administrador (Windows)
- Ou use `sudo` (Linux/Mac)

## 📋 Checklist de Funcionalidades

- ✅ Autenticação JWT
- ✅ Criação de usuários
- ✅ Atualização de usuários  
- ✅ Remoção de usuários
- ✅ Listagem de usuários com paginação
- ✅ Filtros por tipo de usuário
- ✅ Gerenciamento completo de pacientes
- ✅ Validação de CPF brasileiro
- ✅ Busca de pacientes por nome/CPF
- ✅ Gerenciamento completo de consultas
- ✅ Busca de consultas por filtros
- ✅ Controle de acesso por tipo de usuário
- ✅ Paginação em todas as listagens
- ✅ Soft delete para preservar histórico
- ✅ Banco de dados SQLite
- ✅ Dados de exemplo
- ✅ Documentação completa
- ✅ Testes automatizados

## 🌐 Acesso à API

- **URL Base**: http://localhost:5000
- **Documentação**: README.md
- **Coleção Postman**: postman_collection.json
- **Testes**: test_api.py

---

**🎯 Projeto desenvolvido em Python com Flask, SQLAlchemy e JWT**
