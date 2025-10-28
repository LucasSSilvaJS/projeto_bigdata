from fastapi import APIRouter, Query, HTTPException
from core.services.thanos_service import ThanosService

from typing import List, Dict, Any
# rota dar delete em todos os dados registrados no sistema

router = APIRouter(
    prefix="/thanos",
    tags=["💀 Thanos"],
    responses={
        404: {"description": "Recurso não encontrado"},
        422: {"description": "Dados inválidos"}
    }
)

service = ThanosService()

@router.delete("/estalar",
    summary="Estalar os dedos do Thanos",
    description="Remove todos os dados do sistema, simbolizando o 'estalo' do Thanos.",
    response_description="Todos os dados foram removidos com sucesso")
def estalar_dedos():
    """
    ## 💀 Estalar os Dedos do Thanos
    Remove todos os dados do sistema, simbolizando o "estalo" do Thanos.
    ### Exemplo de uso:
    ```
    DELETE /thanos/estalar
    ```
    ### Resposta:
    ```json
    {
        "mensagem": "Todos os dados foram removidos com sucesso"
    }
    ```
    """
    return service.estalar_dedos()