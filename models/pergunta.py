import hashlib
from datetime import datetime

class Pergunta:
    def __init__(self, texto: str, pergunta_id: str = None):
        self.texto = texto
        self.pergunta_id = pergunta_id or self._gerar_id()
        self.data_criacao = datetime.now().isoformat()

    def _gerar_id(self):
        """Gera um ID único baseado no texto e timestamp"""
        timestamp = str(datetime.now().timestamp())
        dados = f"{self.texto}_{timestamp}"
        return hashlib.md5(dados.encode()).hexdigest()[:12]

    def to_dict(self):
        return {
            "pergunta_id": self.pergunta_id,
            "texto": self.texto,
            "data_criacao": self.data_criacao
        }
