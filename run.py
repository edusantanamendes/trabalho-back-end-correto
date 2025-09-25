#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização rápida do Consultório Médico
Execute este script para configurar e executar a aplicação
"""

import subprocess
import sys
import os

def instalar_dependencias():
    """Instala as dependências do projeto"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def inicializar_banco():
    """Inicializa o banco de dados"""
    print("🗄️ Inicializando banco de dados...")
    try:
        subprocess.check_call([sys.executable, "init_db.py"])
        print("✅ Banco de dados inicializado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao inicializar banco de dados")
        return False

def executar_aplicacao():
    """Executa a aplicação Flask"""
    print("🚀 Iniciando aplicação...")
    print("📡 API disponível em: http://localhost:5000")
    print("🔑 Usuários de exemplo:")
    print("   - Admin: joao.silva@consultorio.com / 123456")
    print("   - Médico: maria.santos@consultorio.com / 123456")
    print("   - Recepcionista: ana.oliveira@consultorio.com / 123456")
    print("\n⏹️ Para parar a aplicação, pressione Ctrl+C")
    print("=" * 60)
    
    try:
        subprocess.check_call([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar aplicação")

def main():
    """Função principal"""
    print("=" * 60)
    print("🏥 CONSULTÓRIO MÉDICO - API REST")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Execute este script no diretório do projeto")
        print("   Certifique-se de que os arquivos app.py, requirements.txt estão presentes")
        return
    
    # Instalar dependências
    if not instalar_dependencias():
        return
    
    # Inicializar banco de dados
    if not inicializar_banco():
        return
    
    # Executar aplicação
    executar_aplicacao()

if __name__ == "__main__":
    main()
