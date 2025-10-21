from core.database import MongoConnection

class PerguntaRepository:
    def __init__(self):
        self.collection = MongoConnection().get_collection("perguntas")

    def save(self, pergunta):
        self.collection.update_one(
            {"pergunta_id": pergunta.pergunta_id},
            {"$set": pergunta.to_dict()},
            upsert=True
        )

    def get_all(self):
        return list(self.collection.find({}, {"_id": 0}))

    def get_last(self):
        return self.collection.find_one(sort=[("data_criacao", -1)], projection={"_id": 0})

    def get_by_id(self, pergunta_id):
        return self.collection.find_one({"pergunta_id": pergunta_id}, {"_id": 0})

    def delete(self, pergunta_id):
        self.collection.delete_one({"pergunta_id": pergunta_id})
