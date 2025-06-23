CREATE TABLE "REGISTROS" (
    "ID_REGISTRO" INTEGER PRIMARY KEY AUTOINCREMENT,
    "ID_FERRAMENTA" integer NOT NULL, -- Ferramenta emprestada
    "ID_USUARIO" INTEGER NOT NULL, -- Usuario que fez o empréstimo
    "DT_EMPRESTIMO" TIMESTAMP NOT NULL, -- Data do empréstimo
    "DT_DEVOLUCAO" TIMESTAMP, -- Data da devolução
    "ID_STATUS" INT DEFAULT 1 NOT NULL, -- Status do empréstimo
    "DT_REGISTRO" TIMESTAMP DEFAULT (DATETIME('now', '-3 hours')) NOT NULL -- Data do registro do empréstimo
);

-- usuário 1 cadastra a ferramenta
-- usuario 2 vai ver a ferramenta no sistema
-- Usuario 2 vai solicitar o empréstimo (ou "reservar")
-- Na tabela REGISTROS:
--      ID_REGISTRO, ID_FERRAMENTA, ID_USUARIO, DT_EMPRESTIMO, DT_DEVOLUCAO, ID_STATUS = 1

-- Usuario 1 vai ver a solicitação de empréstimo
-- Usuario 1 vai aceitar o empréstimo
-- Na tabela REGISTROS:
--      UPDATE ID_STATUS = 3
-- Na tabela FERRAMENTAS:
--      UPDATE FERRAMENTA_DISPONIVEL = 0

-- Usuario 2 vai ver que o empréstimo foi aceito (pq ID_STATUS = 3)
--     "Ver" quer dizer que na aba de "Meus Empréstimos" vai ser mostrados todos os registros que tem o ID_USUARIO do usuario 2 
-- Usuario 2 vai retirar a ferramenta
-- Usuario 2 vai devolver a ferramenta
-- Na tabela REGISTROS:
--      UPDATE DT_DEVOLUCAO = data_atual, ID_STATUS = 4
-- Na tabela FERRAMENTAS:
--      UPDATE FERRAMENTA_DISPONIVEL = 1

INSERT INTO REGISTROS (
    DT_REGISTRO,
    DT_DEVOLUCAO,
    DT_EMPRESTIMO,
    ID_USUARIO,
    ID_FERRAMENTA,
    ID_REGISTRO
)
VALUES (
    '2025-06-22 17:45:42',
    '2025-06-26 18:45:42',
    '2025-06-22 18:45:42',
    1,
    1,
    1
);

