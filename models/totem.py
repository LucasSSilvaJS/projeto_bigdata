import hashlib
from datetime import datetime

class Totem:
    def __init__(self, latitude: float, longitude: float, totem_id: str = None):
        self.latitude = latitude
        self.longitude = longitude
        self.totem_id = totem_id or self._gerar_id()
        self.data_criacao = datetime.now().isoformat()

    def _gerar_id(self):
        """Gera um ID único baseado nas coordenadas e timestamp"""
        timestamp = str(datetime.now().timestamp())
        dados = f"{self.latitude}_{self.longitude}_{timestamp}"
        return hashlib.md5(dados.encode()).hexdigest()[:12]

    def to_dict(self):
        return {
            "totem_id": self.totem_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "data_criacao": self.data_criacao
        }
