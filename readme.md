# 🧠 API de Interações — Projeto Big Data

Sistema **RESTful** desenvolvido com **FastAPI** para gerenciar interações entre **Usuários**, **Totens** e **Perguntas**, com foco na **coleta e análise de dados (Big Data)**.

---

## 🚀 Início Rápido

### 1️⃣ Instalação
```bash
pip install -r requirements.txt
```

### 2️⃣ Configuração
O projeto utiliza **variáveis de ambiente**.  
É obrigatória a configuração do **MongoDB**:

```bash
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=projeto_bigdata
```

### 3️⃣ Execução

**Modo Desenvolvimento (com reload automático):**
```bash
uvicorn app:app --reload
```

**Modo Produção:**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 📡 API Endpoints

### 📘 Documentação Swagger
- **URL:** [http://localhost:8000/docs/](http://localhost:8000/docs/)
- **Descrição:** Interface interativa gerada automaticamente pelo **FastAPI/Swagger UI**.

---

### 🔍 Principais Endpoints

| Método | Endpoint | Descrição |
|:-------|:----------|:-----------|
| **POST** | `/usuarios/` | Cria novo usuário (`vem_hash`) |
| **GET** | `/usuarios/{vem_hash}` | Busca usuário por hash |
| **POST** | `/totens/` | Cria novo totem (`latitude`, `longitude`) |
| **GET** | `/totens/{totem_id}` | Busca totem por ID |
| **POST** | `/perguntas/` | Cria nova pergunta (`texto`) |
| **GET** | `/perguntas/{pergunta_id}` | Busca pergunta por ID |
| **POST** | `/interacoes/` | Registra interação (`resposta` do usuário) |
| **GET** | `/interacoes/` | Lista todas as interações |
| **GET** | `/health` | Verifica o status da aplicação |

---

## ⚙️ Configurações Principais

### Banco de Dados — MongoDB
```bash
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=projeto_bigdata
```

---

## 🔧 Scripts Úteis

### Teste Rápido
```bash
curl -X POST "http://localhost:8000/usuarios/?vem_hash=teste123"
```

---

## 📊 Funcionamento do Sistema

O sistema registra **interações de usuários** (identificados por um *hash*) em **totens físicos**, respondendo a perguntas.  
Os dados são armazenados no **MongoDB** para posterior **análise de Big Data**.

**Fluxo Geral:**
1. 🧍 **Extração:** Usuários interagem via totens.  
2. 💾 **Armazenamento:** Dados são salvos no MongoDB.  
3. 📈 **Análise:** Consultas agregadas geram dashboards (Satisfação, Geográfica, Temporal).

---

## 🏗️ Estrutura do Projeto

```
projeto_bigdata/
├── app.py                 # Aplicação principal (FastAPI)
├── core/                  # Lógica de negócio (database, repositories, services)
├── models/                # Modelos de dados (Pydantic/MongoDB)
├── routes/                # Endpoints da API
└── requirements.txt       # Dependências do projeto
```

---

## 🧪 Exemplo de Uso

### Registrar uma Interação
```bash
curl -X POST "http://localhost:8000/interacoes/?vem_hash=user123&pergunta_id=pergunta001&totem_id=totem001&resposta=sim"
```

---

## 🩺 Troubleshooting

| Problema | Solução |
|:----------|:---------|
| ❌ **Erro de conexão** | Verifique `MONGODB_URI` e se o MongoDB está em execução. |
| ⚠️ **Banco não existe** | O MongoDB cria a base automaticamente no primeiro uso. |
| 🧩 **Validação de dados** | Confira os requisitos do modelo Pydantic na documentação Swagger. |

---

📘 **Autor:** Projeto Acadêmico — API de Interações com FastAPI e MongoDB  
📅 **Versão:** 1.0.0  
📍 **Licença:** MIT  
