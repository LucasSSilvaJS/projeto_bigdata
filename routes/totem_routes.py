from fastapi import APIRouter, Query, HTTPException
from core.services.totem_service import TotemService
from typing import List, Dict, Any

router = APIRouter(
    prefix="/totens", 
    tags=["🤖 Totens"],
    responses={
        404: {"description": "Totem não encontrado"},
        422: {"description": "Coordenadas inválidas"}
    }
)
service = TotemService()

@router.post("/", 
    summary="Criar novo totem",
    description="Cria um novo totem com localização geográfica específica. O ID é gerado automaticamente.",
    response_description="Totem criado com sucesso")
def criar_totem(
    latitude: float = Query(..., description="Latitude geográfica", example=-23.5505),
    longitude: float = Query(..., description="Longitude geográfica", example=-46.6333)
):
    """
    ## 📍 Criar Novo Totem
    
    Cria um novo totem no sistema com sua localização geográfica.
    O ID do totem é gerado automaticamente usando hash baseado nas coordenadas e timestamp.
    
    ### Parâmetros:
    - **latitude** (float): Coordenada de latitude
    - **longitude** (float): Coordenada de longitude
    
    ### Exemplo de uso:
    ```
    POST /totens/?latitude=-23.5505&longitude=-46.6333
    ```
    
    ### Resposta:
    ```json
    {
        "totem_id": "a1b2c3d4e5f6",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "data_criacao": "2025-01-13T02:30:00.123456"
    }
    ```
    """
    return service.criar_totem(latitude, longitude)

@router.get("/", 
    summary="Listar todos os totens",
    description="Retorna uma lista com todos os totens cadastrados no sistema.",
    response_description="Lista de totens")
def listar_totens():
    """
    ## 📋 Listar Todos os Totens
    
    Retorna uma lista com todos os totens cadastrados no sistema.
    
    ### Resposta:
    ```json
    [
        {
            "totem_id": "totem001",
            "latitude": -23.5505,
            "longitude": -46.6333
        }
    ]
    ```
    """
    return service.listar_totens()

@router.get("/{totem_id}", 
    summary="Buscar totem por ID",
    description="Busca um totem específico usando seu identificador único.",
    response_description="Dados do totem encontrado")
def buscar_totem(totem_id: str):
    """
    ## 🔍 Buscar Totem por ID
    
    Busca um totem específico no sistema usando seu identificador único.
    
    ### Parâmetros:
    - **totem_id** (string): Identificador único do totem
    
    ### Exemplo de uso:
    ```
    GET /totens/totem001
    ```
    
    ### Resposta:
    ```json
    {
        "totem_id": "totem001",
        "latitude": -23.5505,
        "longitude": -46.6333
    }
    ```
    """
    totem = service.buscar_totem(totem_id)
    if not totem:
        raise HTTPException(status_code=404, detail="Totem não encontrado")
    return totem

@router.delete("/{totem_id}", 
    summary="Excluir totem",
    description="Remove um totem do sistema usando seu identificador único.",
    response_description="Confirmação de exclusão")
def excluir_totem(totem_id: str):
    """
    ## 🗑️ Excluir Totem
    
    Remove um totem do sistema usando seu identificador único.
    
    ### Parâmetros:
    - **totem_id** (string): Identificador único do totem
    
    ### Exemplo de uso:
    ```
    DELETE /totens/totem001
    ```
    
    ### Resposta:
    ```json
    {
        "mensagem": "Totem removido com sucesso"
    }
    ```
    """
    return service.excluir_totem(totem_id)
