from fastapi import APIRouter, Query, HTTPException
from core.services.usuario_service import UsuarioService
from typing import List, Dict, Any

router = APIRouter(
    prefix="/usuarios", 
    tags=["👤 Usuários"],
    responses={
        404: {"description": "Usuário não encontrado"},
        422: {"description": "Dados inválidos"}
    }
)
service = UsuarioService()

@router.post("/{vem_hash}", 
    summary="Criar novo usuário",
    description="Cria um novo usuário no sistema identificado por um hash único.",
    response_description="Usuário criado com sucesso")
def criar_usuario(vem_hash: str):
    """
    ## 📝 Criar Novo Usuário
    
    Cria um novo usuário no sistema usando um hash único como identificador.
    
    ### Parâmetros:
    - **vem_hash** (string): Hash único do usuário
    
    ### Exemplo de uso:
    ```
    POST /usuarios/?vem_hash=cliente001
    ```
    
    ### Resposta:
    ```json
    {
        "vem_hash": "cliente001"
    }
    ```
    """
    #verificar se o usuário já existe
    existing_user = service.buscar_usuario(vem_hash)
    if existing_user:
        raise HTTPException(status_code=422, detail="Usuário já existe")
    return service.criar_usuario(vem_hash)

@router.get("/", 
    summary="Listar todos os usuários",
    description="Retorna uma lista com todos os usuários cadastrados no sistema.",
    response_description="Lista de usuários")
def listar_usuarios():
    """
    ## 📋 Listar Todos os Usuários
    
    Retorna uma lista com todos os usuários cadastrados no sistema.
    
    ### Resposta:
    ```json
    [
        {"vem_hash": "user123"},
        {"vem_hash": "user456"}
    ]
    ```
    """
    return service.listar_usuarios()

@router.get("/{vem_hash}", 
    summary="Buscar usuário por hash",
    description="Busca um usuário específico usando seu hash único.",
    response_description="Dados do usuário encontrado")
def buscar_usuario(vem_hash: str):
    """
    ## 🔍 Buscar Usuário por Hash
    
    Busca um usuário específico no sistema usando seu hash único.
    
    ### Parâmetros:
    - **vem_hash** (string): Hash único do usuário
    
    ### Exemplo de uso:
    ```
    GET /usuarios/user123
    ```
    
    ### Resposta:
    ```json
    {
        "vem_hash": "user123"
    }
    ```
    """
    usuario = service.buscar_usuario(vem_hash)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.delete("/{vem_hash}", 
    summary="Excluir usuário",
    description="Remove um usuário do sistema usando seu hash único.",
    response_description="Confirmação de exclusão")
def excluir_usuario(vem_hash: str):
    """
    ## 🗑️ Excluir Usuário
    
    Remove um usuário do sistema usando seu hash único.
    
    ### Parâmetros:
    - **vem_hash** (string): Hash único do usuário
    
    ### Exemplo de uso:
    ```
    DELETE /usuarios/user123
    ```
    
    ### Resposta:
    ```json
    {
        "mensagem": "Usuário removido com sucesso"
    }
    ```
    """
    return service.excluir_usuario(vem_hash)
