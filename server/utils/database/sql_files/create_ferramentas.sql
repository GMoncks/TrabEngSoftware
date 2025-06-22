-- Active: 1747592286665@@127.0.0.1@3306
CREATE TABLE "FERRAMENTAS" (
    "ID_FERRAMENTA" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "NOME" VARCHAR(255) NOT NULL,
    "DESCRICAO" TEXT NOT NULL,
    "ID_CATEGORIA" INTEGER NOT NULL,
    "DT_CADASTRO" TIMESTAMP DEFAULT (DATETIME('now', '-3 hours')) NOT NULL,
    "ID_USUARIO" INTEGER NOT NULL, -- Usuário que cadastrou a ferramenta
    "FERRAMENTA_DISPONIVEL" INT DEFAULT 1 NOT NULL, -- Ferramenta disponível para empréstimo no presente momento
    "FOTO" TEXT DEFAULT NULL -- URL da foto da ferramenta
);

INSERT INTO FERRAMENTAS (
    FOTO,
    FERRAMENTA_DISPONIVEL,
    ID_USUARIO,
    DT_CADASTRO,
    ID_CATEGORIA,
    DESCRICAO,
    NOME,
    ID_FERRAMENTA
)
VALUES
    (
        'https://madeirasgasometro.vtexassets.com/arquivos/ids/176481/parafusadeira-ld12sc-imagem-01.jpg',
        1,
        1,
        '2025-06-22 18:45:00',
        5,
        'Parafusadeira em bom estado',
        'Parafusadeira',
        2
    ),
    (
        'https://eletrorastro.fbitsstatic.net/img/p/martelo-unha-27mm-vonder-80167/267270.jpg',
        1,
        1,
        '2025-06-22 18:45:00',
        13,
        'Martelo em bom estado',
        'Martelo',
        1
    );