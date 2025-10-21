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
    
    # obter resultado de numero de sim ou não em percentual de acordo com o pergunta_id
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
        score = {}
        for item in results:
            resposta = item['_id']
            count = item['count']
            percentage = (count / total) * 100 if total > 0 else 0
            score[resposta] = percentage
        return score
