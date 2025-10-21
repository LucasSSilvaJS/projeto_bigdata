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
    
    #transforme o score em percentual de respostas "sim" e "não"
    def get_score(self, pergunta_id):
        pipeline = [
            {"$match": {"pergunta_id": pergunta_id}},
            {
                "$group": {
                    "_id": "$resposta",
                    "count": {"$sum": 1}
                }
            }
        ]
        results = list(self.collection.aggregate(pipeline))
        total = sum(item['count'] for item in results)
        score = {"sim": 0, "nao": 0}
        for item in results:
            if item['_id'] == "sim":
                score["sim"] = (item['count'] / total) * 100
            elif item['_id'] == "nao":
                score["nao"] = (item['count'] / total) * 100
        return score
    
    def delete_by_pergunta_id(self, pergunta_id):
        self.collection.delete_many({"pergunta_id": pergunta_id})

    #verificar se o usuário já interagiu com a pergunta
    def has_interacted(self, vem_hash, pergunta_id):
        return self.collection.find_one(
            {"vem_hash": vem_hash, "pergunta_id": pergunta_id}
        ) is not None