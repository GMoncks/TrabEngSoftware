-- Active: 1747592286665@@127.0.0.1@3306
CREATE TABLE "REGISTROS" (
    "ID_REGISTRO" INTEGER PRIMARY KEY AUTOINCREMENT, -- ID do registro, auto-incrementado
    "DT_REGISTRO" TIMESTAMP DEFAULT (DATETIME('now', '-3 hours')) NOT NULL, -- Data do registro no fuso de Brasília
    "ID_USUARIO" INTEGER NOT NULL, -- FK para ID_USUARIO da tabela USUARIOS
    "ID_FERRAMENTA" INTEGER NOT NULL, -- FK para ID_FERRAMENTA da tabela FERRAMENTAS
    "DT_INICIO_EMPRESTIMO" TIMESTAMP NOT NULL, -- Data de início do empréstimo da ferramenta
    "DT_FIM_EMPRESTIMO" TIMESTAMP NOT NULL -- Data de fim do empréstimo da ferramenta
);