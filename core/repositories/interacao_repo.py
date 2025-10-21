from core.database import MongoConnection

class InteracaoRepository:
    def __init__(self):
        self.collection = MongoConnection().get_collection("interacoes")

    def save(self, interacao):
        """
        Salva uma interação no banco. Atualiza se já existir, caso contrário cria uma nova.
        """
        data = interacao.to_dict()
        if "_id" in data:
            del data["_id"]  # Evita conflito de _id no MongoDB

        self.collection.update_one(
            {
                "vem_hash": interacao.vem_hash,
                "pergunta_id": interacao.pergunta_id,
                "totem_id": interacao.totem_id
            },
            {"$set": data},
            upsert=True
        )

    def get_all(self):
        """
        Retorna todas as interações do banco.
        """
        return list(self.collection.find({}, {"_id": 0}))
    
    def get_score(self, pergunta_id):
        """
        Retorna o percentual de respostas "sim" e "nao" para a pergunta especificada.
        Protegido contra divisão por zero.
        """
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
        if total > 0:
            for item in results:
                if item['_id'] == "sim":
                    score["sim"] = round((item['count'] / total) * 100, 2)
                elif item['_id'] == "nao":
                    score["nao"] = round((item['count'] / total) * 100, 2)
        return score
    
    def delete_by_pergunta_id(self, pergunta_id):
        """
        Exclui todas as interações relacionadas a uma pergunta.
        """
        self.collection.delete_many({"pergunta_id": pergunta_id})

    def has_interacted(self, vem_hash, pergunta_id):
        """
        Verifica se o usuário já interagiu com uma pergunta específica.
        """
        return self.collection.find_one(
            {"vem_hash": vem_hash, "pergunta_id": pergunta_id}
        ) is not None
