from fastapi import APIRouter, Query, HTTPException
from core.services.interacao_service import InteracaoService
from typing import List, Dict, Any

router = APIRouter(
    prefix="/interacoes", 
    tags=["🔄 Interações"],
    responses={
        404: {"description": "Recurso não encontrado"},
        422: {"description": "Dados inválidos"}
    }
)
service = InteracaoService()

@router.post("/", 
    summary="Registrar nova interação",
    description="Registra uma nova interação de um usuário respondendo uma pergunta em um totem específico.",
    response_description="Interação registrada com sucesso")
def criar_interacao(
    vem_hash: str = Query(..., description="Hash único do usuário", example="user123"),
    pergunta_id: str = Query(..., description="ID da pergunta respondida", example="pergunta001"),
    totem_id: str = Query(..., description="ID do totem onde ocorreu a interação", example="totem001"),
    resposta: str = Query(..., description="Resposta do usuário (sim ou não)", example="sim")
):
    """
    ## 🔄 Registrar Nova Interação
    
    Registra uma nova interação de um usuário respondendo uma pergunta em um totem específico.
    
    ### Parâmetros:
    - **vem_hash** (string): Hash único do usuário
    - **pergunta_id** (string): ID da pergunta respondida
    - **totem_id** (string): ID do totem onde ocorreu a interação
    - **resposta** (string): Resposta do usuário ("sim" ou "não")
    
    ### Exemplo de uso:
    ```
    POST /interacoes/?vem_hash=user123&pergunta_id=pergunta001&totem_id=totem001&resposta=sim
    ```
    
    ### Resposta:
    ```json
    {
        "vem_hash": "user123",
        "pergunta_id": "pergunta001",
        "totem_id": "totem001",
        "resposta": "sim"
    }
    ```
    
    ### Validações:
    - A resposta deve ser exatamente "sim" ou "não"
    - O usuário, pergunta e totem devem existir no sistema
    """
    if resposta not in ["sim", "não"]:
        raise HTTPException(status_code=422, detail="Resposta deve ser 'sim' ou 'não'")
    
    return service.registrar_interacao(vem_hash, pergunta_id, totem_id, resposta)

@router.get("/", 
    summary="Listar todas as interações",
    description="Retorna uma lista com todas as interações registradas no sistema.",
    response_description="Lista de interações")
def listar_interacoes():
    """
    ## 📋 Listar Todas as Interações
    
    Retorna uma lista com todas as interações registradas no sistema.
    
    ### Resposta:
    ```json
    [
        {
            "vem_hash": "user123",
            "pergunta_id": "pergunta001",
            "totem_id": "totem001",
            "resposta": "sim"
        }
    ]
    ```
    
    ### Uso para Análise:
    Esta lista pode ser usada para:
    - Análise de satisfação
    - Análise geográfica
    - Análise temporal
    - Dashboards de Big Data
    """
    return service.listar_interacoes()
