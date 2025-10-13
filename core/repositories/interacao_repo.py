from core.database import MongoConnection

class InteracaoRepository:
    def __init__(self):
        self.collection = MongoConnection().get_collection("interacoes")

    def save(self, interacao):
        self.collection.update_one(
            {
                "vem_hash": interacao.vem_hash,
                "pergunta_id": interacao.pergunta_id,
                "totem_id": interacao.totem_id
            },
            {"$set": interacao.to_dict()},
            upsert=True
        )

    def get_all(self):
        return list(self.collection.find({}, {"_id": 0}))
