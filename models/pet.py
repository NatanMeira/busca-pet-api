from .base import BaseModel
from .endereco import Endereco
from db import db


class Pet(BaseModel):
    __tablename__ = 'pets'
    
    TIPOS = ['Cachorro', 'Gato', 'Ave', 'Outro']
    IDADES = ['Filhote', 'Adulto', 'Idoso']
    PORTES = ['Pequeno', 'Medio', 'Grande']
    SEXOS = ['Macho', 'Femea']
    
    tipo = db.Column(db.Enum(*TIPOS, name='pet_tipo'), nullable=False)
    foto = db.Column(db.Text, nullable=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Enum(*IDADES, name='pet_idade'), nullable=False)
    porte = db.Column(db.Enum(*PORTES, name='pet_porte'), nullable=False)
    raca = db.Column(db.String(100), nullable=False)
    info_contato = db.Column(db.Text, nullable=False)
    sexo = db.Column(db.Enum(*SEXOS, name='pet_sexo'), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    data_desaparecimento = db.Column(db.DateTime, nullable=False)
    
    endereco_id = db.Column(db.Integer, db.ForeignKey('enderecos.id'), nullable=False)
    endereco = db.relationship('Endereco', backref='pets', lazy=True)
    
    def __repr__(self):
        return f'<Pet {self.nome} - {self.tipo}>'