#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inicialização do banco de dados do Consultório Médico
Este script cria as tabelas e insere dados de exemplo
"""

from app import app, db, Usuario, Paciente, Consulta
from werkzeug.security import generate_password_hash
from datetime import datetime, date

def criar_dados_exemplo():
    """Cria dados de exemplo no banco de dados"""
    
    print("Criando dados de exemplo...")
    
    # Criar usuários de exemplo
    usuarios_exemplo = [
        {
            'nome': 'Dr. João Silva',
            'email': 'joao.silva@consultorio.com',
            'senha': '123456',
            'tipo_usuario': 'admin',
            'telefone': '(11) 99999-9999',
            'endereco': 'Rua das Flores, 123 - São Paulo/SP'
        },
        {
            'nome': 'Dra. Maria Santos',
            'email': 'maria.santos@consultorio.com',
            'senha': '123456',
            'tipo_usuario': 'medico',
            'telefone': '(11) 88888-8888',
            'endereco': 'Av. Paulista, 456 - São Paulo/SP'
        },
        {
            'nome': 'Dr. Pedro Costa',
            'email': 'pedro.costa@consultorio.com',
            'senha': '123456',
            'tipo_usuario': 'medico',
            'telefone': '(11) 77777-7777',
            'endereco': 'Rua Augusta, 789 - São Paulo/SP'
        },
        {
            'nome': 'Ana Oliveira',
            'email': 'ana.oliveira@consultorio.com',
            'senha': '123456',
            'tipo_usuario': 'recepcionista',
            'telefone': '(11) 66666-6666',
            'endereco': 'Rua Consolação, 321 - São Paulo/SP'
        }
    ]
    
    for user_data in usuarios_exemplo:
        # Verificar se usuário já existe
        if not Usuario.query.filter_by(email=user_data['email']).first():
            usuario = Usuario(
                nome=user_data['nome'],
                email=user_data['email'],
                senha_hash=generate_password_hash(user_data['senha']),
                tipo_usuario=user_data['tipo_usuario'],
                telefone=user_data['telefone'],
                endereco=user_data['endereco']
            )
            db.session.add(usuario)
            print(f"✓ Usuário criado: {user_data['nome']}")
        else:
            print(f"- Usuário já existe: {user_data['nome']}")
    
    # Criar pacientes de exemplo
    pacientes_exemplo = [
        {
            'nome': 'Carlos Eduardo Silva',
            'cpf': '123.456.789-01',
            'data_nascimento': date(1985, 3, 15),
            'telefone': '(11) 55555-5555',
            'email': 'carlos.silva@email.com',
            'endereco': 'Rua das Palmeiras, 100 - São Paulo/SP'
        },
        {
            'nome': 'Fernanda Lima',
            'cpf': '987.654.321-02',
            'data_nascimento': date(1990, 7, 22),
            'telefone': '(11) 44444-4444',
            'email': 'fernanda.lima@email.com',
            'endereco': 'Av. Brasil, 200 - São Paulo/SP'
        },
        {
            'nome': 'Roberto Alves',
            'cpf': '456.789.123-03',
            'data_nascimento': date(1978, 11, 8),
            'telefone': '(11) 33333-3333',
            'email': 'roberto.alves@email.com',
            'endereco': 'Rua das Acácias, 300 - São Paulo/SP'
        },
        {
            'nome': 'Patricia Souza',
            'cpf': '789.123.456-04',
            'data_nascimento': date(1992, 5, 30),
            'telefone': '(11) 22222-2222',
            'email': 'patricia.souza@email.com',
            'endereco': 'Av. Faria Lima, 400 - São Paulo/SP'
        },
        {
            'nome': 'Marcos Pereira',
            'cpf': '321.654.987-05',
            'data_nascimento': date(1988, 12, 12),
            'telefone': '(11) 11111-1111',
            'email': 'marcos.pereira@email.com',
            'endereco': 'Rua dos Pinheiros, 500 - São Paulo/SP'
        }
    ]
    
    for paciente_data in pacientes_exemplo:
        # Verificar se paciente já existe
        if not Paciente.query.filter_by(cpf=paciente_data['cpf']).first():
            paciente = Paciente(**paciente_data)
            db.session.add(paciente)
            print(f"✓ Paciente criado: {paciente_data['nome']}")
        else:
            print(f"- Paciente já existe: {paciente_data['nome']}")
    
    # Commit das alterações
    db.session.commit()
    
    # Criar consultas de exemplo
    consultas_exemplo = [
        {
            'paciente_id': 1,
            'medico_id': 2,
            'data_consulta': datetime(2024, 1, 15, 9, 0),
            'tipo_consulta': 'Consulta de Rotina',
            'observacoes': 'Paciente com histórico de hipertensão',
            'status': 'realizada'
        },
        {
            'paciente_id': 2,
            'medico_id': 2,
            'data_consulta': datetime(2024, 1, 15, 10, 30),
            'tipo_consulta': 'Consulta Cardiológica',
            'observacoes': 'Dor no peito e falta de ar',
            'status': 'realizada'
        },
        {
            'paciente_id': 3,
            'medico_id': 3,
            'data_consulta': datetime(2024, 1, 16, 14, 0),
            'tipo_consulta': 'Consulta Dermatológica',
            'observacoes': 'Manchas na pele',
            'status': 'agendada'
        },
        {
            'paciente_id': 4,
            'medico_id': 2,
            'data_consulta': datetime(2024, 1, 17, 8, 30),
            'tipo_consulta': 'Consulta de Rotina',
            'observacoes': 'Check-up anual',
            'status': 'agendada'
        },
        {
            'paciente_id': 5,
            'medico_id': 3,
            'data_consulta': datetime(2024, 1, 18, 16, 0),
            'tipo_consulta': 'Consulta Dermatológica',
            'observacoes': 'Seguimento de tratamento',
            'status': 'agendada'
        }
    ]
    
    for consulta_data in consultas_exemplo:
        consulta = Consulta(**consulta_data)
        db.session.add(consulta)
        print(f"✓ Consulta criada: {consulta_data['tipo_consulta']} - {consulta_data['data_consulta']}")
    
    # Commit final
    db.session.commit()
    print("\n✓ Dados de exemplo criados com sucesso!")
    print("\nUsuários de exemplo:")
    print("- Email: joao.silva@consultorio.com | Senha: 123456 | Tipo: Admin")
    print("- Email: maria.santos@consultorio.com | Senha: 123456 | Tipo: Médico")
    print("- Email: pedro.costa@consultorio.com | Senha: 123456 | Tipo: Médico")
    print("- Email: ana.oliveira@consultorio.com | Senha: 123456 | Tipo: Recepcionista")

def main():
    """Função principal"""
    print("=== Inicialização do Banco de Dados do Consultório Médico ===\n")
    
    with app.app_context():
        # Criar todas as tabelas
        print("Criando tabelas do banco de dados...")
        db.create_all()
        print("✓ Tabelas criadas com sucesso!\n")
        
        # Criar dados de exemplo
        criar_dados_exemplo()
        
        print("\n=== Inicialização concluída! ===")
        print("Agora você pode executar: python app.py")

if __name__ == '__main__':
    main()
