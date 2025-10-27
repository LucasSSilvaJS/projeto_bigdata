class Usuario:
    def __init__(self, vem_hash: str, pontuacao: int = 0):
        self.vem_hash = vem_hash
        self.pontuacao = pontuacao

    def to_dict(self):
        return {
            "vem_hash": self.vem_hash,
            "pontuacao": self.pontuacao
        }
