from enum import Enum

class LoanStatus(Enum):
    AGUARDANDO_AUTORIZACAO = 1
    NAO_AUTORIZADO = 2
    EMPRESTADO = 3
    DEVOLVIDO = 4

    def label(self):
        """Retorna o nome legível do enum."""
        labels = {
            LoanStatus.AGUARDANDO_AUTORIZACAO: "Aguardando autorização",
            LoanStatus.NAO_AUTORIZADO: "Não Autorizado",
            LoanStatus.EMPRESTADO: "Emprestado",
            LoanStatus.DEVOLVIDO: "Devolvido",
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
            LoanStatus.AGUARDANDO_AUTORIZACAO: "Aguardando autorização",
            LoanStatus.NAO_AUTORIZADO: "Não Autorizado",
            LoanStatus.EMPRESTADO: "Emprestado",
            LoanStatus.DEVOLVIDO: "Devolvido",
        }
        return icons[self]
