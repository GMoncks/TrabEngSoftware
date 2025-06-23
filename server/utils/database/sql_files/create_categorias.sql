CREATE TABLE CATEGORIAS (
    ID_CATEGORIA   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    NOME_CATEGORIA TEXT    NOT NULL
);

INSERT INTO CATEGORIAS (NOME_CATEGORIA)
VALUES
    ('Tesoura'),
    ('Pá'),
    ('Esmerilhadeira'),
    ('Lixadeira'),
    ('Parafusadeira'),
    ('Furradeira'),
    ('Marreta'),
    ('Trena'),
    ('Chave Phillips'),
    ('Serra'),
    ('Alicate'),
    ('Chave de Fenda'),
    ('Martelo');