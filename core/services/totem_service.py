from core.repositories.totem_repo import TotemRepository
from models.totem import Totem

class TotemService:
    def __init__(self):
        self.repo = TotemRepository()

    def criar_totem(self, latitude, longitude):
        totem = Totem(latitude, longitude)
        self.repo.save(totem)
        return totem.to_dict()

    def listar_totens(self):
        return self.repo.get_all()

    def buscar_totem(self, totem_id):
        return self.repo.get_by_id(totem_id)

    def excluir_totem(self, totem_id):
        self.repo.delete(totem_id)
        return {"mensagem": "Totem removido com sucesso"}
