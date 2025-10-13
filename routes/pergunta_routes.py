from fastapi import APIRouter, Query, HTTPException
from core.services.pergunta_service import PerguntaService
from typing import List, Dict, Any

router = APIRouter(
    prefix="/perguntas", 
    tags=["❓ Perguntas"],
    responses={
        404: {"description": "Pergunta não encontrada"},
        422: {"description": "Dados inválidos"}
    }
)
service = PerguntaService()

@router.post("/", 
    summary="Criar nova pergunta",
    description="Cria uma nova pergunta que pode ser respondida pelos usuários nos totens. O ID é gerado automaticamente.",
    response_description="Pergunta criada com sucesso")
def criar_pergunta(
    texto: str = Query(..., description="Texto da pergunta", example="Você gostou do atendimento?")
):
    """
    ## ❓ Criar Nova Pergunta
    
    Cria uma nova pergunta que pode ser respondida pelos usuários nos totens.
    O ID da pergunta é gerado automaticamente usando hash baseado no texto e timestamp.
    
    ### Parâmetros:
    - **texto** (string): Texto da pergunta
    
    ### Exemplo de uso:
    ```
    POST /perguntas/?texto=Você ficou satisfeito com nosso atendimento?
    ```
    
    ### Resposta:
    ```json
    {
        "pergunta_id": "b2c3d4e5f6a1",
        "texto": "Você ficou satisfeito com nosso atendimento?",
        "data_criacao": "2025-01-13T02:30:00.123456"
    }
    ```
    """
    return service.criar_pergunta(texto)

@router.get("/", 
    summary="Listar todas as perguntas",
    description="Retorna uma lista com todas as perguntas cadastradas no sistema.",
    response_description="Lista de perguntas")
def listar_perguntas():
    """
    ## 📋 Listar Todas as Perguntas
    
    Retorna uma lista com todas as perguntas cadastradas no sistema.
    
    ### Resposta:
    ```json
    [
        {
            "pergunta_id": "pergunta001",
            "texto": "Você gostou do atendimento?"
        }
    ]
    ```
    """
    return service.listar_perguntas()

@router.get("/{pergunta_id}", 
    summary="Buscar pergunta por ID",
    description="Busca uma pergunta específica usando seu identificador único.",
    response_description="Dados da pergunta encontrada")
def buscar_pergunta(pergunta_id: str):
    """
    ## 🔍 Buscar Pergunta por ID
    
    Busca uma pergunta específica no sistema usando seu identificador único.
    
    ### Parâmetros:
    - **pergunta_id** (string): Identificador único da pergunta
    
    ### Exemplo de uso:
    ```
    GET /perguntas/pergunta001
    ```
    
    ### Resposta:
    ```json
    {
        "pergunta_id": "pergunta001",
        "texto": "Você gostou do atendimento?"
    }
    ```
    """
    pergunta = service.buscar_pergunta(pergunta_id)
    if not pergunta:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    return pergunta

@router.delete("/{pergunta_id}", 
    summary="Excluir pergunta",
    description="Remove uma pergunta do sistema usando seu identificador único.",
    response_description="Confirmação de exclusão")
def excluir_pergunta(pergunta_id: str):
    """
    ## 🗑️ Excluir Pergunta
    
    Remove uma pergunta do sistema usando seu identificador único.
    
    ### Parâmetros:
    - **pergunta_id** (string): Identificador único da pergunta
    
    ### Exemplo de uso:
    ```
    DELETE /perguntas/pergunta001
    ```
    
    ### Resposta:
    ```json
    {
        "mensagem": "Pergunta removida com sucesso"
    }
    ```
    """
    return service.excluir_pergunta(pergunta_id)
