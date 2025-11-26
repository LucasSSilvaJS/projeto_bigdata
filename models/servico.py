from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field
import hashlib

class Servico(BaseModel):
    """
    Modelo para serviços públicos (Detran, Hospitais, Escolas, etc)
    que ficam próximos aos totens
    """
    servico_id: str = Field(..., description="ID único do serviço")
    nome: str = Field(..., min_length=2, max_length=200, description="Nome do serviço")
    tipo: str = Field(..., description="Tipo do serviço (Saúde, Transporte, Educação, etc)")
    latitude: float = Field(..., description="Latitude da localização")
    longitude: float = Field(..., description="Longitude da localização")
    endereco: Optional[str] = Field(None, max_length=300, description="Endereço completo")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone de contato")
    horario_funcionamento: Optional[str] = Field(None, max_length=100, description="Horário de funcionamento")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição do serviço")
    ativo: bool = Field(default=True, description="Se o serviço está ativo")
    data_criacao: datetime = Field(default_factory=datetime.utcnow, description="Data de criação")
    ultima_atualizacao: datetime = Field(default_factory=datetime.utcnow, description="Última atualização")
    
    @staticmethod
    def gerar_id(nome: str, latitude: float, longitude: float) -> str:
        """Gera um ID único baseado no nome e coordenadas"""
        dados = f"{nome}_{latitude}_{longitude}"
        return hashlib.md5(dados.encode()).hexdigest()[:12]
    
    def calcular_distancia(self, lat: float, lon: float) -> float:
        """
        Calcula a distância em km entre o serviço e um ponto (usando fórmula de Haversine)
        """
        from math import radians, sin, cos, sqrt, atan2
        
        # Raio da Terra em km
        R = 6371.0
        
        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(lat)
        lon2 = radians(lon)
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distancia = R * c
        return round(distancia, 2)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ServicoCreate(BaseModel):
    """Schema para criar um novo serviço"""
    nome: str = Field(..., min_length=2, max_length=200)
    tipo: str
    latitude: float
    longitude: float
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    horario_funcionamento: Optional[str] = None
    descricao: Optional[str] = None


class ServicoResposta(BaseModel):
    """Schema para resposta da API"""
    servico_id: str
    nome: str
    tipo: str
    latitude: float
    longitude: float
    endereco: Optional[str]
    telefone: Optional[str]
    horario_funcionamento: Optional[str]
    descricao: Optional[str]
    ativo: bool
    distancia_km: Optional[float] = None  # Distância do totem (quando aplicável)
    
    class Config:
        from_attributes = True