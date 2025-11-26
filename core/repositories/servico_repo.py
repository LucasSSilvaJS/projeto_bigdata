from core.database import MongoConnection
from models.servico import Servico
from typing import Optional, List

class ServicoRepository:
    def __init__(self):
        self.collection = MongoConnection().get_collection("servicos")

    def save(self, servico: Servico) -> None:
        """
        Salva ou atualiza um serviço no banco de dados
        """
        servico_dict = servico.model_dump(mode='json')
        
        self.collection.update_one(
            {"servico_id": servico.servico_id},
            {"$set": servico_dict},
            upsert=True
        )

    def get_all(self) -> List[dict]:
        """
        Retorna todos os serviços cadastrados
        """
        return list(self.collection.find({}, {"_id": 0}))

    def get_ativos(self) -> List[dict]:
        """
        Retorna apenas serviços ativos
        """
        return list(self.collection.find({"ativo": True}, {"_id": 0}))

    def get_by_id(self, servico_id: str) -> Optional[dict]:
        """
        Busca um serviço específico pelo ID
        """
        return self.collection.find_one({"servico_id": servico_id}, {"_id": 0})

    def get_by_tipo(self, tipo: str) -> List[dict]:
        """
        Busca serviços por tipo (Saúde, Transporte, Educação, etc)
        """
        return list(self.collection.find(
            {"tipo": tipo, "ativo": True},
            {"_id": 0}
        ))

    def get_por_localizacao(self, latitude: float, longitude: float, raio_km: float = 5.0) -> List[dict]:
        """
        Busca serviços próximos a uma localização usando índice geoespacial do MongoDB
        Nota: Requer índice 2dsphere criado no campo de localização
        """
        # MongoDB usa GeoJSON, então precisamos estruturar assim
        servicos = list(self.collection.find(
            {
                "ativo": True,
                "latitude": {"$exists": True},
                "longitude": {"$exists": True}
            },
            {"_id": 0}
        ))
        
        # Como não estamos usando GeoJSON completo, vamos filtrar manualmente
        # (Isso será otimizado no service com o método calcular_distancia)
        return servicos

    def delete(self, servico_id: str) -> None:
        """
        Remove um serviço do banco de dados
        """
        self.collection.delete_one({"servico_id": servico_id})

    def desativar(self, servico_id: str) -> bool:
        """
        Desativa um serviço ao invés de deletá-lo (soft delete)
        """
        result = self.collection.update_one(
            {"servico_id": servico_id},
            {"$set": {"ativo": False}}
        )
        return result.modified_count > 0

    def ativar(self, servico_id: str) -> bool:
        """
        Reativa um serviço
        """
        result = self.collection.update_one(
            {"servico_id": servico_id},
            {"$set": {"ativo": True}}
        )
        return result.modified_count > 0

    def update_partial(self, servico_id: str, campos: dict) -> bool:
        """
        Atualiza campos específicos de um serviço
        """
        from datetime import datetime
        
        if not campos:
            return False
        
        campos["ultima_atualizacao"] = datetime.utcnow().isoformat()
        
        result = self.collection.update_one(
            {"servico_id": servico_id},
            {"$set": campos}
        )
        return result.modified_count > 0

    def exists(self, servico_id: str) -> bool:
        """
        Verifica se um serviço existe
        """
        return self.collection.count_documents({"servico_id": servico_id}, limit=1) > 0

    def count_total(self) -> int:
        """
        Conta o total de serviços cadastrados
        """
        return self.collection.count_documents({})

    def count_ativos(self) -> int:
        """
        Conta quantos serviços estão ativos
        """
        return self.collection.count_documents({"ativo": True})

    def count_por_tipo(self) -> dict:
        """
        Retorna contagem de serviços agrupados por tipo
        """
        pipeline = [
            {"$match": {"ativo": True}},
            {"$group": {
                "_id": "$tipo",
                "total": {"$sum": 1}
            }},
            {"$sort": {"total": -1}}
        ]
        
        resultado = list(self.collection.aggregate(pipeline))
        return {item["_id"]: item["total"] for item in resultado}