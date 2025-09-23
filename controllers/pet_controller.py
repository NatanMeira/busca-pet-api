from flask import Blueprint, request
from flask_restx import Api, Resource, Namespace
from marshmallow import ValidationError
from datetime import datetime
from services import PetService
from schemas import pet_schema, pets_schema, pet_create_schema, pet_update_schema
from swagger_models import create_swagger_models
from logger import get_logger

logger = get_logger(__name__)

pet_bp = Blueprint('pets', __name__, url_prefix='/api')

api = Api(
    pet_bp,
    title='Busca Pet API',
    version='1.0.0',
    description='API para gerenciar pets perdidos',
    doc='/docs/'
)

pets_ns = Namespace('Pets', description='Operações relacionadas a pets perdidos', path='/pets')
api.add_namespace(pets_ns)

models = create_swagger_models(api)


@pets_ns.route('')
class PetListResource(Resource):
    @pets_ns.doc('get_all_pets')
    @pets_ns.marshal_with(models['paginated_response'])
    @pets_ns.param('nome', 'Filtrar por nome do pet')
    @pets_ns.param('tipo', 'Filtrar por tipo do pet')
    @pets_ns.param('cidade', 'Filtrar por cidade onde desapareceu')
    @pets_ns.param('start_date', 'Data inicial para filtro (ISO format)')
    @pets_ns.param('end_date', 'Data final para filtro (ISO format)')
    @pets_ns.param('page_number', 'Número da página (padrão: 1)', type='integer')
    @pets_ns.param('page_size', 'Tamanho da página (padrão: 20, máximo: 100)', type='integer')
    def get(self):
        try:
            nome = request.args.get('nome')
            tipo = request.args.get('tipo')
            cidade = request.args.get('cidade')
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            page_number = int(request.args.get('page_number', 1))
            page_size = int(request.args.get('page_size', 20))
            
            if page_number < 1:
                page_number = 1
            if page_size < 1 or page_size > 100:
                page_size = 20
            
            filters = {}
            if nome:
                filters['nome'] = nome
            if tipo:
                filters['tipo'] = tipo
            if cidade:
                filters['cidade'] = cidade
            if start_date and end_date:
                filters['start_date'] = datetime.fromisoformat(start_date)
                filters['end_date'] = datetime.fromisoformat(end_date)
            
            pets, total_count = PetService.search_pets_with_filters(filters, page_number, page_size)
            
            result = pets_schema.dump(pets)
            
            total_pages = (total_count + page_size - 1) // page_size
            has_next = page_number < total_pages
            has_prev = page_number > 1
            
            return {
                'message': f'{len(pets)} pets encontrados (página {page_number} de {total_pages})',
                'data': result,
                'pagination': {
                    'page_number': page_number,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': total_pages,
                    'has_next': has_next,
                    'has_prev': has_prev
                }
            }, 200
            
        except ValueError as e:
            logger.warning(f"Value error getting pets: {str(e)}")
            return {
                'message': 'Parâmetros de consulta inválidos'
            }, 400
            
        except Exception as e:
            logger.error(f"Unexpected error getting pets: {str(e)}")
            return {
                'message': 'Erro interno do servidor'
            }, 500
    
    @pets_ns.doc('create_pet')
    @pets_ns.expect(models['pet_create'])
    @pets_ns.marshal_with(models['success_response'], code=201)
    @pets_ns.response(400, 'Dados inválidos', models['error_response'])
    @pets_ns.response(500, 'Erro interno do servidor', models['error_response'])
    def post(self):
        try:
            data = pet_create_schema.load(request.json)
            
            pet = PetService.create_pet_with_endereco(data)
            
            result = pet_schema.dump(pet)
            logger.info(f"Pet created successfully with ID: {pet.id}")
            
            return {
                'message': 'Pet criado com sucesso',
                'data': result
            }, 201
            
        except ValidationError as e:
            logger.warning(f"Validation error creating pet: {e.messages}")
            return {
                'message': 'Dados inválidos',
                'errors': e.messages
            }, 400
            
        except ValueError as e:
            logger.warning(f"Value error creating pet: {str(e)}")
            return {
                'message': str(e)
            }, 400
            
        except Exception as e:
            logger.error(f"Unexpected error creating pet: {str(e)}")
            return {
                'message': 'Erro interno do servidor'
            }, 500


@pets_ns.route('/<int:pet_id>')
class PetResource(Resource):
    @pets_ns.doc('get_pet_by_id')
    @pets_ns.marshal_with(models['success_response'])
    @pets_ns.response(404, 'Pet não encontrado', models['error_response'])
    @pets_ns.response(500, 'Erro interno do servidor', models['error_response'])
    def get(self, pet_id):
        try:
            pet = PetService.get_pet_by_id(pet_id)
            
            if not pet:
                return {
                    'message': 'Pet não encontrado'
                }, 404
            
            result = pet_schema.dump(pet)
            
            return {
                'message': 'Pet encontrado',
                'data': result
            }, 200
            
        except Exception as e:
            logger.error(f"Unexpected error getting pet {pet_id}: {str(e)}")
            return {
                'message': 'Erro interno do servidor'
            }, 500
    
    @pets_ns.doc('update_pet')
    @pets_ns.expect(models['pet_update'])
    @pets_ns.marshal_with(models['success_response'])
    @pets_ns.response(400, 'Dados inválidos', models['error_response'])
    @pets_ns.response(404, 'Pet não encontrado', models['error_response'])
    @pets_ns.response(500, 'Erro interno do servidor', models['error_response'])
    def put(self, pet_id):
        try:
            data = pet_update_schema.load(request.json, partial=True)
            
            pet = PetService.update_pet_with_endereco(pet_id, data)
            
            if not pet:
                return {
                    'message': 'Pet não encontrado'
                }, 404
            
            result = pet_schema.dump(pet)
            
            return {
                'message': 'Pet atualizado com sucesso',
                'data': result
            }, 200
            
        except ValidationError as e:
            logger.warning(f"Validation error updating pet {pet_id}: {e.messages}")
            return {
                'message': 'Dados inválidos',
                'errors': e.messages
            }, 400
            
        except ValueError as e:
            logger.warning(f"Value error updating pet {pet_id}: {str(e)}")
            return {
                'message': str(e)
            }, 400
            
        except Exception as e:
            logger.error(f"Unexpected error updating pet {pet_id}: {str(e)}")
            return {
                'message': 'Erro interno do servidor'
            }, 500
    
    @pets_ns.doc('delete_pet')
    @pets_ns.marshal_with(models['success_response'])
    @pets_ns.response(404, 'Pet não encontrado', models['error_response'])
    @pets_ns.response(500, 'Erro interno do servidor', models['error_response'])
    def delete(self, pet_id):
        try:
            success = PetService.delete_pet(pet_id)
            
            if not success:
                return {
                    'message': 'Pet não encontrado'
                }, 404
            
            return {
                'message': 'Pet deletado com sucesso'
            }, 200
            
        except Exception as e:
            logger.error(f"Unexpected error deleting pet {pet_id}: {str(e)}")
            return {
                'message': 'Erro interno do servidor'
            }, 500