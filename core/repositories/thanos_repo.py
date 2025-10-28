from core.database import MongoConnection

# Repositório para operações relacionadas ao Thanos (remoção de todos os dados), simbolizando o "estalo" do Thanos.

class ThanosRepository:
    def __init__(self):
        self.pergunta_collection = MongoConnection().get_collection("perguntas")
        self.usuario_collection = MongoConnection().get_collection("usuarios")
        self.totem_collection = MongoConnection().get_collection("totens")
        self.interacao_collection = MongoConnection().get_collection("interacoes")

    def delete_all_data(self):
        self.pergunta_collection.delete_many({})
        self.usuario_collection.delete_many({})
        self.totem_collection.delete_many({})
        self.interacao_collection.delete_many({})