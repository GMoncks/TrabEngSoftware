CREATE TABLE STATUS (
    ID_STATUS   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    NOME_STATUS TEXT    NOT NULL
);

INSERT INTO STATUS (NOME_STATUS)
VALUES
    ('Aguardando autorização'),
    ('Não Autorizado'),
    ('Emprestado'),
    ('Devolvido');