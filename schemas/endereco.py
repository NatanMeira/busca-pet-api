from marshmallow import Schema, fields, validate, post_load
from models.endereco import Endereco


class EnderecoSchema(Schema):
    id = fields.Integer(dump_only=True)
    cep = fields.String(
        required=True,
        validate=validate.Length(min=8, max=10),
        error_messages={'required': 'CEP é obrigatório'}
    )
    rua = fields.String(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={'required': 'Rua é obrigatória'}
    )
    bairro = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Bairro é obrigatório'}
    )
    cidade = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Cidade é obrigatória'}
    )
    estado = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Estado é obrigatório'}
    )
    pais = fields.String(
        missing='Brasil',
        validate=validate.Length(min=1, max=100)
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


endereco_schema = EnderecoSchema()
enderecos_schema = EnderecoSchema(many=True)