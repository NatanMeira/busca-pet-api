from marshmallow import Schema, fields, validate
from models.pet import Pet
from .endereco import EnderecoSchema


class PetSchema(Schema):
    
    id = fields.Integer(dump_only=True)
    tipo = fields.String(
        required=True,
        validate=validate.OneOf(Pet.TIPOS),
        error_messages={'required': 'Tipo é obrigatório'}
    )
    foto = fields.String(allow_none=True)
    nome = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Nome é obrigatório'}
    )
    idade = fields.String(
        required=True,
        validate=validate.OneOf(Pet.IDADES),
        error_messages={'required': 'Idade é obrigatória'}
    )
    porte = fields.String(
        required=True,
        validate=validate.OneOf(Pet.PORTES),
        error_messages={'required': 'Porte é obrigatório'}
    )
    raca = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Raça é obrigatória'}
    )
    info_contato = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={'required': 'Informações de contato são obrigatórias'}
    )
    sexo = fields.String(
        required=True,
        validate=validate.OneOf(Pet.SEXOS),
        error_messages={'required': 'Sexo é obrigatório'}
    )
    descricao = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={'required': 'Descrição é obrigatória'}
    )
    observacoes = fields.String(allow_none=True)
    data_desaparecimento = fields.DateTime(
        required=True,
        error_messages={'required': 'Data de desaparecimento é obrigatória'}
    )
    endereco_id = fields.Integer(load_only=True)
    endereco = fields.Nested(EnderecoSchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class PetCreateSchema(Schema):
    tipo = fields.String(
        required=True,
        validate=validate.OneOf(Pet.TIPOS),
        error_messages={'required': 'Tipo é obrigatório'}
    )
    foto = fields.String(allow_none=True)
    nome = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Nome é obrigatório'}
    )
    idade = fields.String(
        required=True,
        validate=validate.OneOf(Pet.IDADES),
        error_messages={'required': 'Idade é obrigatória'}
    )
    porte = fields.String(
        required=True,
        validate=validate.OneOf(Pet.PORTES),
        error_messages={'required': 'Porte é obrigatório'}
    )
    raca = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Raça é obrigatória'}
    )
    info_contato = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={'required': 'Informações de contato são obrigatórias'}
    )
    sexo = fields.String(
        required=True,
        validate=validate.OneOf(Pet.SEXOS),
        error_messages={'required': 'Sexo é obrigatório'}
    )
    descricao = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={'required': 'Descrição é obrigatória'}
    )
    observacoes = fields.String(allow_none=True)
    data_desaparecimento = fields.DateTime(
        required=True,
        error_messages={'required': 'Data de desaparecimento é obrigatória'}
    )
    endereco_desaparecimento = fields.Nested(
        EnderecoSchema,
        required=True,
        error_messages={'required': 'Endereço de desaparecimento é obrigatório'}
    )


class PetUpdateSchema(Schema):
    tipo = fields.String(
        validate=validate.OneOf(Pet.TIPOS),
        allow_none=True
    )
    foto = fields.String(allow_none=True)
    nome = fields.String(
        validate=validate.Length(min=1, max=100),
        allow_none=True
    )
    idade = fields.String(
        validate=validate.OneOf(Pet.IDADES),
        allow_none=True
    )
    porte = fields.String(
        validate=validate.OneOf(Pet.PORTES),
        allow_none=True
    )
    raca = fields.String(
        validate=validate.Length(min=1, max=100),
        allow_none=True
    )
    info_contato = fields.String(
        validate=validate.Length(min=1),
        allow_none=True
    )
    sexo = fields.String(
        validate=validate.OneOf(Pet.SEXOS),
        allow_none=True
    )
    descricao = fields.String(
        validate=validate.Length(min=1),
        allow_none=True
    )
    observacoes = fields.String(allow_none=True)
    data_desaparecimento = fields.DateTime(allow_none=True)
    endereco_id = fields.Integer(allow_none=True)
    endereco_desaparecimento = fields.Nested(
        EnderecoSchema,
        allow_none=True
    )


pet_schema = PetSchema()
pets_schema = PetSchema(many=True)
pet_create_schema = PetCreateSchema()
pet_update_schema = PetUpdateSchema()