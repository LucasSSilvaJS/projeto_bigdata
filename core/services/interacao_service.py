from core.repositories.interacao_repo import InteracaoRepository
from models.interacao import Interacao

class InteracaoService:
    def __init__(self):
        self.repo = InteracaoRepository()

    def registrar_interacao(self, vem_hash, pergunta_id, totem_id, resposta):
        interacao = Interacao(vem_hash, pergunta_id, totem_id, resposta)
        self.repo.save(interacao)
        return interacao.to_dict()

    def listar_interacoes(self):
        return self.repo.get_all()

    def obter_score(self, pergunta_id):
        return self.repo.get_score(pergunta_id)