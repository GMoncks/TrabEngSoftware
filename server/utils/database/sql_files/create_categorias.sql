CREATE TABLE CATEGORIAS (
    id_categoria   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome_categoria TEXT    NOT NULL
);

INSERT INTO CATEGORIAS (nome_categoria, id_categoria)
VALUES
    ('Tesoura', 1),
    ('Pá', 2),
    ('Esmerilhadeira', 3),
    ('Lixadeira', 4),
    ('Parafusadeira', 5),
    ('Furradeira', 6),
    ('Marreta', 7),
    ('Trena', 8),
    ('Chave Phillips', 9),
    ('Serra', 10),
    ('Alicate', 11),
    ('Chave de Fenda', 12),
    ('Martelo', 13);