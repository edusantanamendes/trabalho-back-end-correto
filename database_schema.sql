-- Script SQL para criação do banco de dados do Consultório Médico
-- Este script cria todas as tabelas necessárias e insere dados de exemplo

-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    tipo_usuario VARCHAR(20) NOT NULL CHECK (tipo_usuario IN ('admin', 'medico', 'recepcionista')),
    telefone VARCHAR(20),
    endereco VARCHAR(200),
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT 1
);

-- Criar tabela de pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(120),
    endereco VARCHAR(200),
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT 1
);

-- Criar tabela de consultas
CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    medico_id INTEGER NOT NULL,
    data_consulta DATETIME NOT NULL,
    tipo_consulta VARCHAR(50) NOT NULL,
    observacoes TEXT,
    status VARCHAR(20) DEFAULT 'agendada' CHECK (status IN ('agendada', 'realizada', 'cancelada')),
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (medico_id) REFERENCES usuarios(id)
);

-- Inserir dados de exemplo - Usuários
INSERT INTO usuarios (nome, email, senha_hash, tipo_usuario, telefone, endereco) VALUES
('Dr. João Silva', 'joao.silva@consultorio.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K', 'admin', '(11) 99999-9999', 'Rua das Flores, 123 - São Paulo/SP'),
('Dra. Maria Santos', 'maria.santos@consultorio.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K', 'medico', '(11) 88888-8888', 'Av. Paulista, 456 - São Paulo/SP'),
('Dr. Pedro Costa', 'pedro.costa@consultorio.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K', 'medico', '(11) 77777-7777', 'Rua Augusta, 789 - São Paulo/SP'),
('Ana Oliveira', 'ana.oliveira@consultorio.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K', 'recepcionista', '(11) 66666-6666', 'Rua Consolação, 321 - São Paulo/SP');

-- Inserir dados de exemplo - Pacientes
INSERT INTO pacientes (nome, cpf, data_nascimento, telefone, email, endereco) VALUES
('Carlos Eduardo Silva', '123.456.789-01', '1985-03-15', '(11) 55555-5555', 'carlos.silva@email.com', 'Rua das Palmeiras, 100 - São Paulo/SP'),
('Fernanda Lima', '987.654.321-02', '1990-07-22', '(11) 44444-4444', 'fernanda.lima@email.com', 'Av. Brasil, 200 - São Paulo/SP'),
('Roberto Alves', '456.789.123-03', '1978-11-08', '(11) 33333-3333', 'roberto.alves@email.com', 'Rua das Acácias, 300 - São Paulo/SP'),
('Patricia Souza', '789.123.456-04', '1992-05-30', '(11) 22222-2222', 'patricia.souza@email.com', 'Av. Faria Lima, 400 - São Paulo/SP'),
('Marcos Pereira', '321.654.987-05', '1988-12-12', '(11) 11111-1111', 'marcos.pereira@email.com', 'Rua dos Pinheiros, 500 - São Paulo/SP');

-- Inserir dados de exemplo - Consultas
INSERT INTO consultas (paciente_id, medico_id, data_consulta, tipo_consulta, observacoes, status) VALUES
(1, 2, '2024-01-15 09:00:00', 'Consulta de Rotina', 'Paciente com histórico de hipertensão', 'realizada'),
(2, 2, '2024-01-15 10:30:00', 'Consulta Cardiológica', 'Dor no peito e falta de ar', 'realizada'),
(3, 3, '2024-01-16 14:00:00', 'Consulta Dermatológica', 'Manchas na pele', 'agendada'),
(4, 2, '2024-01-17 08:30:00', 'Consulta de Rotina', 'Check-up anual', 'agendada'),
(5, 3, '2024-01-18 16:00:00', 'Consulta Dermatológica', 'Seguimento de tratamento', 'agendada');

-- Criar índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_tipo ON usuarios(tipo_usuario);
CREATE INDEX IF NOT EXISTS idx_pacientes_cpf ON pacientes(cpf);
CREATE INDEX IF NOT EXISTS idx_consultas_paciente ON consultas(paciente_id);
CREATE INDEX IF NOT EXISTS idx_consultas_medico ON consultas(medico_id);
CREATE INDEX IF NOT EXISTS idx_consultas_data ON consultas(data_consulta);

-- Comentários sobre a estrutura
-- 
-- TABELA USUARIOS:
-- - Armazena informações dos funcionários do consultório (médicos, recepcionistas, admin)
-- - Senhas são armazenadas com hash para segurança
-- - Campo 'ativo' permite soft delete
-- 
-- TABELA PACIENTES:
-- - Armazena informações dos pacientes
-- - CPF é único para evitar duplicatas
-- - Campo 'ativo' permite soft delete
-- 
-- TABELA CONSULTAS:
-- - Armazena informações das consultas agendadas
-- - Relaciona pacientes com médicos
-- - Status permite controle do fluxo da consulta
-- 
-- SENHAS PADRÃO (hash para '123456'):
-- Todos os usuários de exemplo têm a senha '123456'
-- Em produção, cada usuário deve definir sua própria senha
