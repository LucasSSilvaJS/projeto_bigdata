from core.database import MongoConnection

class TotemRepository:
    def __init__(self):
        self.collection = MongoConnection().get_collection("totens")

    def save(self, totem):
        self.collection.update_one(
            {"totem_id": totem.totem_id},
            {"$set": totem.to_dict()},
            upsert=True
        )

    def get_all(self):
        return list(self.collection.find({}, {"_id": 0}))

    def get_by_id(self, totem_id):
        return self.collection.find_one({"totem_id": totem_id}, {"_id": 0})

    def delete(self, totem_id):
        self.collection.delete_one({"totem_id": totem_id})
