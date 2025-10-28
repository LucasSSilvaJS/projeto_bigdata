from core.repositories.thanos_repo import ThanosRepository

class ThanosService:
    def __init__(self):
        self.repo = ThanosRepository()

    def estalar_dedos(self):
        """
        Remove todos os dados do sistema, simbolizando o "estalo" do Thanos.
        """
        self.repo.delete_all_data()
        return {"mensagem": "Todos os dados foram removidos com sucesso"}