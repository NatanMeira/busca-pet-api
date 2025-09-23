from .base import BaseModel
from db import db


class Endereco(BaseModel):
    __tablename__ = 'enderecos'
    
    cep = db.Column(db.String(10), nullable=False)
    rua = db.Column(db.String(255), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(100), nullable=False, default='Brasil')
    
    def __repr__(self):
        return f'<Endereco {self.rua}, {self.cidade}>'