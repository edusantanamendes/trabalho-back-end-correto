from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import re
from config import config

# Configuração da aplicação Flask
app = Flask(__name__)

# Carregar configuração baseada no ambiente
config_name = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(config[config_name])

# Inicialização das extensões
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Função para validar CPF
def validar_cpf(cpf):
    """Valida CPF brasileiro"""
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto
    
    # Verifica o primeiro dígito
    if int(cpf[9]) != digito1:
        return False
    
    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto
    
    # Verifica o segundo dígito
    if int(cpf[10]) != digito2:
        return False
    
    return True

# Modelo de Usuário
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)  # 'admin', 'medico', 'recepcionista'
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo_usuario': self.tipo_usuario,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'data_criacao': self.data_criacao.isoformat(),
            'ativo': self.ativo
        }

# Modelo de Paciente
class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    endereco = db.Column(db.String(200))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento.isoformat(),
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'data_cadastro': self.data_cadastro.isoformat(),
            'ativo': self.ativo
        }

# Modelo de Consulta
class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_consulta = db.Column(db.DateTime, nullable=False)
    tipo_consulta = db.Column(db.String(50), nullable=False)
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='agendada')  # 'agendada', 'realizada', 'cancelada'
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    paciente = db.relationship('Paciente', backref='consultas')
    medico = db.relationship('Usuario', backref='consultas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'medico_id': self.medico_id,
            'data_consulta': self.data_consulta.isoformat(),
            'tipo_consulta': self.tipo_consulta,
            'observacoes': self.observacoes,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat(),
            'paciente_nome': self.paciente.nome if self.paciente else None,
            'medico_nome': self.medico.nome if self.medico else None
        }

# Rotas de Autenticação
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('senha'):
            return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
        
        usuario = Usuario.query.filter_by(email=data['email'], ativo=True).first()
        
        if usuario and check_password_hash(usuario.senha_hash, data['senha']):
            access_token = create_access_token(identity=str(usuario.id))
            return jsonify({
                'mensagem': 'Login realizado com sucesso',
                'access_token': access_token,
                'usuario': usuario.to_dict()
            }), 200
        else:
            return jsonify({'erro': 'Credenciais inválidas'}), 401
            
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

# Rotas de Usuários
@app.route('/api/usuarios', methods=['POST'])
@jwt_required()
def criar_usuario():
    try:
        data = request.get_json()
        usuario_atual_id = get_jwt_identity()
        usuario_atual = Usuario.query.get(usuario_atual_id)
        
        # Verificar se o usuário atual é admin
        if usuario_atual.tipo_usuario != 'admin':
            return jsonify({'erro': 'Apenas administradores podem criar usuários'}), 403
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['nome', 'email', 'senha', 'tipo_usuario']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
        
        # Verificar se email já existe
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'Email já cadastrado'}), 400
        
        # Criar novo usuário
        novo_usuario = Usuario(
            nome=data['nome'],
            email=data['email'],
            senha_hash=generate_password_hash(data['senha']),
            tipo_usuario=data['tipo_usuario'],
            telefone=data.get('telefone'),
            endereco=data.get('endereco')
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Usuário criado com sucesso',
            'usuario': novo_usuario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    try:
        # Parâmetros de paginação
        pagina = request.args.get('pagina', 1, type=int)
        por_pagina = request.args.get('por_pagina', 10, type=int)
        tipo_usuario = request.args.get('tipo_usuario')
        
        # Limitar o número de itens por página
        if por_pagina > 100:
            por_pagina = 100
        
        # Query base
        query = Usuario.query.filter_by(ativo=True)
        
        # Filtrar por tipo de usuário
        if tipo_usuario:
            if tipo_usuario not in ['admin', 'medico', 'recepcionista']:
                return jsonify({'erro': 'Tipo de usuário inválido'}), 400
            query = query.filter(Usuario.tipo_usuario == tipo_usuario)
        
        # Paginação
        paginacao = query.paginate(
            page=pagina, 
            per_page=por_pagina, 
            error_out=False
        )
        
        return jsonify({
            'usuarios': [usuario.to_dict() for usuario in paginacao.items],
            'paginacao': {
                'pagina_atual': paginacao.page,
                'total_paginas': paginacao.pages,
                'total_itens': paginacao.total,
                'itens_por_pagina': por_pagina,
                'tem_proxima': paginacao.has_next,
                'tem_anterior': paginacao.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
@jwt_required()
def obter_usuario(usuario_id):
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        return jsonify({'usuario': usuario.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(usuario_id):
    try:
        data = request.get_json()
        usuario_atual_id = get_jwt_identity()
        usuario_atual = Usuario.query.get(usuario_atual_id)
        
        # Verificar se o usuário atual é admin ou está atualizando seu próprio perfil
        if usuario_atual.tipo_usuario != 'admin' and usuario_atual_id != usuario_id:
            return jsonify({'erro': 'Você só pode atualizar seu próprio perfil'}), 403
        
        usuario = Usuario.query.get_or_404(usuario_id)
        
        # Atualizar campos
        if 'nome' in data:
            usuario.nome = data['nome']
        if 'email' in data:
            # Verificar se email já existe em outro usuário
            usuario_existente = Usuario.query.filter_by(email=data['email']).first()
            if usuario_existente and usuario_existente.id != usuario_id:
                return jsonify({'erro': 'Email já cadastrado'}), 400
            usuario.email = data['email']
        if 'senha' in data:
            usuario.senha_hash = generate_password_hash(data['senha'])
        if 'tipo_usuario' in data and usuario_atual.tipo_usuario == 'admin':
            usuario.tipo_usuario = data['tipo_usuario']
        if 'telefone' in data:
            usuario.telefone = data['telefone']
        if 'endereco' in data:
            usuario.endereco = data['endereco']
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Usuário atualizado com sucesso',
            'usuario': usuario.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
def remover_usuario(usuario_id):
    try:
        usuario_atual_id = get_jwt_identity()
        usuario_atual = Usuario.query.get(usuario_atual_id)
        
        # Verificar se o usuário atual é admin
        if usuario_atual.tipo_usuario != 'admin':
            return jsonify({'erro': 'Apenas administradores podem remover usuários'}), 403
        
        usuario = Usuario.query.get_or_404(usuario_id)
        
        # Soft delete - marcar como inativo
        usuario.ativo = False
        db.session.commit()
        
        return jsonify({'mensagem': 'Usuário removido com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

# Rotas de Pacientes
@app.route('/api/pacientes', methods=['POST'])
@jwt_required()
def criar_paciente():
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['nome', 'cpf', 'data_nascimento']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
        
        # Validar CPF
        if not validar_cpf(data['cpf']):
            return jsonify({'erro': 'CPF inválido'}), 400
        
        # Verificar se CPF já existe
        if Paciente.query.filter_by(cpf=data['cpf']).first():
            return jsonify({'erro': 'CPF já cadastrado'}), 400
        
        # Criar novo paciente
        novo_paciente = Paciente(
            nome=data['nome'],
            cpf=data['cpf'],
            data_nascimento=datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date(),
            telefone=data.get('telefone'),
            email=data.get('email'),
            endereco=data.get('endereco')
        )
        
        db.session.add(novo_paciente)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Paciente criado com sucesso',
            'paciente': novo_paciente.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/pacientes', methods=['GET'])
@jwt_required()
def listar_pacientes():
    try:
        # Parâmetros de paginação
        pagina = request.args.get('pagina', 1, type=int)
        por_pagina = request.args.get('por_pagina', 10, type=int)
        
        # Limitar o número de itens por página
        if por_pagina > 100:
            por_pagina = 100
        
        # Query base
        query = Paciente.query.filter_by(ativo=True)
        
        # Paginação
        paginacao = query.paginate(
            page=pagina, 
            per_page=por_pagina, 
            error_out=False
        )
        
        return jsonify({
            'pacientes': [paciente.to_dict() for paciente in paginacao.items],
            'paginacao': {
                'pagina_atual': paginacao.page,
                'total_paginas': paginacao.pages,
                'total_itens': paginacao.total,
                'itens_por_pagina': por_pagina,
                'tem_proxima': paginacao.has_next,
                'tem_anterior': paginacao.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/pacientes/<int:paciente_id>', methods=['GET'])
@jwt_required()
def obter_paciente(paciente_id):
    try:
        paciente = Paciente.query.get_or_404(paciente_id)
        return jsonify({'paciente': paciente.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/pacientes/<int:paciente_id>', methods=['PUT'])
@jwt_required()
def atualizar_paciente(paciente_id):
    try:
        data = request.get_json()
        paciente = Paciente.query.get_or_404(paciente_id)
        
        # Atualizar campos
        if 'nome' in data:
            paciente.nome = data['nome']
        if 'cpf' in data:
            # Validar CPF
            if not validar_cpf(data['cpf']):
                return jsonify({'erro': 'CPF inválido'}), 400
            
            # Verificar se CPF já existe em outro paciente
            paciente_existente = Paciente.query.filter_by(cpf=data['cpf']).first()
            if paciente_existente and paciente_existente.id != paciente_id:
                return jsonify({'erro': 'CPF já cadastrado'}), 400
            paciente.cpf = data['cpf']
        if 'data_nascimento' in data:
            paciente.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        if 'telefone' in data:
            paciente.telefone = data['telefone']
        if 'email' in data:
            paciente.email = data['email']
        if 'endereco' in data:
            paciente.endereco = data['endereco']
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Paciente atualizado com sucesso',
            'paciente': paciente.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/pacientes/<int:paciente_id>', methods=['DELETE'])
@jwt_required()
def remover_paciente(paciente_id):
    try:
        usuario_atual_id = get_jwt_identity()
        usuario_atual = Usuario.query.get(usuario_atual_id)
        
        # Verificar se o usuário atual é admin ou recepcionista
        if usuario_atual.tipo_usuario not in ['admin', 'recepcionista']:
            return jsonify({'erro': 'Apenas administradores e recepcionistas podem remover pacientes'}), 403
        
        paciente = Paciente.query.get_or_404(paciente_id)
        
        # Soft delete - marcar como inativo
        paciente.ativo = False
        db.session.commit()
        
        return jsonify({'mensagem': 'Paciente removido com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/pacientes/buscar', methods=['GET'])
@jwt_required()
def buscar_pacientes():
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'erro': 'Parâmetro de busca é obrigatório'}), 400
        
        # Buscar por nome ou CPF
        pacientes = Paciente.query.filter(
            Paciente.ativo == True,
            (Paciente.nome.contains(query)) | (Paciente.cpf.contains(query))
        ).all()
        
        return jsonify({
            'pacientes': [paciente.to_dict() for paciente in pacientes]
        }), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

# Rotas de Consultas
@app.route('/api/consultas', methods=['POST'])
@jwt_required()
def criar_consulta():
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['paciente_id', 'medico_id', 'data_consulta', 'tipo_consulta']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
        
        # Verificar se paciente e médico existem
        paciente = Paciente.query.get(data['paciente_id'])
        medico = Usuario.query.get(data['medico_id'])
        
        if not paciente:
            return jsonify({'erro': 'Paciente não encontrado'}), 404
        if not medico or medico.tipo_usuario != 'medico':
            return jsonify({'erro': 'Médico não encontrado'}), 404
        
        # Criar nova consulta
        nova_consulta = Consulta(
            paciente_id=data['paciente_id'],
            medico_id=data['medico_id'],
            data_consulta=datetime.strptime(data['data_consulta'], '%Y-%m-%d %H:%M'),
            tipo_consulta=data['tipo_consulta'],
            observacoes=data.get('observacoes')
        )
        
        db.session.add(nova_consulta)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Consulta criada com sucesso',
            'consulta': nova_consulta.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/consultas', methods=['GET'])
@jwt_required()
def listar_consultas():
    try:
        # Parâmetros de paginação
        pagina = request.args.get('pagina', 1, type=int)
        por_pagina = request.args.get('por_pagina', 10, type=int)
        
        # Limitar o número de itens por página
        if por_pagina > 100:
            por_pagina = 100
        
        # Query base
        query = Consulta.query
        
        # Paginação
        paginacao = query.paginate(
            page=pagina, 
            per_page=por_pagina, 
            error_out=False
        )
        
        return jsonify({
            'consultas': [consulta.to_dict() for consulta in paginacao.items],
            'paginacao': {
                'pagina_atual': paginacao.page,
                'total_paginas': paginacao.pages,
                'total_itens': paginacao.total,
                'itens_por_pagina': por_pagina,
                'tem_proxima': paginacao.has_next,
                'tem_anterior': paginacao.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/consultas/<int:consulta_id>', methods=['GET'])
@jwt_required()
def obter_consulta(consulta_id):
    try:
        consulta = Consulta.query.get_or_404(consulta_id)
        return jsonify({'consulta': consulta.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/consultas/<int:consulta_id>', methods=['PUT'])
@jwt_required()
def atualizar_consulta(consulta_id):
    try:
        data = request.get_json()
        usuario_atual_id = get_jwt_identity()
        usuario_atual = Usuario.query.get(usuario_atual_id)
        
        consulta = Consulta.query.get_or_404(consulta_id)
        
        # Verificar se o usuário pode atualizar a consulta
        if usuario_atual.tipo_usuario not in ['admin', 'medico'] and consulta.medico_id != usuario_atual_id:
            return jsonify({'erro': 'Você só pode atualizar suas próprias consultas'}), 403
        
        # Atualizar campos
        if 'paciente_id' in data:
            # Verificar se paciente existe
            paciente = Paciente.query.get(data['paciente_id'])
            if not paciente:
                return jsonify({'erro': 'Paciente não encontrado'}), 404
            consulta.paciente_id = data['paciente_id']
        
        if 'medico_id' in data:
            # Verificar se médico existe
            medico = Usuario.query.get(data['medico_id'])
            if not medico or medico.tipo_usuario != 'medico':
                return jsonify({'erro': 'Médico não encontrado'}), 404
            consulta.medico_id = data['medico_id']
        
        if 'data_consulta' in data:
            consulta.data_consulta = datetime.strptime(data['data_consulta'], '%Y-%m-%d %H:%M')
        
        if 'tipo_consulta' in data:
            consulta.tipo_consulta = data['tipo_consulta']
        
        if 'observacoes' in data:
            consulta.observacoes = data['observacoes']
        
        if 'status' in data:
            if data['status'] not in ['agendada', 'realizada', 'cancelada']:
                return jsonify({'erro': 'Status inválido'}), 400
            consulta.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Consulta atualizada com sucesso',
            'consulta': consulta.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/consultas/<int:consulta_id>', methods=['DELETE'])
@jwt_required()
def remover_consulta(consulta_id):
    try:
        usuario_atual_id = get_jwt_identity()
        usuario_atual = Usuario.query.get(usuario_atual_id)
        
        consulta = Consulta.query.get_or_404(consulta_id)
        
        # Verificar se o usuário pode remover a consulta
        if usuario_atual.tipo_usuario not in ['admin', 'recepcionista'] and consulta.medico_id != usuario_atual_id:
            return jsonify({'erro': 'Você só pode remover suas próprias consultas'}), 403
        
        # Verificar se a consulta pode ser removida (apenas agendadas)
        if consulta.status == 'realizada':
            return jsonify({'erro': 'Não é possível remover uma consulta já realizada'}), 400
        
        db.session.delete(consulta)
        db.session.commit()
        
        return jsonify({'mensagem': 'Consulta removida com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/consultas/buscar', methods=['GET'])
@jwt_required()
def buscar_consultas():
    try:
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        medico_id = request.args.get('medico_id')
        status = request.args.get('status')
        
        query = Consulta.query
        
        # Filtrar por data
        if data_inicio:
            try:
                data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
                query = query.filter(Consulta.data_consulta >= data_inicio_dt)
            except ValueError:
                return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        if data_fim:
            try:
                data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
                # Adicionar 23:59:59 para incluir o dia inteiro
                data_fim_dt = data_fim_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(Consulta.data_consulta <= data_fim_dt)
            except ValueError:
                return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        # Filtrar por médico
        if medico_id:
            try:
                medico_id = int(medico_id)
                query = query.filter(Consulta.medico_id == medico_id)
            except ValueError:
                return jsonify({'erro': 'ID do médico deve ser um número'}), 400
        
        # Filtrar por status
        if status:
            if status not in ['agendada', 'realizada', 'cancelada']:
                return jsonify({'erro': 'Status inválido'}), 400
            query = query.filter(Consulta.status == status)
        
        consultas = query.all()
        
        return jsonify({
            'consultas': [consulta.to_dict() for consulta in consultas]
        }), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

# Rota de saúde da API
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'mensagem': 'API do Consultório Médico funcionando corretamente',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
