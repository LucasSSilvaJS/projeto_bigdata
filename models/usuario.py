from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class Usuario(BaseModel):
    """
    Modelo de usuário para o sistema de votação com gamificação
    """
    vem_hash: str = Field(..., description="Hash único do usuário")
    nome: Optional[str] = Field(None, max_length=100, description="Nome do usuário")
    email: Optional[EmailStr] = Field(None, description="Email do usuário")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento do usuário")
    pontuacao: int = Field(default=0, ge=0, description="Pontuação acumulada")
    cadastro_completo: bool = Field(default=False, description="Indica se o cadastro está completo")
    data_criacao: datetime = Field(default_factory=datetime.utcnow, description="Data de criação do registro")
    ultima_atualizacao: datetime = Field(default_factory=datetime.utcnow, description="Data da última atualização")
    
    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento(cls, v):
        """Valida se a data de nascimento não é futura e se o usuário tem idade mínima"""
        if v:
            if v > date.today():
                raise ValueError('Data de nascimento não pode ser futura')
            
            # Calcula idade
            idade = (date.today() - v).days // 365
            if idade < 13:
                raise ValueError('Usuário deve ter pelo menos 13 anos')
        return v
    
    def calcular_idade(self) -> Optional[int]:
        """Retorna a idade do usuário em anos"""
        if not self.data_nascimento:
            return None
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        # Ajusta se ainda não fez aniversário este ano
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        return idade
    
    def adicionar_pontos(self, pontos: int) -> int:
        """Adiciona pontos ao usuário e retorna a nova pontuação"""
        self.pontuacao += pontos
        self.ultima_atualizacao = datetime.utcnow()
        return self.pontuacao
    
    def completar_cadastro(self, nome: str, email: str, data_nascimento: date):
        """Completa o cadastro do usuário"""
        self.nome = nome
        self.email = email
        self.data_nascimento = data_nascimento
        self.cadastro_completo = True
        self.ultima_atualizacao = datetime.utcnow()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }


class UsuarioCadastro(BaseModel):
    """Schema para cadastro de novo usuário"""
    vem_hash: str
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    data_nascimento: date


class UsuarioResposta(BaseModel):
    """Schema para resposta da API"""
    vem_hash: str
    nome: Optional[str]
    pontuacao: int
    cadastro_completo: bool
    idade: Optional[int] = None
    
    class Config:
        from_attributes = True