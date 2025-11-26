from core.repositories.servico_repo import ServicoRepository
from models.servico import Servico, ServicoCreate, ServicoResposta
from typing import List, Dict, Optional

class ServicoService:
    def __init__(self):
        self.repo = ServicoRepository()

    def criar_servico(self, dados: ServicoCreate) -> dict:
        """
        Cria um novo serviço público
        """
        # Gera ID único baseado no nome e coordenadas
        servico_id = Servico.gerar_id(
            nome=dados.nome,
            latitude=dados.latitude,
            longitude=dados.longitude
        )
        
        # Cria o objeto Servico
        servico = Servico(
            servico_id=servico_id,
            nome=dados.nome,
            tipo=dados.tipo,
            latitude=dados.latitude,
            longitude=dados.longitude,
            endereco=dados.endereco,
            telefone=dados.telefone,
            horario_funcionamento=dados.horario_funcionamento,
            descricao=dados.descricao
        )
        
        # Salva no banco
        self.repo.save(servico)
        
        return servico.model_dump(mode='json')

    def listar_servicos(self, apenas_ativos: bool = True) -> List[dict]:
        """
        Lista todos os serviços (ou apenas ativos)
        """
        if apenas_ativos:
            return self.repo.get_ativos()
        return self.repo.get_all()

    def buscar_servico(self, servico_id: str) -> Optional[dict]:
        """
        Busca um serviço específico por ID
        """
        return self.repo.get_by_id(servico_id)

    def buscar_por_tipo(self, tipo: str) -> List[dict]:
        """
        Busca serviços por tipo
        """
        return self.repo.get_by_tipo(tipo)

    def buscar_proximos_ao_totem(
        self, 
        totem_latitude: float, 
        totem_longitude: float, 
        raio_km: float = 5.0
    ) -> List[ServicoResposta]:
        """
        Busca serviços próximos a um totem dentro de um raio em km.
        Retorna lista ordenada por distância (mais próximo primeiro).
        """
        # Busca todos os serviços ativos
        servicos = self.repo.get_ativos()
        
        # Lista para armazenar serviços com distância calculada
        servicos_com_distancia = []
        
        for servico_dict in servicos:
            # Converte dict para objeto Servico para usar o método calcular_distancia
            servico = Servico(**servico_dict)
            
            # Calcula distância do totem até o serviço
            distancia = servico.calcular_distancia(totem_latitude, totem_longitude)
            
            # Se estiver dentro do raio, adiciona na lista
            if distancia <= raio_km:
                servicos_com_distancia.append({
                    "servico": servico,
                    "distancia_km": distancia
                })
        
        # Ordena por distância (mais próximo primeiro)
        servicos_com_distancia.sort(key=lambda x: x["distancia_km"])
        
        # Converte para ServicoResposta
        resultado = []
        for item in servicos_com_distancia:
            servico = item["servico"]
            resposta = ServicoResposta(
                servico_id=servico.servico_id,
                nome=servico.nome,
                tipo=servico.tipo,
                latitude=servico.latitude,
                longitude=servico.longitude,
                endereco=servico.endereco,
                telefone=servico.telefone,
                horario_funcionamento=servico.horario_funcionamento,
                descricao=servico.descricao,
                ativo=servico.ativo,
                distancia_km=item["distancia_km"]
            )
            resultado.append(resposta)
        
        return resultado

    def buscar_proximos_por_totem_id(self, totem_id: str, raio_km: float = 5.0) -> List[ServicoResposta]:
        """
        Busca serviços próximos a um totem usando o ID do totem.
        Busca as coordenadas do totem e depois os serviços próximos.
        """
        from core.repositories.totem_repo import TotemRepository
        
        totem_repo = TotemRepository()
        totem = totem_repo.get_by_totem_id(totem_id)
        
        if not totem:
            raise ValueError(f"Totem {totem_id} não encontrado")
        
        return self.buscar_proximos_ao_totem(
            totem_latitude=totem["latitude"],
            totem_longitude=totem["longitude"],
            raio_km=raio_km
        )

    def atualizar_servico(self, servico_id: str, campos: dict) -> dict:
        """
        Atualiza campos específicos de um serviço
        """
        if not self.repo.exists(servico_id):
            raise ValueError("Serviço não encontrado")
        
        # Remove campos que não devem ser atualizados
        campos_proibidos = ["servico_id", "data_criacao"]
        for campo in campos_proibidos:
            campos.pop(campo, None)
        
        sucesso = self.repo.update_partial(servico_id, campos)
        
        if not sucesso:
            raise ValueError("Falha ao atualizar serviço")
        
        return {
            "mensagem": "Serviço atualizado com sucesso",
            "servico_id": servico_id,
            "campos_atualizados": list(campos.keys())
        }

    def excluir_servico(self, servico_id: str, soft_delete: bool = True) -> dict:
        """
        Exclui um serviço (soft delete por padrão)
        """
        if not self.repo.exists(servico_id):
            raise ValueError("Serviço não encontrado")
        
        if soft_delete:
            self.repo.desativar(servico_id)
            mensagem = "Serviço desativado com sucesso"
        else:
            self.repo.delete(servico_id)
            mensagem = "Serviço removido permanentemente"
        
        return {
            "mensagem": mensagem,
            "servico_id": servico_id
        }

    def reativar_servico(self, servico_id: str) -> dict:
        """
        Reativa um serviço desativado
        """
        if not self.repo.exists(servico_id):
            raise ValueError("Serviço não encontrado")
        
        self.repo.ativar(servico_id)
        
        return {
            "mensagem": "Serviço reativado com sucesso",
            "servico_id": servico_id
        }

    def obter_estatisticas(self) -> dict:
        """
        Retorna estatísticas sobre os serviços cadastrados
        """
        total = self.repo.count_total()
        ativos = self.repo.count_ativos()
        inativos = total - ativos
        por_tipo = self.repo.count_por_tipo()
        
        return {
            "total_servicos": total,
            "servicos_ativos": ativos,
            "servicos_inativos": inativos,
            "percentual_ativos": round((ativos / total * 100), 2) if total > 0 else 0,
            "servicos_por_tipo": por_tipo
        }

    def listar_tipos_disponiveis(self) -> List[str]:
        """
        Retorna lista de tipos de serviços cadastrados
        """
        por_tipo = self.repo.count_por_tipo()
        return list(por_tipo.keys())

    def existe_servico(self, servico_id: str) -> bool:
        """
        Verifica se um serviço existe
        """
        return self.repo.exists(servico_id)