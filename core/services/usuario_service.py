from core.repositories.usuario_repo import UsuarioRepository
from models.usuario import Usuario

class UsuarioService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def criar_usuario(self, vem_hash):
        usuario = Usuario(vem_hash, pontuacao=0)
        self.repo.save(usuario)
        return usuario.to_dict()

    def listar_usuarios(self):
        return self.repo.get_all()

    def buscar_usuario(self, vem_hash):
        return self.repo.get_by_vem_hash(vem_hash)

    def excluir_usuario(self, vem_hash):
        self.repo.delete(vem_hash)
        return {"mensagem": "Usuário removido com sucesso"}
    
    def atualizar_pontuacao(self, vem_hash, pontos):
        usuario = self.repo.get_by_vem_hash(vem_hash)
        if not usuario:
            return None
        nova_pontuacao = usuario.get("pontuacao", 0) + pontos
        self.repo.set_points(vem_hash, nova_pontuacao)
        return {"vem_hash": vem_hash, "pontuacao": nova_pontuacao}
