from core.repositories.usuario_repo import UsuarioRepository
from models.usuario import Usuario, UsuarioCadastro, UsuarioResposta
from datetime import date, datetime
from typing import Optional, List, Dict, Any

class UsuarioService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def criar_usuario(self, vem_hash: str) -> dict:
        """
        Cria um novo usuário apenas com o hash (cadastro inicial via QR Code)
        """
        usuario = Usuario(vem_hash=vem_hash)
        self.repo.save(usuario)
        return usuario.model_dump()

    def verificar_usuario(self, vem_hash: str) -> UsuarioResposta:
        """
        Verifica se o usuário existe pelo hash do QR Code.
        Se não existir, cria um usuário temporário.
        Retorna dados do usuário indicando se precisa completar cadastro.
        """
        usuario_dict = self.repo.get_by_vem_hash(vem_hash)
        
        if not usuario_dict:
            # Cria usuário temporário apenas com hash
            usuario = Usuario(vem_hash=vem_hash)
            self.repo.save(usuario)
            usuario_dict = usuario.model_dump()
        
        # Converte dict para objeto Usuario para usar métodos
        usuario = Usuario(**usuario_dict)
        
        return UsuarioResposta(
            vem_hash=usuario.vem_hash,
            nome=usuario.nome,
            pontuacao=usuario.pontuacao,
            cadastro_completo=usuario.cadastro_completo,
            idade=usuario.calcular_idade()
        )

    def completar_cadastro(self, dados: UsuarioCadastro) -> UsuarioResposta:
        """
        Completa o cadastro do usuário com nome, email e data de nascimento
        """
        usuario_dict = self.repo.get_by_vem_hash(dados.vem_hash)
        
        if not usuario_dict:
            raise ValueError("Usuário não encontrado. Escaneie o QR Code primeiro.")
        
        # Converte dict para objeto Usuario
        usuario = Usuario(**usuario_dict)
        
        if usuario.cadastro_completo:
            raise ValueError("Usuário já possui cadastro completo")
        
        # Completa o cadastro
        usuario.completar_cadastro(
            nome=dados.nome,
            email=dados.email,
            data_nascimento=dados.data_nascimento
        )
        
        # Salva no repositório
        self.repo.update(dados.vem_hash, usuario.model_dump(mode='json'))
        
        return UsuarioResposta(
            vem_hash=usuario.vem_hash,
            nome=usuario.nome,
            pontuacao=usuario.pontuacao,
            cadastro_completo=usuario.cadastro_completo,
            idade=usuario.calcular_idade()
        )

    def listar_usuarios(self) -> List[dict]:
        """
        Lista todos os usuários do sistema
        """
        return self.repo.get_all()

    def buscar_usuario(self, vem_hash: str) -> Optional[dict]:
        """
        Busca um usuário específico pelo hash
        """
        return self.repo.get_by_vem_hash(vem_hash)
    
    def buscar_usuario_detalhado(self, vem_hash: str) -> Optional[UsuarioResposta]:
        """
        Busca um usuário e retorna no formato de resposta padronizado
        """
        usuario_dict = self.repo.get_by_vem_hash(vem_hash)
        
        if not usuario_dict:
            return None
        
        usuario = Usuario(**usuario_dict)
        
        return UsuarioResposta(
            vem_hash=usuario.vem_hash,
            nome=usuario.nome,
            pontuacao=usuario.pontuacao,
            cadastro_completo=usuario.cadastro_completo,
            idade=usuario.calcular_idade()
        )

    def excluir_usuario(self, vem_hash: str) -> dict:
        """
        Remove um usuário do sistema
        """
        # Verifica se usuário existe antes de deletar
        if not self.repo.exists(vem_hash):
            raise ValueError("Usuário não encontrado")
        
        self.repo.delete(vem_hash)
        return {"mensagem": "Usuário removido com sucesso", "vem_hash": vem_hash}
    
    def atualizar_pontuacao(self, vem_hash: str, pontos: int) -> Optional[dict]:
        """
        Atualiza a pontuação de um usuário (adiciona ou subtrai pontos)
        Versão otimizada usando operação atômica do MongoDB
        """
        nova_pontuacao = self.repo.increment_points(vem_hash, pontos)
        
        if nova_pontuacao is None:
            return None
        
        return {
            "vem_hash": vem_hash, 
            "pontuacao": nova_pontuacao,
            "pontos_adicionados": pontos
        }
    
    def adicionar_pontos_por_voto(self, vem_hash: str, pontos: int = 10) -> dict:
        """
        Adiciona pontos ao usuário após registrar um voto.
        Método específico para o fluxo de votação.
        """
        resultado = self.atualizar_pontuacao(vem_hash, pontos)
        if not resultado:
            raise ValueError("Usuário não encontrado")
        
        return {
            "mensagem": "Voto registrado com sucesso!",
            "vem_hash": vem_hash,
            "pontuacao_atual": resultado["pontuacao"],
            "pontos_ganhos": pontos
        }
    
    def atualizar_dados_parcial(self, vem_hash: str, campos: dict) -> dict:
        """
        Atualiza campos específicos de um usuário sem afetar outros dados.
        Útil para atualizações incrementais.
        
        Exemplo: atualizar_dados_parcial("hash123", {"nome": "João Silva"})
        """
        if not self.repo.exists(vem_hash):
            raise ValueError("Usuário não encontrado")
        
        # Remove campos que não devem ser atualizados diretamente
        campos_proibidos = ["vem_hash", "data_criacao", "pontuacao"]
        for campo in campos_proibidos:
            campos.pop(campo, None)
        
        sucesso = self.repo.update_partial(vem_hash, campos)
        
        if not sucesso:
            raise ValueError("Falha ao atualizar usuário")
        
        return {
            "mensagem": "Dados atualizados com sucesso",
            "vem_hash": vem_hash,
            "campos_atualizados": list(campos.keys())
        }
    
    def obter_estatisticas_idade(self) -> dict:
        """
        Retorna estatísticas sobre a idade dos usuários cadastrados
        Útil para análise demográfica
        """
        usuarios = self.repo.get_all()
        idades = []
        
        for usuario_dict in usuarios:
            if usuario_dict.get('data_nascimento'):
                try:
                    usuario = Usuario(**usuario_dict)
                    idade = usuario.calcular_idade()
                    if idade:
                        idades.append(idade)
                except Exception:
                    # Ignora usuários com dados inválidos
                    continue
        
        if not idades:
            return {
                "total_usuarios_com_idade": 0,
                "idade_media": None,
                "idade_minima": None,
                "idade_maxima": None
            }
        
        return {
            "total_usuarios_com_idade": len(idades),
            "idade_media": round(sum(idades) / len(idades), 2),
            "idade_minima": min(idades),
            "idade_maxima": max(idades)
        }
    
    def obter_estatisticas_gerais(self) -> dict:
        """
        Retorna estatísticas gerais sobre os usuários
        """
        total_usuarios = self.repo.count_total()
        cadastros_completos = self.repo.count_cadastros_completos()
        cadastros_incompletos = total_usuarios - cadastros_completos
        
        # Calcula pontuação total e média
        usuarios = self.repo.get_all()
        pontuacoes = [u.get('pontuacao', 0) for u in usuarios]
        pontuacao_total = sum(pontuacoes)
        pontuacao_media = round(pontuacao_total / total_usuarios, 2) if total_usuarios > 0 else 0
        
        return {
            "total_usuarios": total_usuarios,
            "cadastros_completos": cadastros_completos,
            "cadastros_incompletos": cadastros_incompletos,
            "percentual_cadastros_completos": round((cadastros_completos / total_usuarios * 100), 2) if total_usuarios > 0 else 0,
            "pontuacao_total": pontuacao_total,
            "pontuacao_media": pontuacao_media,
            "pontuacao_maxima": max(pontuacoes) if pontuacoes else 0,
            "estatisticas_idade": self.obter_estatisticas_idade()
        }
    
    def listar_usuarios_por_pontuacao(self, limite: int = 10, ordem: str = "desc") -> List[dict]:
        """
        Lista usuários ordenados por pontuação (ranking)
        
        Args:
            limite: Número máximo de usuários a retornar
            ordem: "desc" para maior pontuação primeiro, "asc" para menor
        """
        usuarios = self.repo.get_all()
        
        # Ordena por pontuação
        reverse = (ordem == "desc")
        usuarios_ordenados = sorted(
            usuarios, 
            key=lambda x: x.get('pontuacao', 0), 
            reverse=reverse
        )
        
        return usuarios_ordenados[:limite]
    
    def existe_usuario(self, vem_hash: str) -> bool:
        """
        Verifica se um usuário existe no sistema
        """
        return self.repo.exists(vem_hash)