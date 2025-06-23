from enum import Enum

class Tool(Enum):
    TESOURA = 1
    PA = 2
    ESMERILHADEIRA = 3
    LIXADEIRA = 4
    PARAFUSADEIRA = 5
    FURADEIRA = 6
    MARRETA = 7
    TRENA = 8
    CHAVE_PHILLIPS = 9
    SERRA = 10
    ALICATE = 11
    CHAVE_DE_FENDA = 12
    MARTELO = 13

    def label(self):
        """Retorna o nome legível do enum."""
        labels = {
            Tool.TESOURA: "Tesoura",
            Tool.PA: "Pá",
            Tool.ESMERILHADEIRA: "Esmerilhadeira",
            Tool.LIXADEIRA: "Lixadeira",
            Tool.PARAFUSADEIRA: "Parafusadeira",
            Tool.FURADEIRA: "Furadeira",
            Tool.MARRETA: "Marreta",
            Tool.TRENA: "Trena",
            Tool.CHAVE_PHILLIPS: "Chave Phillips",
            Tool.SERRA: "Serra",
            Tool.ALICATE: "Alicate",
            Tool.CHAVE_DE_FENDA: "Chave de Fenda",
            Tool.MARTELO: "Martelo",
        }
        return labels[self]

    @classmethod
    def from_value(cls, value: int):
        """Retorna a ferramenta correspondente ao valor numérico."""
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"Valor inválido: {value}. Deve estar entre 1 e {len(cls)}.")
        
    def icone(self):
        icons = {
            Tool.TESOURA: "Tesoura",
            Tool.PA: "Pá",
            Tool.ESMERILHADEIRA: "Esmerilhadeira",
            Tool.LIXADEIRA: "Lixadeira",
            Tool.PARAFUSADEIRA: "Parafusadeira",
            Tool.FURADEIRA: "Furadeira",
            Tool.MARRETA: "Marreta",
            Tool.TRENA: "Trena",
            Tool.CHAVE_PHILLIPS: "Chave Phillips",
            Tool.SERRA: "Serra",
            Tool.ALICATE: "Alicate",
            Tool.CHAVE_DE_FENDA: "Chave de Fenda",
            Tool.MARTELO: "Martelo",
        }
        return icons[self]
