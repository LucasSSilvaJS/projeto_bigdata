from fastapi import APIRouter, HTTPException, status, Body
from core.services.usuario_service import UsuarioService
from models.usuario import UsuarioCadastro, UsuarioResposta
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
        {
            "vem_hash": "abc123",
            "nome": "João Silva",
            "email": "joao@email.com",
            "pontuacao": 50,
            "cadastro_completo": true
        },
        {
            "vem_hash": "xyz789",
            "pontuacao": 0,
            "cadastro_completo": false
        }
    ]
```
    """
    return service.listar_usuarios()

@router.get("/ranking", 
    summary="Ranking de usuários por pontuação",
    description="Retorna os usuários ordenados por pontuação (maior para menor).",
    response_description="Lista de usuários ordenada por pontuação")
def ranking_usuarios(limite: int = 10, ordem: str = "desc"):
    """
    ## 🏆 Ranking de Usuários
    
    Retorna os usuários com maior pontuação para gamificação.
    
    ### Parâmetros:
    - **limite** (int): Quantidade de usuários a retornar (padrão: 10)
    - **ordem** (string): "desc" para maior pontuação primeiro, "asc" para menor (padrão: "desc")
    
    ### Exemplo de uso:
```
    GET /usuarios/ranking?limite=5&ordem=desc
```
    
    ### Resposta:
```json
    [
        {"vem_hash": "user1", "nome": "João", "pontuacao": 150},
        {"vem_hash": "user2", "nome": "Maria", "pontuacao": 120},
        {"vem_hash": "user3", "nome": "Pedro", "pontuacao": 100}
    ]
```
    """
    if limite < 1 or limite > 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limite deve estar entre 1 e 100"
        )
    
    if ordem not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ordem deve ser 'asc' ou 'desc'"
        )
    
    return service.listar_usuarios_por_pontuacao(limite=limite, ordem=ordem)

@router.get("/estatisticas",
    summary="Estatísticas gerais dos usuários",
    description="Retorna estatísticas completas sobre usuários, cadastros e pontuações.",
    response_description="Estatísticas do sistema")
def obter_estatisticas():
    """
    ## 📊 Estatísticas Gerais
    
    Retorna estatísticas completas sobre os usuários do sistema.
    
    ### Resposta:
```json
    {
        "total_usuarios": 150,
        "cadastros_completos": 120,
        "cadastros_incompletos": 30,
        "percentual_cadastros_completos": 80.0,
        "pontuacao_total": 5000,
        "pontuacao_media": 33.33,
        "pontuacao_maxima": 200,
        "estatisticas_idade": {
            "idade_media": 28.5,
            "idade_minima": 18,
            "idade_maxima": 65
        }
    }
```
    """
    return service.obter_estatisticas_gerais()

@router.post("/verificar/{vem_hash}",
    response_model=UsuarioResposta,
    summary="Verificar usuário por QR Code",
    description="Verifica se o usuário existe pelo hash do QR Code. Se não existir, cria automaticamente.",
    response_description="Dados do usuário e status de cadastro")
def verificar_usuario(vem_hash: str):
    """
    ## 🔍 Verificar Usuário (Fluxo do QR Code)
    
    Este endpoint é chamado quando o QR Code é escaneado no app.
    - Se o usuário **não existe**: cria um registro temporário
    - Se o usuário **existe**: retorna os dados dele
    
    O app usa o campo `cadastro_completo` para decidir:
    - `false` → Abre tela de cadastro
    - `true` → Abre app direto com a pontuação
    
    ### Parâmetros:
    - **vem_hash** (string): Hash único do QR Code gerado pelo ESP32
    
    ### Exemplo de uso:
```
    POST /usuarios/verificar/abc123xyz
```
    
    ### Resposta (Usuário novo):
```json
    {
        "vem_hash": "abc123xyz",
        "nome": null,
        "pontuacao": 0,
        "cadastro_completo": false,
        "idade": null
    }
```
    
    ### Resposta (Usuário existente):
```json
    {
        "vem_hash": "abc123xyz",
        "nome": "João Silva",
        "pontuacao": 50,
        "cadastro_completo": true,
        "idade": 28
    }
```
    """
    try:
        return service.verificar_usuario(vem_hash)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar usuário: {str(e)}"
        )

@router.post("/cadastrar",
    response_model=UsuarioResposta,
    summary="Completar cadastro do usuário",
    description="Completa o cadastro com nome, email e data de nascimento.",
    response_description="Dados do usuário cadastrado")
def cadastrar_usuario(dados: UsuarioCadastro):
    """
    ## ✍️ Completar Cadastro
    
    Completa o cadastro do usuário após o QR Code ser escaneado.
    Este endpoint é chamado quando o usuário preenche o formulário no app.
    
    ### Body (JSON):
```json
    {
        "vem_hash": "abc123xyz",
        "nome": "João Silva",
        "email": "joao@email.com",
        "data_nascimento": "1995-03-15"
    }
```
    
    ### Validações:
    - **nome**: mínimo 2 caracteres, máximo 100
    - **email**: formato válido de email
    - **data_nascimento**: não pode ser futura, idade mínima 13 anos
    
    ### Resposta:
```json
    {
        "vem_hash": "abc123xyz",
        "nome": "João Silva",
        "pontuacao": 0,
        "cadastro_completo": true,
        "idade": 28
    }
```
    """
    try:
        return service.completar_cadastro(dados)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao cadastrar usuário: {str(e)}"
        )

@router.post("/{vem_hash}", 
    summary="Criar novo usuário (manual)",
    description="Cria um novo usuário manualmente apenas com o hash. Use /verificar para o fluxo normal.",
    response_description="Usuário criado com sucesso",
    deprecated=True)
def criar_usuario(vem_hash: str):
    """
    ## 📝 Criar Novo Usuário (Manual)
    
    ⚠️ **DEPRECATED**: Use o endpoint `/usuarios/verificar/{vem_hash}` para o fluxo normal.
    
    Este endpoint cria um usuário apenas com o hash.
    Mantido para compatibilidade com versões antigas.
    
    ### Parâmetros:
    - **vem_hash** (string): Hash único do usuário
    
    ### Exemplo de uso:
```
    POST /usuarios/cliente001
```
    """
    # Verifica se o usuário já existe
    if service.existe_usuario(vem_hash):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Usuário já existe"
        )
    return service.criar_usuario(vem_hash)

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
    GET /usuarios/abc123xyz
```
    
    ### Resposta:
```json
    {
        "vem_hash": "abc123xyz",
        "nome": "João Silva",
        "email": "joao@email.com",
        "pontuacao": 50,
        "cadastro_completo": true,
        "data_nascimento": "1995-03-15"
    }
```
    """
    usuario = service.buscar_usuario(vem_hash)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
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
    DELETE /usuarios/abc123xyz
```
    
    ### Resposta:
```json
    {
        "mensagem": "Usuário removido com sucesso",
        "vem_hash": "abc123xyz"
    }
```
    """
    try:
        return service.excluir_usuario(vem_hash)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.patch("/{vem_hash}/pontuacao/{pontos}",
    summary="Atualizar pontuação do usuário",
    description="Adiciona ou remove pontos de um usuário.",
    response_description="Pontuação atualizada com sucesso")
def atualizar_pontuacao(vem_hash: str, pontos: int):
    """
    ## ⚙️ Atualizar Pontuação do Usuário
    
    Adiciona ou remove pontos de um usuário específico.
    
    ### Parâmetros:
    - **vem_hash** (string): Hash único do usuário
    - **pontos** (int): Número de pontos a adicionar (positivo) ou subtrair (negativo)
    
    ### Exemplo de uso:
```
    PATCH /usuarios/abc123xyz/pontuacao/10
```
    
    ### Resposta:
```json
    {
        "vem_hash": "abc123xyz",
        "pontuacao": 60,
        "pontos_adicionados": 10
    }
```
    """
    resultado = service.atualizar_pontuacao(vem_hash, pontos)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return resultado

@router.post("/{vem_hash}/votar",
    summary="Registrar voto e adicionar pontos",
    description="Registra um voto do usuário e adiciona pontos de gamificação.",
    response_description="Voto registrado e pontos adicionados")
def registrar_voto(vem_hash: str, pontos: int = 10):
    """
    ## 🗳️ Registrar Voto (Gamificação)
    
    Registra um voto do usuário e adiciona pontos automaticamente.
    Este endpoint é chamado após o usuário responder uma pergunta no totem.
    
    ### Parâmetros:
    - **vem_hash** (string): Hash único do usuário
    - **pontos** (int): Quantidade de pontos a adicionar (padrão: 10)
    
    ### Exemplo de uso:
```
    POST /usuarios/abc123xyz/votar?pontos=15
```
    
    ### Resposta:
```json
    {
        "mensagem": "Voto registrado com sucesso!",
        "vem_hash": "abc123xyz",
        "pontuacao_atual": 65,
        "pontos_ganhos": 15
    }
```
    """
    try:
        return service.adicionar_pontos_por_voto(vem_hash, pontos)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.patch("/{vem_hash}/atualizar",
    summary="Atualizar dados do usuário",
    description="Atualiza campos específicos de um usuário sem afetar outros dados.",
    response_description="Dados atualizados com sucesso")
def atualizar_dados(vem_hash: str, campos: Dict[str, Any] = Body(...)):
    """
    ## 🔄 Atualizar Dados Parcialmente
    
    Atualiza campos específicos de um usuário sem sobrescrever todos os dados.
    
    ### Parâmetros:
    - **vem_hash** (string): Hash único do usuário
    - **campos** (object): Objeto JSON com os campos a atualizar
    
    ### Campos permitidos:
    - nome
    - email
    - data_nascimento
    
    ### Campos protegidos (não podem ser atualizados):
    - vem_hash
    - pontuacao (use o endpoint específico)
    - data_criacao
    
    ### Exemplo de uso:
```
    PATCH /usuarios/abc123xyz/atualizar
    
    Body:
    {
        "nome": "João Pedro Silva",
        "email": "joao.pedro@email.com"
    }
```
    
    ### Resposta:
```json
    {
        "mensagem": "Dados atualizados com sucesso",
        "vem_hash": "abc123xyz",
        "campos_atualizados": ["nome", "email"]
    }
```
    """
    try:
        return service.atualizar_dados_parcial(vem_hash, campos)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )