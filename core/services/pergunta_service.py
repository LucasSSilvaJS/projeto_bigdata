from core.repositories.pergunta_repo import PerguntaRepository
from models.pergunta import Pergunta

class PerguntaService:
    def __init__(self):
        self.repo = PerguntaRepository()

    def criar_pergunta(self, texto):
        pergunta = Pergunta(texto)
        self.repo.save(pergunta)
        return pergunta.to_dict()

    def listar_perguntas(self):
        return self.repo.get_all()

    def buscar_pergunta(self, pergunta_id):
        return self.repo.get_by_id(pergunta_id)

    def excluir_pergunta(self, pergunta_id):
        self.repo.delete(pergunta_id)
        return {"mensagem": "Pergunta removida com sucesso"}
