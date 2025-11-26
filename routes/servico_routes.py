from fastapi import APIRouter, HTTPException, status, UploadFile, File
from core.services.servico_service import ServicoService
from models.servico import ServicoCreate, ServicoResposta
from typing import List, Dict, Any
import csv
import io
import openpyxl

router = APIRouter(
    prefix="/servicos",
    tags=["🏢 Serviços Públicos"],
    responses={
        404: {"description": "Serviço não encontrado"},
        422: {"description": "Dados inválidos"}
    }
)

service = ServicoService()

@router.get("/",
    summary="Listar todos os serviços",
    description="Retorna lista de todos os serviços públicos cadastrados.",
    response_description="Lista de serviços")
def listar_servicos(apenas_ativos: bool = True):
    """
    ## 📋 Listar Serviços Públicos
    
    Retorna todos os serviços cadastrados no sistema.
    
    ### Parâmetros:
    - **apenas_ativos** (bool): Se True, retorna apenas serviços ativos (padrão: True)
    
    ### Resposta:
```json
    [
        {
            "servico_id": "abc123",
            "nome": "Detran Recife",
            "tipo": "Transporte",
            "latitude": -8.0476,
            "longitude": -34.8770,
            "endereco": "Rua da Aurora, 123"
        }
    ]
```
    """
    return service.listar_servicos(apenas_ativos=apenas_ativos)

@router.get("/tipos",
    summary="Listar tipos de serviços",
    description="Retorna lista de tipos de serviços disponíveis.",
    response_description="Lista de tipos")
def listar_tipos():
    """
    ## 🏷️ Listar Tipos de Serviços
    
    Retorna todos os tipos de serviços cadastrados (Saúde, Transporte, Educação, etc).
    
    ### Resposta:
```json
    ["Transporte", "Saúde", "Educação", "Segurança"]
```
    """
    return service.listar_tipos_disponiveis()

@router.get("/estatisticas",
    summary="Estatísticas dos serviços",
    description="Retorna estatísticas gerais sobre os serviços cadastrados.",
    response_description="Estatísticas")
def obter_estatisticas():
    """
    ## 📊 Estatísticas de Serviços
    
    Retorna estatísticas sobre os serviços públicos cadastrados.
    
    ### Resposta:
```json
    {
        "total_servicos": 50,
        "servicos_ativos": 48,
        "servicos_inativos": 2,
        "percentual_ativos": 96.0,
        "servicos_por_tipo": {
            "Saúde": 20,
            "Transporte": 15,
            "Educação": 13
        }
    }
```
    """
    return service.obter_estatisticas()

@router.get("/proximos-totem/{totem_id}",
    response_model=List[ServicoResposta],
    summary="Buscar serviços próximos ao totem",
    description="Retorna serviços públicos próximos a um totem específico.",
    response_description="Lista de serviços próximos ordenados por distância")
def buscar_proximos_totem(totem_id: str, raio_km: float = 5.0):
    """
    ## 📍 Buscar Serviços Próximos ao Totem
    
    Retorna lista de serviços públicos dentro de um raio do totem.
    **Lista ordenada por distância (mais próximo primeiro).**
    
    ### Parâmetros:
    - **totem_id** (string): ID do totem
    - **raio_km** (float): Raio de busca em km (padrão: 5.0 km)
    
    ### Exemplo de uso:
```
    GET /servicos/proximos-totem/totem123?raio_km=3.0
```
    
    ### Resposta:
```json
    [
        {
            "servico_id": "abc123",
            "nome": "Detran Recife",
            "tipo": "Transporte",
            "latitude": -8.0476,
            "longitude": -34.8770,
            "distancia_km": 0.5
        },
        {
            "servico_id": "def456",
            "nome": "Hospital da Restauração",
            "tipo": "Saúde",
            "distancia_km": 1.2
        }
    ]
```
    """
    try:
        return service.buscar_proximos_por_totem_id(totem_id, raio_km)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/proximos",
    response_model=List[ServicoResposta],
    summary="Buscar serviços próximos a coordenadas",
    description="Retorna serviços próximos a uma latitude/longitude específica.",
    response_description="Lista de serviços próximos")
def buscar_proximos_coordenadas(
    latitude: float,
    longitude: float,
    raio_km: float = 5.0
):
    """
    ## 🗺️ Buscar Serviços por Coordenadas
    
    Busca serviços próximos a uma coordenada específica.
    
    ### Parâmetros:
    - **latitude** (float): Latitude do ponto
    - **longitude** (float): Longitude do ponto
    - **raio_km** (float): Raio de busca em km (padrão: 5.0)
    
    ### Exemplo:
```
    GET /servicos/proximos?latitude=-8.0476&longitude=-34.8770&raio_km=2.0
```
    """
    return service.buscar_proximos_ao_totem(latitude, longitude, raio_km)

@router.get("/tipo/{tipo}",
    summary="Buscar serviços por tipo",
    description="Retorna todos os serviços de um tipo específico.",
    response_description="Lista de serviços do tipo")
def buscar_por_tipo(tipo: str):
    """
    ## 🏷️ Buscar Serviços por Tipo
    
    Filtra serviços por tipo (Saúde, Transporte, Educação, etc).
    
    ### Exemplo:
```
    GET /servicos/tipo/Saúde
```
    """
    return service.buscar_por_tipo(tipo)

@router.post("/",
    summary="Cadastrar novo serviço",
    description="Cadastra um novo serviço público no sistema.",
    response_description="Serviço criado com sucesso")
def criar_servico(dados: ServicoCreate):
    """
    ## ➕ Cadastrar Novo Serviço
    
    Cadastra um novo serviço público.
    
    ### Body (JSON):
```json
    {
        "nome": "Detran Recife - Boa Vista",
        "tipo": "Transporte",
        "latitude": -8.0476,
        "longitude": -34.8770,
        "endereco": "Rua da Aurora, 123, Boa Vista",
        "telefone": "(81) 3184-9000",
        "horario_funcionamento": "Segunda a Sexta: 8h às 17h",
        "descricao": "Atendimento para CNH, veículos e multas"
    }
```
    
    ### Campos obrigatórios:
    - nome, tipo, latitude, longitude
    
    ### Campos opcionais:
    - endereco, telefone, horario_funcionamento, descricao
    """
    try:
        return service.criar_servico(dados)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar serviço: {str(e)}"
        )

@router.post("/importar-csv",
    summary="Importar serviços via CSV/Excel",
    description="Importa múltiplos serviços de um arquivo CSV ou Excel.",
    response_description="Resultado da importação")
async def importar_servicos(arquivo: UploadFile = File(...)):
    """
    ## 📤 Importar Serviços em Massa
    
    Importa serviços de um arquivo CSV ou Excel (.xlsx).
    
    ### Formato do arquivo CSV:
```csv
    nome,tipo,latitude,longitude,endereco,telefone,horario_funcionamento,descricao
    "Detran Boa Vista","Transporte",-8.0476,-34.8770,"Rua da Aurora, 123","(81) 3184-9000","Seg-Sex: 8h-17h","Atendimento CNH"
    "Hospital Restauração","Saúde",-8.0524,-34.8813,"Av. Gov. Magalhães","(81) 3184-1300","24 horas","Hospital de trauma"
```
    
    ### Formato Excel (.xlsx):
    Mesmas colunas, primeira linha com cabeçalhos.
    
    ### Campos obrigatórios:
    - nome, tipo, latitude, longitude
    
    ### Resposta:
```json
    {
        "total_linhas": 10,
        "importados_com_sucesso": 9,
        "erros": 1,
        "detalhes_erros": [
            {"linha": 5, "erro": "Latitude inválida"}
        ]
    }
```
    """
    try:
        # Lê o conteúdo do arquivo
        conteudo = await arquivo.read()
        
        servicos_criados = 0
        erros = []
        total_linhas = 0
        
        # Detecta o tipo de arquivo
        if arquivo.filename.endswith('.csv'):
            # Processa CSV
            conteudo_str = conteudo.decode('utf-8')
            reader = csv.DictReader(io.StringIO(conteudo_str))
            
            for idx, linha in enumerate(reader, start=2):  # Linha 2 porque linha 1 é cabeçalho
                total_linhas += 1
                try:
                    # Validações básicas
                    if not all(k in linha for k in ['nome', 'tipo', 'latitude', 'longitude']):
                        raise ValueError("Campos obrigatórios faltando")
                    
                    # Cria objeto ServicoCreate
                    servico_data = ServicoCreate(
                        nome=linha['nome'].strip(),
                        tipo=linha['tipo'].strip(),
                        latitude=float(linha['latitude']),
                        longitude=float(linha['longitude']),
                        endereco=linha.get('endereco', '').strip() or None,
                        telefone=linha.get('telefone', '').strip() or None,
                        horario_funcionamento=linha.get('horario_funcionamento', '').strip() or None,
                        descricao=linha.get('descricao', '').strip() or None
                    )
                    
                    # Cria o serviço
                    service.criar_servico(servico_data)
                    servicos_criados += 1
                    
                except Exception as e:
                    erros.append({
                        "linha": idx,
                        "nome": linha.get('nome', 'N/A'),
                        "erro": str(e)
                    })
        
        elif arquivo.filename.endswith(('.xlsx', '.xls')):
            # Processa Excel
            workbook = openpyxl.load_workbook(io.BytesIO(conteudo))
            sheet = workbook.active
            
            # Pega cabeçalhos da primeira linha
            headers = [cell.value for cell in sheet[1]]
            
            for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                total_linhas += 1
                try:
                    # Cria dicionário da linha
                    linha_dict = dict(zip(headers, row))
                    
                    # Validações
                    if not all(k in linha_dict for k in ['nome', 'tipo', 'latitude', 'longitude']):
                        raise ValueError("Campos obrigatórios faltando")
                    
                    # Cria objeto ServicoCreate
                    servico_data = ServicoCreate(
                        nome=str(linha_dict['nome']).strip(),
                        tipo=str(linha_dict['tipo']).strip(),
                        latitude=float(linha_dict['latitude']),
                        longitude=float(linha_dict['longitude']),
                        endereco=str(linha_dict.get('endereco', '')).strip() or None,
                        telefone=str(linha_dict.get('telefone', '')).strip() or None,
                        horario_funcionamento=str(linha_dict.get('horario_funcionamento', '')).strip() or None,
                        descricao=str(linha_dict.get('descricao', '')).strip() or None
                    )
                    
                    # Cria o serviço
                    service.criar_servico(servico_data)
                    servicos_criados += 1
                    
                except Exception as e:
                    erros.append({
                        "linha": idx,
                        "nome": linha_dict.get('nome', 'N/A') if 'linha_dict' in locals() else 'N/A',
                        "erro": str(e)
                    })
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de arquivo não suportado. Use .csv ou .xlsx"
            )
        
        return {
            "mensagem": "Importação concluída",
            "total_linhas": total_linhas,
            "importados_com_sucesso": servicos_criados,
            "com_erros": len(erros),
            "taxa_sucesso": round((servicos_criados / total_linhas * 100), 2) if total_linhas > 0 else 0,
            "detalhes_erros": erros[:10]  # Mostra no máximo 10 erros
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar arquivo: {str(e)}"
        )

@router.get("/{servico_id}",
    summary="Buscar serviço por ID",
    description="Retorna detalhes de um serviço específico.",
    response_description="Dados do serviço")
def buscar_servico(servico_id: str):
    """
    ## 🔍 Buscar Serviço por ID
    
    Retorna os detalhes completos de um serviço.
    
    ### Exemplo:
```
    GET /servicos/abc123
```
    """
    servico = service.buscar_servico(servico_id)
    if not servico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Serviço não encontrado"
        )
    return servico

@router.patch("/{servico_id}",
    summary="Atualizar serviço",
    description="Atualiza dados de um serviço específico.",
    response_description="Serviço atualizado")
def atualizar_servico(servico_id: str, campos: Dict[str, Any]):
    """
    ## 🔄 Atualizar Serviço
    
    Atualiza campos específicos de um serviço.
    
    ### Exemplo:
```json
    {
        "telefone": "(81) 9999-9999",
        "horario_funcionamento": "24 horas"
    }
```
    """
    try:
        return service.atualizar_servico(servico_id, campos)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{servico_id}",
    summary="Excluir serviço",
    description="Remove um serviço do sistema.",
    response_description="Confirmação de exclusão")
def excluir_servico(servico_id: str, permanente: bool = False):
    """
    ## 🗑️ Excluir Serviço
    
    Remove um serviço (soft delete por padrão).
    
    ### Parâmetros:
    - **permanente** (bool): Se True, deleta permanentemente. Se False, apenas desativa.
    """
    try:
        return service.excluir_servico(servico_id, soft_delete=not permanente)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/{servico_id}/reativar",
    summary="Reativar serviço",
    description="Reativa um serviço que foi desativado.",
    response_description="Confirmação de reativação")
def reativar_servico(servico_id: str):
    """
    ## ♻️ Reativar Serviço
    
    Reativa um serviço que foi desativado anteriormente.
    """
    try:
        return service.reativar_servico(servico_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )