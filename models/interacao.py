class Interacao:
    def __init__(self, vem_hash: str, pergunta_id: str, totem_id: str, resposta: str):
        if resposta not in ["sim", "não"]:
            raise ValueError("Resposta deve ser 'sim' ou 'não'")

        self.vem_hash = vem_hash
        self.pergunta_id = pergunta_id
        self.totem_id = totem_id
        self.resposta = resposta

    def to_dict(self):
        return {
            "vem_hash": self.vem_hash,
            "pergunta_id": self.pergunta_id,
            "totem_id": self.totem_id,
            "resposta": self.resposta
        }
