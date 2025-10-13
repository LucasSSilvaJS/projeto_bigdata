from core.database import MongoConnection

class UsuarioRepository:
    def __init__(self):
        self.collection = MongoConnection().get_collection("usuarios")

    def save(self, usuario):
        self.collection.update_one(
            {"vem_hash": usuario.vem_hash},
            {"$set": usuario.to_dict()},
            upsert=True
        )

    def get_all(self):
        return list(self.collection.find({}, {"_id": 0}))

    def get_by_vem_hash(self, vem_hash):
        return self.collection.find_one({"vem_hash": vem_hash}, {"_id": 0})

    def delete(self, vem_hash):
        self.collection.delete_one({"vem_hash": vem_hash})
