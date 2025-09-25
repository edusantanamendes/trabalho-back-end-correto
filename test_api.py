#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para a API do Consultório Médico
Este script demonstra como usar todas as funcionalidades da API
"""

import requests
import json
from datetime import datetime

# Configuração da API
BASE_URL = 'http://localhost:5000/api'
HEADERS = {'Content-Type': 'application/json'}

class ConsultorioAPITest:
    def __init__(self):
        self.token = None
        self.headers = HEADERS.copy()
    
    def login(self, email, senha):
        """Realiza login e obtém token JWT"""
        url = f'{BASE_URL}/auth/login'
        data = {
            'email': email,
            'senha': senha
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result['access_token']
            self.headers['Authorization'] = f'Bearer {self.token}'
            print(f"✓ Login realizado com sucesso para: {email}")
            return True
        else:
            print(f"✗ Erro no login: {response.json()}")
            return False
    
    def test_health_check(self):
        """Testa o endpoint de saúde da API"""
        url = f'{BASE_URL}/health'
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✓ API está funcionando corretamente")
            return True
        else:
            print("✗ API não está respondendo")
            return False
    
    def criar_usuario(self, dados_usuario):
        """Cria um novo usuário"""
        url = f'{BASE_URL}/usuarios'
        response = requests.post(url, json=dados_usuario, headers=self.headers)
        
        if response.status_code == 201:
            print(f"✓ Usuário criado: {dados_usuario['nome']}")
            return response.json()
        else:
            print(f"✗ Erro ao criar usuário: {response.json()}")
            return None
    
    def listar_usuarios(self, pagina=1, por_pagina=10, tipo_usuario=None):
        """Lista todos os usuários com paginação"""
        url = f'{BASE_URL}/usuarios'
        params = {'pagina': pagina, 'por_pagina': por_pagina}
        if tipo_usuario:
            params['tipo_usuario'] = tipo_usuario
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data['usuarios']
            paginacao = data['paginacao']
            print(f"✓ Encontrados {paginacao['total_itens']} usuários (página {paginacao['pagina_atual']}/{paginacao['total_paginas']})")
            for usuario in usuarios:
                print(f"  - {usuario['nome']} ({usuario['tipo_usuario']})")
            return usuarios
        else:
            print(f"✗ Erro ao listar usuários: {response.json()}")
            return []
    
    def atualizar_usuario(self, usuario_id, dados_atualizacao):
        """Atualiza um usuário existente"""
        url = f'{BASE_URL}/usuarios/{usuario_id}'
        response = requests.put(url, json=dados_atualizacao, headers=self.headers)
        
        if response.status_code == 200:
            print(f"✓ Usuário {usuario_id} atualizado com sucesso")
            return response.json()
        else:
            print(f"✗ Erro ao atualizar usuário: {response.json()}")
            return None
    
    def remover_usuario(self, usuario_id):
        """Remove um usuário (soft delete)"""
        url = f'{BASE_URL}/usuarios/{usuario_id}'
        response = requests.delete(url, headers=self.headers)
        
        if response.status_code == 200:
            print(f"✓ Usuário {usuario_id} removido com sucesso")
            return True
        else:
            print(f"✗ Erro ao remover usuário: {response.json()}")
            return False
    
    def criar_paciente(self, dados_paciente):
        """Cria um novo paciente"""
        url = f'{BASE_URL}/pacientes'
        response = requests.post(url, json=dados_paciente, headers=self.headers)
        
        if response.status_code == 201:
            print(f"✓ Paciente criado: {dados_paciente['nome']}")
            return response.json()
        else:
            print(f"✗ Erro ao criar paciente: {response.json()}")
            return None
    
    def listar_pacientes(self, pagina=1, por_pagina=10):
        """Lista todos os pacientes com paginação"""
        url = f'{BASE_URL}/pacientes'
        params = {'pagina': pagina, 'por_pagina': por_pagina}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            pacientes = data['pacientes']
            paginacao = data['paginacao']
            print(f"✓ Encontrados {paginacao['total_itens']} pacientes (página {paginacao['pagina_atual']}/{paginacao['total_paginas']})")
            for paciente in pacientes:
                print(f"  - {paciente['nome']} (CPF: {paciente['cpf']})")
            return pacientes
        else:
            print(f"✗ Erro ao listar pacientes: {response.json()}")
            return []
    
    def criar_consulta(self, dados_consulta):
        """Cria uma nova consulta"""
        url = f'{BASE_URL}/consultas'
        response = requests.post(url, json=dados_consulta, headers=self.headers)
        
        if response.status_code == 201:
            print(f"✓ Consulta criada: {dados_consulta['tipo_consulta']}")
            return response.json()
        else:
            print(f"✗ Erro ao criar consulta: {response.json()}")
            return None
    
    def listar_consultas(self, pagina=1, por_pagina=10):
        """Lista todas as consultas com paginação"""
        url = f'{BASE_URL}/consultas'
        params = {'pagina': pagina, 'por_pagina': por_pagina}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            consultas = data['consultas']
            paginacao = data['paginacao']
            print(f"✓ Encontradas {paginacao['total_itens']} consultas (página {paginacao['pagina_atual']}/{paginacao['total_paginas']})")
            for consulta in consultas:
                print(f"  - {consulta['tipo_consulta']} - {consulta['data_consulta']}")
            return consultas
        else:
            print(f"✗ Erro ao listar consultas: {response.json()}")
            return []
    
    def obter_paciente(self, paciente_id):
        """Obtém um paciente específico"""
        url = f'{BASE_URL}/pacientes/{paciente_id}'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            paciente = response.json()['paciente']
            print(f"✓ Paciente obtido: {paciente['nome']}")
            return paciente
        else:
            print(f"✗ Erro ao obter paciente: {response.json()}")
            return None
    
    def atualizar_paciente(self, paciente_id, dados_atualizacao):
        """Atualiza um paciente existente"""
        url = f'{BASE_URL}/pacientes/{paciente_id}'
        response = requests.put(url, json=dados_atualizacao, headers=self.headers)
        
        if response.status_code == 200:
            print(f"✓ Paciente {paciente_id} atualizado com sucesso")
            return response.json()
        else:
            print(f"✗ Erro ao atualizar paciente: {response.json()}")
            return None
    
    def buscar_pacientes(self, query):
        """Busca pacientes por nome ou CPF"""
        url = f'{BASE_URL}/pacientes/buscar'
        params = {'q': query}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            pacientes = response.json()['pacientes']
            print(f"✓ Encontrados {len(pacientes)} pacientes para '{query}'")
            for paciente in pacientes:
                print(f"  - {paciente['nome']} (CPF: {paciente['cpf']})")
            return pacientes
        else:
            print(f"✗ Erro ao buscar pacientes: {response.json()}")
            return []
    
    def obter_consulta(self, consulta_id):
        """Obtém uma consulta específica"""
        url = f'{BASE_URL}/consultas/{consulta_id}'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            consulta = response.json()['consulta']
            print(f"✓ Consulta obtida: {consulta['tipo_consulta']}")
            return consulta
        else:
            print(f"✗ Erro ao obter consulta: {response.json()}")
            return None
    
    def atualizar_consulta(self, consulta_id, dados_atualizacao):
        """Atualiza uma consulta existente"""
        url = f'{BASE_URL}/consultas/{consulta_id}'
        response = requests.put(url, json=dados_atualizacao, headers=self.headers)
        
        if response.status_code == 200:
            print(f"✓ Consulta {consulta_id} atualizada com sucesso")
            return response.json()
        else:
            print(f"✗ Erro ao atualizar consulta: {response.json()}")
            return None
    
    def buscar_consultas(self, data_inicio=None, data_fim=None, medico_id=None, status=None):
        """Busca consultas com filtros"""
        url = f'{BASE_URL}/consultas/buscar'
        params = {}
        
        if data_inicio:
            params['data_inicio'] = data_inicio
        if data_fim:
            params['data_fim'] = data_fim
        if medico_id:
            params['medico_id'] = medico_id
        if status:
            params['status'] = status
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            consultas = response.json()['consultas']
            print(f"✓ Encontradas {len(consultas)} consultas com os filtros aplicados")
            for consulta in consultas:
                print(f"  - {consulta['tipo_consulta']} - {consulta['data_consulta']}")
            return consultas
        else:
            print(f"✗ Erro ao buscar consultas: {response.json()}")
            return []

def executar_testes():
    """Executa todos os testes da API"""
    print("=== TESTE DA API DO CONSULTÓRIO MÉDICO ===\n")
    
    # Inicializar cliente de teste
    cliente = ConsultorioAPITest()
    
    # Teste 1: Verificar saúde da API
    print("1. Testando saúde da API...")
    if not cliente.test_health_check():
        print("API não está funcionando. Certifique-se de que o servidor está rodando.")
        return
    
    # Teste 2: Login como administrador
    print("\n2. Realizando login como administrador...")
    if not cliente.login('joao.silva@consultorio.com', '123456'):
        print("Não foi possível fazer login. Execute init_db.py primeiro.")
        return
    
    # Teste 3: Listar usuários com paginação
    print("\n3. Listando usuários existentes com paginação...")
    usuarios = cliente.listar_usuarios(pagina=1, por_pagina=5)
    
    # Teste 4: Listar apenas médicos
    print("\n4. Listando apenas médicos...")
    medicos = cliente.listar_usuarios(tipo_usuario='medico')
    
    # Teste 5: Criar novo usuário
    print("\n5. Criando novo usuário...")
    novo_usuario = {
        'nome': 'Dr. Carlos Mendes',
        'email': 'carlos.mendes@consultorio.com',
        'senha': '123456',
        'tipo_usuario': 'medico',
        'telefone': '(11) 55555-1234',
        'endereco': 'Rua das Orquídeas, 500 - São Paulo/SP'
    }
    cliente.criar_usuario(novo_usuario)
    
    # Teste 6: Atualizar usuário
    print("\n6. Atualizando usuário...")
    cliente.atualizar_usuario(1, {'telefone': '(11) 99999-0000'})
    
    # Teste 7: Listar pacientes com paginação
    print("\n7. Listando pacientes com paginação...")
    pacientes = cliente.listar_pacientes(pagina=1, por_pagina=3)
    
    # Teste 8: Obter paciente específico
    print("\n8. Obtendo paciente específico...")
    cliente.obter_paciente(1)
    
    # Teste 9: Buscar pacientes
    print("\n9. Buscando pacientes por nome...")
    cliente.buscar_pacientes('Carlos')
    
    # Teste 10: Criar novo paciente com CPF válido
    print("\n10. Criando novo paciente...")
    novo_paciente = {
        'nome': 'João da Silva Santos',
        'cpf': '123.456.789-09',  # CPF válido
        'data_nascimento': '1990-01-15',
        'telefone': '(11) 99999-1111',
        'email': 'joao.santos@email.com',
        'endereco': 'Rua das Margaridas, 200 - São Paulo/SP'
    }
    cliente.criar_paciente(novo_paciente)
    
    # Teste 11: Atualizar paciente
    print("\n11. Atualizando paciente...")
    cliente.atualizar_paciente(1, {'telefone': '(11) 88888-8888'})
    
    # Teste 12: Listar consultas com paginação
    print("\n12. Listando consultas com paginação...")
    consultas = cliente.listar_consultas(pagina=1, por_pagina=3)
    
    # Teste 13: Obter consulta específica
    print("\n13. Obtendo consulta específica...")
    cliente.obter_consulta(1)
    
    # Teste 14: Buscar consultas por status
    print("\n14. Buscando consultas agendadas...")
    cliente.buscar_consultas(status='agendada')
    
    # Teste 15: Criar nova consulta
    print("\n15. Criando nova consulta...")
    nova_consulta = {
        'paciente_id': 1,
        'medico_id': 2,
        'data_consulta': '2024-02-01 14:30',
        'tipo_consulta': 'Consulta de Retorno',
        'observacoes': 'Paciente retornando para acompanhamento'
    }
    cliente.criar_consulta(nova_consulta)
    
    # Teste 16: Atualizar consulta
    print("\n16. Atualizando consulta...")
    cliente.atualizar_consulta(6, {'observacoes': 'Observações atualizadas'})
    
    # Teste 17: Tentar remover usuário (apenas admin pode)
    print("\n17. Testando remoção de usuário...")
    cliente.remover_usuario(5)  # Remove o usuário criado no teste 5
    
    print("\n=== TESTES CONCLUÍDOS ===")
    print("Todos os testes foram executados com sucesso!")
    print("\nPara testar manualmente, use as seguintes credenciais:")
    print("- Admin: joao.silva@consultorio.com / 123456")
    print("- Médico: maria.santos@consultorio.com / 123456")
    print("- Recepcionista: ana.oliveira@consultorio.com / 123456")

if __name__ == '__main__':
    executar_testes()
