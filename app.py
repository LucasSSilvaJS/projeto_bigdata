from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import usuario_routes, pergunta_routes, totem_routes, interacao_routes, thanos_routes, servico_routes

app = FastAPI(
    title="API de Interações - Projeto Big Data",
    description="""
    ## 🚀 API para Coleta de Dados de Interações
    
    Uma API REST desenvolvida em FastAPI para gerenciar interações entre usuários, totens e perguntas, 
    com foco em coleta de dados para análise de Big Data.
    
    ### 🎯 Funcionalidades
    
    * **Usuários**: Gerenciamento de usuários identificados por hash único com gamificação
    * **Totens**: Dispositivos físicos com localização geográfica
    * **Serviços Públicos**: Mapeamento de órgãos públicos próximos aos totens
    * **Perguntas**: Sistema de pesquisas públicas sobre a cidade
    * **Interações**: Registro de respostas dos usuários ("sim" ou "não")
    
    ### 📊 Casos de Uso
    
    * Pesquisas de opinião pública sobre temas da cidade
    * Mapeamento e avaliação de serviços públicos
    * Análise geográfica de interações
    * Análise temporal de padrões de uso
    * Gamificação para engajamento dos cidadãos
    * Coleta de dados para Big Data
    
    ### 🔧 Tecnologias
    
    * **FastAPI** - Framework web moderno
    * **MongoDB Atlas** - Banco de dados NoSQL em cloud
    * **Pydantic** - Validação de dados
    * **Uvicorn** - Servidor ASGI
    * **Python 3.13+** - Linguagem de programação
    """,
    version="2.0.0",
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
app.include_router(servico_routes.router)  # NOVO!
app.include_router(interacao_routes.router)
app.include_router(thanos_routes.router)

@app.get("/", tags=["🏠 Início"])
async def root():
    """
    ## 🏠 Página Inicial da API
    
    Bem-vindo à API de Interações! Aqui você pode gerenciar usuários, totens, serviços públicos, perguntas e interações.
    
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
        "version": "2.0.0",
        "status": "✅ Funcionando perfeitamente",
        "docs": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "usuarios": "/usuarios/",
            "totens": "/totens/",
            "servicos": "/servicos/",
            "perguntas": "/perguntas/",
            "interacoes": "/interacoes/",
            "thanos": "/thanos/estalando"
        },
        "examples": {
            "verificar_usuario": "POST /usuarios/verificar/abc123",
            "cadastrar_usuario": "POST /usuarios/cadastrar",
            "criar_totem": "POST /totens/",
            "criar_servico": "POST /servicos/",
            "importar_servicos": "POST /servicos/importar-csv",
            "servicos_proximos": "GET /servicos/proximos-totem/totem123?raio_km=5",
            "criar_pergunta": "POST /perguntas/",
            "criar_interacao": "POST /interacoes/",
            "thanos_estalo": "POST /thanos/estalando"
        },
        "novidades_v2": {
            "gamificacao": "Sistema de pontos e níveis para usuários",
            "servicos_publicos": "Mapeamento de órgãos públicos próximos aos totens",
            "cadastro_completo": "Nome, email e data de nascimento dos usuários",
            "importacao_massa": "Importar serviços via Excel/CSV",
            "analytics": "Estatísticas de idade, ranking e muito mais"
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
        "version": "2.0.0"
    }