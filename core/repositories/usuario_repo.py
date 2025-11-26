from core.database import MongoConnection
from models.usuario import Usuario
from typing import Optional, List
from datetime import datetime

class UsuarioRepository:
    def __init__(self):
        self.collection = MongoConnection().get_collection("usuarios")

    def save(self, usuario: Usuario) -> None:
        """
        Salva ou atualiza um usuário no banco de dados.
        Usa upsert para criar se não existir ou atualizar se já existir.
        """
        # CORREÇÃO: usar model_dump(mode='json') ao invés de to_dict()
        usuario_dict = usuario.model_dump(mode='json')
        
        self.collection.update_one(
            {"vem_hash": usuario.vem_hash},
            {"$set": usuario_dict},
            upsert=True
        )

    def get_all(self) -> List[dict]:
        """
        Retorna todos os usuários cadastrados
        """
        return list(self.collection.find({}, {"_id": 0}))

    def get_by_vem_hash(self, vem_hash: str) -> Optional[dict]:
        """
        Busca um usuário específico pelo hash único
        """
        return self.collection.find_one({"vem_hash": vem_hash}, {"_id": 0})

    def delete(self, vem_hash: str) -> None:
        """
        Remove um usuário do banco de dados
        """
        self.collection.delete_one({"vem_hash": vem_hash})

    def set_points(self, vem_hash: str, points: int) -> None:
        """
        Atualiza apenas a pontuação de um usuário
        """
        self.collection.update_one(
            {"vem_hash": vem_hash},
            {"$set": {"pontuacao": points}}
        )
    
    def update(self, vem_hash: str, usuario_data: dict) -> bool:
        """
        Atualiza os dados completos de um usuário.
        Retorna True se atualizou com sucesso, False se usuário não existe.
        """
        result = self.collection.update_one(
            {"vem_hash": vem_hash},
            {"$set": usuario_data}
        )
        return result.modified_count > 0 or result.matched_count > 0
    
    def update_timestamp(self, vem_hash: str) -> None:
        """
        Atualiza apenas o timestamp de última atualização
        """
        self.collection.update_one(
            {"vem_hash": vem_hash},
            {"$set": {"ultima_atualizacao": datetime.utcnow().isoformat()}}
        )
    
    def update_partial(self, vem_hash: str, fields: dict) -> bool:
        """
        Atualiza campos específicos de um usuário.
        Útil para atualizações parciais sem sobrescrever tudo.
        """
        if not fields:
            return False
        
        # Adiciona timestamp de atualização automaticamente
        fields["ultima_atualizacao"] = datetime.utcnow().isoformat()
        
        result = self.collection.update_one(
            {"vem_hash": vem_hash},
            {"$set": fields}
        )
        return result.modified_count > 0
    
    def increment_points(self, vem_hash: str, points: int) -> Optional[int]:
        """
        Incrementa (ou decrementa) pontos usando operador atômico do MongoDB.
        Retorna a nova pontuação ou None se usuário não existe.
        """
        result = self.collection.find_one_and_update(
            {"vem_hash": vem_hash},
            {
                "$inc": {"pontuacao": points},
                "$set": {"ultima_atualizacao": datetime.utcnow().isoformat()}
            },
            projection={"pontuacao": 1, "_id": 0},
            return_document=True
        )
        
        if result:
            return result.get("pontuacao")
        return None
    
    def exists(self, vem_hash: str) -> bool:
        """
        Verifica se um usuário existe no banco
        """
        return self.collection.count_documents({"vem_hash": vem_hash}, limit=1) > 0
    
    def get_usuarios_com_cadastro_completo(self) -> List[dict]:
        """
        Retorna apenas usuários que completaram o cadastro
        """
        return list(self.collection.find(
            {"cadastro_completo": True},
            {"_id": 0}
        ))
    
    def get_usuarios_sem_cadastro_completo(self) -> List[dict]:
        """
        Retorna usuários que ainda não completaram o cadastro
        """
        return list(self.collection.find(
            {"cadastro_completo": False},
            {"_id": 0}
        ))
    
    def count_total(self) -> int:
        """
        Conta o total de usuários cadastrados
        """
        return self.collection.count_documents({})
    
    def count_cadastros_completos(self) -> int:
        """
        Conta quantos usuários completaram o cadastro
        """
        return self.collection.count_documents({"cadastro_completo": True})