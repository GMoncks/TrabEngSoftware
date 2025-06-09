-- Active: 1747592286665@@127.0.0.1@3306
CREATE TABLE "USUARIOS" (
    "ID_USUARIO" INTEGER PRIMARY KEY AUTOINCREMENT, -- ID do usuário, auto-incrementado
    "DT_CADASTRO" TIMESTAMP DEFAULT (DATETIME('now', '-3 hours')) NOT NULL, -- Data de cadastro do usuário no fuso de Brasília
    "EMAIL" TEXT NOT NULL UNIQUE, -- Email do usuário, deve ser único
    "SENHA" TEXT NOT NULL, -- Senha mascarada
    "NOME" TEXT NOT NULL, -- Nome do usuário
    "HOME_ID" TEXT DEFAULT NULL,
    "CPF" TEXT NOT NULL UNIQUE, -- CPF do usuário, deve ser único
    "PHONE" TEXT NOT NULL UNIQUE, -- Telefone do usuário, deve ser único
    "SCORE" INTEGER DEFAULT 0 NOT NULL, -- Pontuação do usuário, padrão é 0
    "ADMIN" INTEGER DEFAULT 0 NOT NULL, -- Indica se o usuário é administrador, padrão é 0 (não é administrador)
    "DT_ULTIMO_ACESSO" TIMESTAMP DEFAULT (DATETIME('now', '-3 hours')) NOT NULL -- Data do último acesso do usuário, padrão é a data atual
);

INSERT INTO "USUARIOS" ("EMAIL", "SENHA", "NOME", "CPF", "PHONE", "ADMIN")
VALUES ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Administrador', '0', '0', 1);