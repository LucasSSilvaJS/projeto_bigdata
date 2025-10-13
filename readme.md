# API de Interações - Projeto Big Data

Uma API REST desenvolvida em FastAPI para gerenciar interações entre usuários, totens e perguntas, com foco em coleta de dados para análise de Big Data.

## 📋 Visão Geral

Este projeto implementa um sistema de interações onde:
- **Usuários** podem responder perguntas através de **Totens**
- As **Interações** são registradas para posterior análise de dados
- Utiliza arquitetura em camadas (Repository Pattern) para organização do código
- Banco de dados MongoDB para armazenamento dos dados

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas bem definida:

```
projeto_bigdata/
├── app.py                 # Aplicação principal FastAPI
├── core/                  # Lógica de negócio
│   ├── database.py        # Configuração do MongoDB
│   ├── repositories/      # Camada de acesso a dados
│   └── services/          # Camada de serviços
├── models/                # Modelos de dados
├── routes/                # Endpoints da API
└── requirements.txt       # Dependências do projeto
```

## 🚀 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido para APIs
- **MongoDB** - Banco de dados NoSQL para armazenamento
- **PyMongo** - Driver oficial do MongoDB para Python
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI para FastAPI
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

## 📦 Instalação e Configuração

### 1. Pré-requisitos

- Python 3.7+ (testado com Python 3.13.6)
- MongoDB (local ou na nuvem)
- Git (para clonar o repositório)

### 2. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd projeto_bigdata
```

### 3. Configurar Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

### 4. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 5. Configuração do Banco de Dados

#### Opção A: MongoDB Local
Instale o MongoDB localmente e certifique-se de que está rodando na porta padrão 27017.

#### Opção B: MongoDB com Docker
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

#### Opção C: MongoDB Atlas (Nuvem)
Use uma string de conexão do MongoDB Atlas.

### 6. Configuração do Ambiente

O arquivo `.env` será criado automaticamente com as configurações padrão:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=projeto_bigdata
```

**Para MongoDB Atlas, edite o arquivo `.env`:**
```env
MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/
MONGODB_DB_NAME=projeto_bigdata
```

### 7. Executar a Aplicação

```bash
# Desenvolvimento (com reload automático)
uvicorn app:app --reload

# Produção
uvicorn app:app --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

### 8. Verificar se está Funcionando

Acesse no navegador:
- **🏠 Página Inicial**: `http://localhost:8000`
- **📚 Documentação Swagger**: `http://localhost:8000/docs`
- **📖 Documentação ReDoc**: `http://localhost:8000/redoc`
- **🔧 Schema OpenAPI**: `http://localhost:8000/openapi.json`
- **🏥 Health Check**: `http://localhost:8000/health`

### 9. Testes Rápidos

#### No Windows (PowerShell):
```powershell
# Criar usuário
Invoke-WebRequest -Uri "http://localhost:8000/usuarios/?vem_hash=teste123" -Method POST

# Listar usuários
Invoke-WebRequest -Uri "http://localhost:8000/usuarios/" -Method GET

# Criar totem
Invoke-WebRequest -Uri "http://localhost:8000/totens/?totem_id=totem001&latitude=-23.5505&longitude=-46.6333" -Method POST
```

#### No Linux/Mac:
```bash
# Criar usuário
curl -X POST "http://localhost:8000/usuarios/?vem_hash=teste123"

# Listar usuários
curl http://localhost:8000/usuarios/

# Criar totem
curl -X POST "http://localhost:8000/totens/?totem_id=totem001&latitude=-23.5505&longitude=-46.6333"
```

## 📊 Entidades do Sistema

### 👤 Usuário
Representa um usuário do sistema identificado por um hash único.

**Atributos:**
- `vem_hash` (string): Identificador único do usuário

### 🤖 Totem
Representa um dispositivo físico onde os usuários podem interagir.

**Atributos:**
- `totem_id` (string): Identificador único gerado automaticamente via hash
- `latitude` (float): Coordenada geográfica
- `longitude` (float): Coordenada geográfica
- `data_criacao` (string): Data e hora de criação do totem

### ❓ Pergunta
Representa uma pergunta que pode ser respondida pelos usuários.

**Atributos:**
- `pergunta_id` (string): Identificador único gerado automaticamente via hash
- `texto` (string): Texto da pergunta
- `data_criacao` (string): Data e hora de criação da pergunta

### 🔄 Interação
Registra a resposta de um usuário a uma pergunta em um totem específico.

**Atributos:**
- `vem_hash` (string): Hash do usuário
- `pergunta_id` (string): ID da pergunta respondida
- `totem_id` (string): ID do totem onde ocorreu a interação
- `resposta` (string): Resposta do usuário ("sim" ou "não")

## 🛠️ Endpoints da API

### Usuários (`/usuarios`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/usuarios/` | Criar novo usuário |
| GET | `/usuarios/` | Listar todos os usuários |
| GET | `/usuarios/{vem_hash}` | Buscar usuário por hash |
| DELETE | `/usuarios/{vem_hash}` | Excluir usuário |

### Totens (`/totens`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/totens/` | Criar novo totem |
| GET | `/totens/` | Listar todos os totens |
| GET | `/totens/{totem_id}` | Buscar totem por ID |
| DELETE | `/totens/{totem_id}` | Excluir totem |

### Perguntas (`/perguntas`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/perguntas/` | Criar nova pergunta |
| GET | `/perguntas/` | Listar todas as perguntas |
| GET | `/perguntas/{pergunta_id}` | Buscar pergunta por ID |
| DELETE | `/perguntas/{pergunta_id}` | Excluir pergunta |

### Interações (`/interacoes`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/interacoes/` | Registrar nova interação |
| GET | `/interacoes/` | Listar todas as interações |

## 💡 Exemplos de Uso

### 🚀 Via Interface Swagger (Recomendado)

A documentação Swagger foi completamente desenvolvida com:

#### ✨ **Funcionalidades do Swagger:**
- **📚 Documentação Interativa**: Teste todos os endpoints diretamente
- **🎯 Exemplos Prontos**: Parâmetros pré-preenchidos para teste rápido
- **📋 Descrições Detalhadas**: Cada endpoint com explicação completa
- **🔍 Validação Automática**: Validação de parâmetros em tempo real
- **📊 Respostas de Exemplo**: Veja exatamente o que cada endpoint retorna
- **🏷️ Tags Organizadas**: Endpoints agrupados por funcionalidade
- **🎨 Interface Moderna**: Design limpo e intuitivo

#### 📖 **Como Usar:**
1. **Acesse**: `http://localhost:8000/docs`
2. **Explore**: Navegue pelas seções (👤 Usuários, 🤖 Totens, etc.)
3. **Teste**: Clique em "Try it out" em qualquer endpoint
4. **Execute**: Clique em "Execute" para testar
5. **Analise**: Veja a resposta e códigos de status

#### 🎯 **Endpoints Principais no Swagger:**
- **🏠 Página Inicial**: `/` - Informações gerais da API
- **🏥 Health Check**: `/health` - Status da aplicação
- **👤 Usuários**: `/usuarios/` - CRUD completo
- **🤖 Totens**: `/totens/` - CRUD com coordenadas
- **❓ Perguntas**: `/perguntas/` - CRUD de perguntas
- **🔄 Interações**: `/interacoes/` - Registro de respostas

### Via Linha de Comando

#### Windows (PowerShell):
```powershell
# Criar usuário
Invoke-WebRequest -Uri "http://localhost:8000/usuarios/?vem_hash=user123" -Method POST

# Criar totem (ID gerado automaticamente)
Invoke-WebRequest -Uri "http://localhost:8000/totens/?latitude=-23.5505&longitude=-46.6333" -Method POST

# Criar pergunta (ID gerado automaticamente)
Invoke-WebRequest -Uri "http://localhost:8000/perguntas/?texto=Você gostou do atendimento?" -Method POST

# Registrar interação
Invoke-WebRequest -Uri "http://localhost:8000/interacoes/?vem_hash=user123&pergunta_id=pergunta001&totem_id=totem001&resposta=sim" -Method POST

# Listar dados
Invoke-WebRequest -Uri "http://localhost:8000/usuarios/" -Method GET
Invoke-WebRequest -Uri "http://localhost:8000/interacoes/" -Method GET
```

#### Linux/Mac:
```bash
# Criar usuário
curl -X POST "http://localhost:8000/usuarios/?vem_hash=user123"

# Criar totem (ID gerado automaticamente)
curl -X POST "http://localhost:8000/totens/?latitude=-23.5505&longitude=-46.6333"

# Criar pergunta (ID gerado automaticamente)
curl -X POST "http://localhost:8000/perguntas/?texto=Você gostou do atendimento?"

# Registrar interação
curl -X POST "http://localhost:8000/interacoes/?vem_hash=user123&pergunta_id=pergunta001&totem_id=totem001&resposta=sim"

# Listar dados
curl http://localhost:8000/usuarios/
curl http://localhost:8000/interacoes/
```

### Exemplo de Fluxo Completo
```powershell
# 1. Criar usuário
Invoke-WebRequest -Uri "http://localhost:8000/usuarios/?vem_hash=cliente001" -Method POST

# 2. Criar totem (ID gerado automaticamente)
$totem = Invoke-WebRequest -Uri "http://localhost:8000/totens/?latitude=-23.5505&longitude=-46.6333" -Method POST
$totem_id = ($totem.Content | ConvertFrom-Json).totem_id

# 3. Criar pergunta (ID gerado automaticamente)
$pergunta = Invoke-WebRequest -Uri "http://localhost:8000/perguntas/?texto=Você ficou satisfeito com nosso atendimento?" -Method POST
$pergunta_id = ($pergunta.Content | ConvertFrom-Json).pergunta_id

# 4. Registrar interação usando IDs gerados
Invoke-WebRequest -Uri "http://localhost:8000/interacoes/?vem_hash=cliente001&pergunta_id=$pergunta_id&totem_id=$totem_id&resposta=sim" -Method POST

# 5. Verificar dados salvos
Invoke-WebRequest -Uri "http://localhost:8000/interacoes/" -Method GET
```

## 🏛️ Padrões de Arquitetura

### Repository Pattern
- **Repositories**: Responsáveis pelo acesso aos dados
- **Services**: Contêm a lógica de negócio
- **Models**: Representam as entidades do domínio
- **Routes**: Definem os endpoints da API

### Singleton Pattern
- **MongoConnection**: Garante uma única instância de conexão com o MongoDB

## 📈 Casos de Uso para Big Data

Este sistema é projetado para coleta de dados em larga escala:

### 🎯 **Cenários de Uso**

1. **Análise de Satisfação**: Coleta respostas sobre qualidade do atendimento
2. **Análise Geográfica**: Correlação entre localização dos totens e respostas
3. **Análise Temporal**: Padrões de interação ao longo do tempo
4. **Análise de Usuários**: Comportamento individual e segmentação
5. **Análise de Totens**: Performance e utilização por dispositivo

### 📊 **Exemplos de Dashboards**

#### Dashboard de Satisfação
```javascript
// Consulta MongoDB para análise de satisfação
db.interacoes.aggregate([
  { $match: { pergunta_id: "satisfacao001" } },
  { $group: { 
    _id: "$resposta", 
    count: { $sum: 1 } 
  }}
])
```

#### Dashboard Geográfico
```javascript
// Análise por localização
db.interacoes.aggregate([
  { $lookup: {
    from: "totens",
    localField: "totem_id", 
    foreignField: "totem_id",
    as: "totem_info"
  }},
  { $group: {
    _id: "$totem_info.latitude",
    interacoes: { $sum: 1 }
  }}
])
```

### 🔄 **Pipeline de Dados**

1. **Coleta**: Usuários interagem via totens
2. **Armazenamento**: Dados salvos no MongoDB
3. **Processamento**: Queries agregadas para análise
4. **Visualização**: Dashboards e relatórios
5. **Insights**: Tomada de decisões baseada em dados

### 📈 **Métricas Disponíveis**

- **Taxa de Satisfação**: % de respostas "sim"
- **Volume de Interações**: Total por período
- **Distribuição Geográfica**: Interações por região
- **Performance de Totens**: Uso por dispositivo
- **Padrões Temporais**: Horários de pico de uso

## 🔧 Desenvolvimento

### Estrutura do Código

- **Separação de responsabilidades** clara entre camadas
- **Validação de dados** nos modelos (respostas limitadas a "sim" ou "não")
- **Tratamento de erros** estruturado
- **Código limpo** e bem documentado
- **Singleton Pattern** para conexão MongoDB
- **Repository Pattern** para acesso a dados

### Funcionalidades Implementadas

✅ **CRUD Completo para Usuários**
- Criar, listar, buscar e excluir usuários
- Identificação por hash único

✅ **CRUD Completo para Totens**
- Criar, listar, buscar e excluir totens
- Localização geográfica (latitude/longitude)
- **ID gerado automaticamente** via hash MD5 baseado em coordenadas + timestamp

✅ **CRUD Completo para Perguntas**
- Criar, listar, buscar e excluir perguntas
- Texto personalizado para cada pergunta
- **ID gerado automaticamente** via hash MD5 baseado no texto + timestamp

✅ **Sistema de Interações**
- Registrar respostas dos usuários
- Validação de respostas ("sim" ou "não")
- Relacionamento entre usuário, pergunta e totem

✅ **API REST Completa**
- Documentação automática com Swagger
- Parâmetros via query string
- Respostas em JSON

✅ **Integração MongoDB**
- Conexão automática via variáveis de ambiente
- Persistência de dados
- Consultas otimizadas

✅ **Documentação Swagger Completa**
- Interface interativa profissional
- Exemplos de uso pré-preenchidos
- Validação automática de parâmetros
- Respostas de exemplo detalhadas
- Organização por tags com emojis
- Tratamento de erros documentado

✅ **Geração Automática de IDs**
- **Totens**: ID gerado via hash MD5 (coordenadas + timestamp)
- **Perguntas**: ID gerado via hash MD5 (texto + timestamp)
- **Usuários**: ID fornecido pelo usuário (vem_hash)
- **Timestamps**: Data de criação automática para totens e perguntas

### Comandos de Desenvolvimento

```bash
# Rodar em modo desenvolvimento
uvicorn app:app --reload

# Rodar em porta específica
uvicorn app:app --reload --port 8001

# Rodar em modo produção
uvicorn app:app --host 0.0.0.0 --port 8000

# Verificar sintaxe Python
python -c "from app import app; print('API OK')"

# Instalar dependências de desenvolvimento
pip install pytest black flake8
```

### Estrutura de Logs

O servidor mostra logs detalhados:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
INFO:     127.0.0.1:62770 - "GET /usuarios/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:62791 - "POST /usuarios/?vem_hash=teste123 HTTP/1.1" 200 OK
```

## 🚀 Guia de Inicialização Rápida

### Para Desenvolvedores

```bash
# 1. Clone o projeto
git clone <url-do-repositorio>
cd projeto_bigdata

# 2. Configure ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instale dependências
pip install -r requirements.txt

# 4. Inicie MongoDB (Docker)
docker run -d -p 27017:27017 --name mongodb mongo:latest

# 5. Execute a API
uvicorn app:app --reload

# 6. Teste no navegador
# http://localhost:8000/docs
```

### Para Produção

```bash
# 1. Configure variáveis de ambiente
export MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
export MONGODB_DB_NAME="projeto_bigdata"

# 2. Execute em modo produção
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🔐 Geração Automática de IDs

### 🎯 **Sistema de IDs Automáticos**

A API implementa um sistema robusto de geração automática de IDs:

#### 🤖 **Totens**
- **Algoritmo**: Hash MD5 baseado em `latitude_longitude_timestamp`
- **Tamanho**: 12 caracteres hexadecimais
- **Exemplo**: `bb571e7aa2a6`
- **Vantagem**: IDs únicos baseados na localização geográfica

#### ❓ **Perguntas**
- **Algoritmo**: Hash MD5 baseado em `texto_timestamp`
- **Tamanho**: 12 caracteres hexadecimais
- **Exemplo**: `b7eaf3a2303a`
- **Vantagem**: IDs únicos baseados no conteúdo da pergunta

#### 👤 **Usuários**
- **Sistema**: ID fornecido pelo usuário (`vem_hash`)
- **Flexibilidade**: Permite integração com sistemas externos
- **Uso**: Identificação personalizada por aplicação

#### 📅 **Timestamps Automáticos**
- **Campo**: `data_criacao`
- **Formato**: ISO 8601 (`2025-10-12T23:40:14.618520`)
- **Uso**: Rastreamento temporal para análise de Big Data

### 🔧 **Implementação Técnica**

```python
def _gerar_id(self):
    """Gera um ID único baseado nos dados e timestamp"""
    timestamp = str(datetime.now().timestamp())
    dados = f"{self.latitude}_{self.longitude}_{timestamp}"  # Para totens
    # dados = f"{self.texto}_{timestamp}"  # Para perguntas
    return hashlib.md5(dados.encode()).hexdigest()[:12]
```

### ✅ **Benefícios**

1. **Único**: Impossível gerar IDs duplicados
2. **Rastreável**: Baseado em dados específicos do objeto
3. **Eficiente**: Hash MD5 rápido e confiável
4. **Consistente**: Mesmo algoritmo para todos os objetos
5. **Temporal**: Timestamp garante unicidade temporal

## 🔧 Troubleshooting

### Problemas Comuns

#### ❌ Erro de Conexão MongoDB
```
ValueError: As variáveis MONGODB_URI e MONGODB_DB_NAME precisam estar definidas no .env
```
**Solução**: Verifique se o arquivo `.env` existe e contém as variáveis corretas.

#### ❌ Erro de Encoding no .env
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff
```
**Solução**: Delete o arquivo `.env` e recrie com:
```powershell
New-Item -Path ".env" -ItemType File -Force
Add-Content -Path ".env" -Value "MONGODB_URI=mongodb://localhost:27017"
Add-Content -Path ".env" -Value "MONGODB_DB_NAME=projeto_bigdata"
```

#### ❌ MongoDB não está rodando
```
pymongo.errors.ServerSelectionTimeoutError
```
**Soluções**:
- **Local**: Inicie o serviço MongoDB
- **Docker**: `docker run -d -p 27017:27017 --name mongodb mongo:latest`
- **Atlas**: Verifique a string de conexão

#### ❌ Porta já em uso
```
ERROR: [Errno 98] Address already in use
```
**Solução**: Use porta diferente: `uvicorn app:app --reload --port 8001`

#### ❌ PowerShell não reconhece curl
```
curl : No possvel localizar um parmetro que coincida com o nome de parmetro 'X'
```
**Solução**: Use `Invoke-WebRequest` em vez de `curl` no PowerShell.

### Verificação de Saúde da API

```powershell
# Teste básico
Invoke-WebRequest -Uri "http://localhost:8000/usuarios/" -Method GET

# Deve retornar: StatusCode 200 com Content: []
```

### Logs Úteis

```bash
# Ver logs detalhados
uvicorn app:app --reload --log-level debug

# Logs de exemplo:
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
INFO:     127.0.0.1:62770 - "GET /usuarios/ HTTP/1.1" 200 OK
```

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais e de demonstração.

## 👥 Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 🎯 Status da Implementação

### ✅ **Funcionalidades Testadas e Funcionando**

- **API REST Completa**: Todos os endpoints respondendo corretamente
- **Documentação Automática**: Swagger UI e ReDoc funcionais
- **Integração MongoDB**: Conexão e persistência de dados operacional
- **Validação de Dados**: Modelos validando entrada corretamente
- **Arquitetura em Camadas**: Repository e Service patterns implementados
- **Logs Detalhados**: Monitoramento de requisições ativo

### 🧪 **Testes Realizados**

```powershell
# Testes de CRUD - TODOS FUNCIONANDO ✅
✅ POST /usuarios/?vem_hash=teste123
✅ GET /usuarios/
✅ POST /totens/?totem_id=totem001&latitude=-23.5505&longitude=-46.6333
✅ POST /perguntas/?pergunta_id=pergunta001&texto=Você gostou do atendimento?
✅ POST /interacoes/?vem_hash=teste123&pergunta_id=pergunta001&totem_id=totem001&resposta=sim
✅ GET /interacoes/
```

### 📊 **Dados de Exemplo Criados**

- **1 Usuário**: `{"vem_hash":"teste123"}`
- **1 Totem**: `{"totem_id":"totem001","latitude":-23.5505,"longitude":-46.6333}`
- **1 Pergunta**: `{"pergunta_id":"pergunta001","texto":"Você gostou do atendimento?"}`
- **1 Interação**: `{"vem_hash":"teste123","pergunta_id":"pergunta001","totem_id":"totem001","resposta":"sim"}`

### 🎯 **Swagger Desenvolvido e Funcionando**

✅ **Interface Swagger Profissional:**
- **Página Inicial**: `/` - Informações completas da API
- **Health Check**: `/health` - Status da aplicação
- **Documentação Interativa**: `/docs` - Teste todos os endpoints
- **ReDoc**: `/redoc` - Documentação alternativa
- **OpenAPI Schema**: `/openapi.json` - Schema completo

✅ **Funcionalidades do Swagger:**
- **Exemplos Pré-preenchidos**: Todos os parâmetros com exemplos
- **Validação Visual**: Erros mostrados em tempo real
- **Respostas Detalhadas**: Exemplos de retorno para cada endpoint
- **Tags Organizadas**: Endpoints agrupados com emojis
- **Descrições Completas**: Cada endpoint totalmente documentado

### 🚀 **Pronto para Uso**

A API está **100% funcional** e pronta para:
- ✅ Coleta de dados em produção
- ✅ Integração com sistemas externos
- ✅ Desenvolvimento de dashboards
- ✅ Análise de Big Data
- ✅ Expansão de funcionalidades

### 🔗 **Links Úteis**

#### 🌐 **Acesso Rápido**
- **🏠 Página Inicial**: [http://localhost:8000](http://localhost:8000)
- **📚 Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **📖 ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **🔧 OpenAPI Schema**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)
- **🏥 Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

#### 📋 **Endpoints Principais**
- **👤 Usuários**: [http://localhost:8000/usuarios/](http://localhost:8000/usuarios/)
- **🤖 Totens**: [http://localhost:8000/totens/](http://localhost:8000/totens/)
- **❓ Perguntas**: [http://localhost:8000/perguntas/](http://localhost:8000/perguntas/)
- **🔄 Interações**: [http://localhost:8000/interacoes/](http://localhost:8000/interacoes/)

#### 🚀 **Testes Rápidos**
- **Criar Usuário**: [http://localhost:8000/docs#/Usuários/criar_usuario_usuarios__post](http://localhost:8000/docs#/Usuários/criar_usuario_usuarios__post)
- **Listar Totens**: [http://localhost:8000/docs#/Totens/listar_totens_totens__get](http://localhost:8000/docs#/Totens/listar_totens_totens__get)
- **Criar Interação**: [http://localhost:8000/docs#/Interações/criar_interacao_interacoes__post](http://localhost:8000/docs#/Interações/criar_interacao_interacoes__post)

---

**Desenvolvido com ❤️ usando FastAPI e MongoDB**  
**Status: ✅ FUNCIONANDO PERFEITAMENTE**
