from core.repositories.interacao_repo import InteracaoRepository
from models.interacao import Interacao

class InteracaoService:
    def __init__(self):
        self.repo = InteracaoRepository()

    def listar_interacoes(self):
        """
        Retorna todas as interações registradas no sistema.
        """
        return self.repo.get_all()
    
    def obter_score(self, pergunta_id):
        """
        Retorna o percentual de respostas 'sim' e 'nao' para uma pergunta específica.
        """
        if not pergunta_id:
            raise ValueError("pergunta_id inválido")
        return self.repo.get_score(pergunta_id)

    def registrar_interacao(self, vem_hash, pergunta_id, totem_id, resposta):
        """
        Registra uma nova interação no sistema.
        Valida resposta e parâmetros.
        """
        if not vem_hash or not pergunta_id or not totem_id:
            raise ValueError("vem_hash, pergunta_id e totem_id são obrigatórios")
        if resposta not in ["sim", "nao"]:
            raise ValueError("Resposta inválida, deve ser 'sim' ou 'nao'")
        
        interacao = Interacao(vem_hash, pergunta_id, totem_id, resposta)
        self.repo.save(interacao)
        return interacao.to_dict()
    
    def excluir_interacoes_por_pergunta(self, pergunta_id):
        """
        Remove todas as interações associadas a uma pergunta específica.
        """
        if not pergunta_id:
            raise ValueError("pergunta_id inválido")
        self.repo.delete_by_pergunta_id(pergunta_id)
        return {"mensagem": "Interações removidas com sucesso"}
    
    def verificar_interacao(self, vem_hash, pergunta_id):
        """
        Verifica se o usuário já interagiu com uma pergunta específica.
        """
        if not vem_hash or not pergunta_id:
            raise ValueError("vem_hash e pergunta_id são obrigatórios")
        return self.repo.has_interacted(vem_hash, pergunta_id)
