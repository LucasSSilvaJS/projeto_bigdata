from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import usuario_routes, pergunta_routes, totem_routes, interacao_routes

app = FastAPI(
    title="API de Interações - Projeto Big Data",
    description="""
    ## 🚀 API para Coleta de Dados de Interações
    
    Uma API REST desenvolvida em FastAPI para gerenciar interações entre usuários, totens e perguntas, 
    com foco em coleta de dados para análise de Big Data.
    
    ### 🎯 Funcionalidades
    
    * **Usuários**: Gerenciamento de usuários identificados por hash único
    * **Totens**: Dispositivos físicos com localização geográfica
    * **Perguntas**: Sistema de perguntas personalizáveis
    * **Interações**: Registro de respostas dos usuários ("sim" ou "não")
    
    ### 📊 Casos de Uso
    
    * Análise de satisfação do cliente
    * Análise geográfica de interações
    * Análise temporal de padrões de uso
    * Coleta de dados para Big Data
    
    ### 🔧 Tecnologias
    
    * **FastAPI** - Framework web moderno
    * **MongoDB** - Banco de dados NoSQL
    * **Uvicorn** - Servidor ASGI
    * **Python 3.13+** - Linguagem de programação
    """,
    version="1.0.0",
    contact={
        "name": "Equipe de Desenvolvimento",
        "email": "dev@projeto-bigdata.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Servidor de Desenvolvimento"
        },
        {
            "url": "https://projeto-bigdata.onrender.com/",
            "description": "Servidor de Produção"
        }
    ]
)

# Configurar CORS para permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(usuario_routes.router)
app.include_router(pergunta_routes.router)
app.include_router(totem_routes.router)
app.include_router(interacao_routes.router)

@app.get("/", tags=["🏠 Início"])
async def root():
    """
    ## 🏠 Página Inicial da API
    
    Bem-vindo à API de Interações! Aqui você pode gerenciar usuários, totens, perguntas e interações.
    
    ### 📋 Links Úteis:
    * **Documentação Swagger**: [/docs](/docs)
    * **Documentação ReDoc**: [/redoc](/redoc)
    * **Schema OpenAPI**: [/openapi.json](/openapi.json)
    
    ### 🚀 Começando:
    1. Acesse [/docs](/docs) para a documentação interativa
    2. Teste os endpoints diretamente na interface
    3. Use os exemplos fornecidos para começar rapidamente
    """
    return {
        "message": "🚀 API de Interações - Projeto Big Data",
        "version": "1.0.0",
        "status": "✅ Funcionando perfeitamente",
        "docs": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "usuarios": "/usuarios/",
            "totens": "/totens/",
            "perguntas": "/perguntas/",
            "interacoes": "/interacoes/"
        },
        "examples": {
            "criar_usuario": "POST /usuarios/?vem_hash=exemplo123",
            "criar_totem": "POST /totens/?totem_id=totem001&latitude=-23.5505&longitude=-46.6333",
            "criar_pergunta": "POST /perguntas/?pergunta_id=pergunta001&texto=Você gostou do atendimento?",
            "criar_interacao": "POST /interacoes/?vem_hash=exemplo123&pergunta_id=pergunta001&totem_id=totem001&resposta=sim"
        }
    }

@app.get("/health", tags=["🏥 Saúde"])
async def health_check():
    """
    ## 🏥 Verificação de Saúde da API
    
    Endpoint para verificar se a API está funcionando corretamente.
    Útil para monitoramento e health checks.
    """
    return {
        "status": "healthy",
        "message": "API funcionando perfeitamente",
        "version": "1.0.0"
    }
