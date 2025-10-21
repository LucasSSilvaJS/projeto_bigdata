from fastapi import APIRouter, Query, HTTPException
from core.services.interacao_service import InteracaoService

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
    resposta: str = Query(..., description="Resposta do usuário (sim ou nao)", example="sim")
):
    """
    ## 🔄 Registrar Nova Interação
    
    Registra uma nova interação de um usuário respondendo uma pergunta em um totem específico.
    
    ### Parâmetros:
    - **vem_hash** (string): Hash único do usuário
    - **pergunta_id** (string): ID da pergunta respondida
    - **totem_id** (string): ID do totem onde ocorreu a interação
    - **resposta** (string): Resposta do usuário ("sim" ou "nao")
    
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
    - A resposta deve ser exatamente "sim" ou "nao"
    - O usuário, pergunta e totem devem existir no sistema
    """
    try:
        return service.registrar_interacao(vem_hash, pergunta_id, totem_id, resposta)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

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

@router.delete("/pergunta/{pergunta_id}", 
    summary="Excluir interações por pergunta",
    description="Remove todas as interações associadas a uma pergunta específica.",
    response_description="Interações removidas com sucesso")
def excluir_interacoes_por_pergunta(pergunta_id: str):
    """
    ## 🗑️ Excluir Interações por Pergunta

    Remove todas as interações associadas a uma pergunta específica.

    ### Parâmetros:
    - **pergunta_id** (string): Identificador único da pergunta

    ### Exemplo de uso:
    ```
    DELETE /interacoes/pergunta/pergunta001
    ```

    ### Resposta:
    ```json
    {
        "mensagem": "Interações removidas com sucesso"
    }
    ```
    """
    try:
        return service.excluir_interacoes_por_pergunta(pergunta_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/verificar", 
    summary="Verificar interação do usuário",
    description="Verifica se um usuário já interagiu com uma pergunta específica.",
    response_description="Resultado da verificação")
def verificar_interacao(
    vem_hash: str = Query(..., description="Hash único do usuário", example="user123"),
    pergunta_id: str = Query(..., description="ID da pergunta", example="pergunta001")
):
    """
    ## ✅ Verificar Interação do Usuário

    Verifica se um usuário já interagiu com uma pergunta específica.

    ### Parâmetros:
    - **vem_hash** (string): Hash único do usuário
    - **pergunta_id** (string): ID da pergunta

    ### Exemplo de uso:
    ```
    GET /interacoes/verificar?vem_hash=user123&pergunta_id=pergunta001
    ```

    ### Resposta:
    ```json
    {
        "interagiu": true
    }
    ```
    """
    try:
        interagiu = service.verificar_interacao(vem_hash, pergunta_id)
        return {"interagiu": interagiu}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/score/{pergunta_id}", 
    summary="Obter score de respostas para uma pergunta",
    description="Calcula o percentual de respostas 'sim' e 'nao' para uma pergunta específica.",
    response_description="Score de respostas")
def obter_score(pergunta_id: str):
    """
    ## 📊 Obter Score de Respostas para uma Pergunta

    Calcula o percentual de respostas 'sim' e 'nao' para uma pergunta específica.

    ### Parâmetros:
    - **pergunta_id** (string): Identificador único da pergunta

    ### Exemplo de uso:
    ```
    GET /interacoes/score/pergunta001
    ```

    ### Resposta:
    ```json
    {
        "sim": 75.0,
        "nao": 25.0
    }
    ```
    """
    try:
        return service.obter_score(pergunta_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
