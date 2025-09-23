from flask_restx import fields
from datetime import datetime

def create_swagger_models(api):
    endereco_model = api.model('Endereco', {
        'id': fields.Integer(readonly=True, description='ID único do endereço'),
        'cep': fields.String(required=True, description='CEP', example='01234567'),
        'rua': fields.String(required=True, description='Rua e número', example='Rua das Flores, 123'),
        'bairro': fields.String(required=True, description='Bairro', example='Centro'),
        'cidade': fields.String(required=True, description='Cidade', example='São Paulo'),
        'estado': fields.String(required=True, description='Estado', example='SP'),
        'pais': fields.String(description='País', example='Brasil', default='Brasil'),
        'created_at': fields.DateTime(readonly=True, description='Data de criação'),
        'updated_at': fields.DateTime(readonly=True, description='Data de atualização')
    })
    
    endereco_input_model = api.model('EnderecoInput', {
        'cep': fields.String(required=True, description='CEP', example='01234567'),
        'rua': fields.String(required=True, description='Rua e número', example='Rua das Flores, 123'),
        'bairro': fields.String(required=True, description='Bairro', example='Centro'),
        'cidade': fields.String(required=True, description='Cidade', example='São Paulo'),
        'estado': fields.String(required=True, description='Estado', example='SP'),
        'pais': fields.String(description='País', example='Brasil', default='Brasil')
    })
    
    pet_model = api.model('Pet', {
        'id': fields.Integer(readonly=True, description='ID único do pet'),
        'tipo': fields.String(required=True, description='Tipo do pet', 
                             enum=['Cachorro', 'Gato', 'Ave', 'Outro'], example='Cachorro'),
        'foto': fields.String(description='URL da foto ou base64', example='https://placehold.co/220x220?text=Pré-visualização'),
        'nome': fields.String(required=True, description='Nome do pet', example='Rex'),
        'idade': fields.String(required=True, description='Idade do pet',
                              enum=['Filhote', 'Adulto', 'Idoso'], example='Adulto'),
        'porte': fields.String(required=True, description='Porte do pet',
                              enum=['Pequeno', 'Medio', 'Grande'], example='Grande'),
        'raca': fields.String(required=True, description='Raça do pet', example='Pastor Alemão'),
        'info_contato': fields.String(required=True, description='Informações de contato', 
                                     example='João Silva - (11) 99999-9999'),
        'sexo': fields.String(required=True, description='Sexo do pet',
                             enum=['Macho', 'Femea'], example='Macho'),
        'descricao': fields.String(required=True, description='Descrição do pet', 
                                  example='Cachorro muito dócil, pelagem marrom'),
        'observacoes': fields.String(description='Observações adicionais', 
                                    example='Tem uma cicatriz na pata esquerda'),
        'data_desaparecimento': fields.DateTime(required=True, description='Data do desaparecimento',
                                               example='2024-01-15T10:30:00'),
        'endereco_id': fields.Integer(description='ID do endereço de desaparecimento'),
        'endereco': fields.Nested(endereco_model, description='Endereço onde o pet desapareceu'),
        'created_at': fields.DateTime(readonly=True, description='Data de criação'),
        'updated_at': fields.DateTime(readonly=True, description='Data de atualização')
    })
    
    pet_create_model = api.model('PetCreate', {
        'tipo': fields.String(required=True, description='Tipo do pet',
                             enum=['Cachorro', 'Gato', 'Ave', 'Outro'], example='Cachorro'),
        'foto': fields.String(description='URL da foto ou base64', example='https://placehold.co/220x220?text=Pré-visualização'),
        'nome': fields.String(required=True, description='Nome do pet', example='Rex'),
        'idade': fields.String(required=True, description='Idade do pet',
                              enum=['Filhote', 'Adulto', 'Idoso'], example='Adulto'),
        'porte': fields.String(required=True, description='Porte do pet',
                              enum=['Pequeno', 'Medio', 'Grande'], example='Grande'),
        'raca': fields.String(required=True, description='Raça do pet', example='Pastor Alemão'),
        'info_contato': fields.String(required=True, description='Informações de contato',
                                     example='João Silva - (11) 99999-9999'),
        'sexo': fields.String(required=True, description='Sexo do pet',
                             enum=['Macho', 'Femea'], example='Macho'),
        'descricao': fields.String(required=True, description='Descrição do pet',
                                  example='Cachorro muito dócil, pelagem marrom'),
        'observacoes': fields.String(description='Observações adicionais',
                                    example='Tem uma cicatriz na pata esquerda'),
        'data_desaparecimento': fields.DateTime(required=True, description='Data do desaparecimento',
                                               example='2024-01-15T10:30:00'),
        'endereco_desaparecimento': fields.Nested(endereco_input_model, required=True,
                                                  description='Endereço onde o pet desapareceu')
    })
    
    pet_update_model = api.model('PetUpdate', {
        'tipo': fields.String(description='Tipo do pet', enum=['Cachorro', 'Gato', 'Ave', 'Outro']),
        'foto': fields.String(description='URL da foto ou base64'),
        'nome': fields.String(description='Nome do pet'),
        'idade': fields.String(description='Idade do pet', enum=['Filhote', 'Adulto', 'Idoso']),
        'porte': fields.String(description='Porte do pet', enum=['Pequeno', 'Medio', 'Grande']),
        'raca': fields.String(description='Raça do pet'),
        'info_contato': fields.String(description='Informações de contato'),
        'sexo': fields.String(description='Sexo do pet', enum=['Macho', 'Femea']),
        'descricao': fields.String(description='Descrição do pet'),
        'observacoes': fields.String(description='Observações adicionais'),
        'data_desaparecimento': fields.DateTime(description='Data do desaparecimento'),
        'endereco_id': fields.Integer(description='ID do endereço de desaparecimento'),
        'endereco_desaparecimento': fields.Nested(endereco_input_model, 
                                                  description='Endereço onde o pet desapareceu (atualiza ou cria novo)')
    })
    
    success_response_model = api.model('SuccessResponse', {
        'message': fields.String(description='Mensagem de sucesso'),
        'data': fields.Raw(description='Dados retornados')
    })
    
    error_response_model = api.model('ErrorResponse', {
        'message': fields.String(description='Mensagem de erro'),
        'errors': fields.Raw(description='Detalhes dos erros')
    })
    
    pet_types_model = api.model('PetTypes', {
        'tipos': fields.List(fields.String, description='Tipos de pets disponíveis'),
        'idades': fields.List(fields.String, description='Idades disponíveis'),
        'portes': fields.List(fields.String, description='Portes disponíveis'),
        'sexos': fields.List(fields.String, description='Sexos disponíveis')
    })
    
    pagination_model = api.model('Pagination', {
        'page_number': fields.Integer(description='Número da página atual', example=1),
        'page_size': fields.Integer(description='Tamanho da página', example=20),
        'total_count': fields.Integer(description='Total de registros', example=150),
        'total_pages': fields.Integer(description='Total de páginas', example=8),
        'has_next': fields.Boolean(description='Indica se há próxima página', example=True),
        'has_prev': fields.Boolean(description='Indica se há página anterior', example=False)
    })
    
    paginated_response_model = api.model('PaginatedResponse', {
        'message': fields.String(description='Mensagem de sucesso'),
        'data': fields.List(fields.Nested(pet_model), description='Lista de pets'),
        'pagination': fields.Nested(pagination_model, description='Informações de paginação')
    })
    
    return {
        'endereco': endereco_model,
        'endereco_input': endereco_input_model,
        'pet': pet_model,
        'pet_create': pet_create_model,
        'pet_update': pet_update_model,
        'success_response': success_response_model,
        'error_response': error_response_model,
        'pet_types': pet_types_model,
        'pagination': pagination_model,
        'paginated_response': paginated_response_model
    }
