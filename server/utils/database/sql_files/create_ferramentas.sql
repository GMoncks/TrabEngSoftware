-- Active: 1747592286665@@127.0.0.1@3306
CREATE TABLE "FERRAMENTAS" (
    "ID_FERRAMENTA" INTEGER PRIMARY KEY AUTOINCREMENT, -- ID da ferramenta, auto-incrementado
    "DT_CADASTRO" TIMESTAMP DEFAULT (DATETIME('now', '-3 hours')) NOT NULL, -- Data de cadastro da ferramenta no fuso de Brasília
    "NOME" TEXT NOT NULL, -- Nome da ferramenta
    "DESCRICAO" TEXT DEFAULT NULL, -- Descrição da ferramenta, padrão é NULL
    "ID_USUARIO" INTEGER NOT NULL -- FK para ID_USUARIO da tabela USUARIOS
);
