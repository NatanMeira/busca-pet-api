from typing import List, Optional
from datetime import datetime
from models import Pet, Endereco
from services import EnderecoService
from db import db
from logger import get_logger

logger = get_logger(__name__)


class PetService:
    
    @staticmethod
    def create_pet_with_endereco(pet_data: dict) -> Pet:
        try:
            endereco_data = pet_data.pop('endereco_desaparecimento', None)
            if not endereco_data:
                raise ValueError("Endereço de desaparecimento é obrigatório")
            
            endereco = EnderecoService.create_endereco(endereco_data)
            
            pet_data['endereco_id'] = endereco.id
            pet = Pet(**pet_data)
            pet.save()
            
            logger.info(f"Pet created with ID: {pet.id} and endereco ID: {endereco.id}")
            return pet
        except Exception as e:
            logger.error(f"Error creating pet with endereco: {str(e)}")
            db.session.rollback()
            raise
    
    @staticmethod
    def get_pet_by_id(pet_id: int) -> Optional[Pet]:
        try:
            pet = Pet.query.options(db.joinedload(Pet.endereco)).get(pet_id)
            if pet:
                logger.info(f"Pet found with ID: {pet_id}")
            else:
                logger.warning(f"Pet not found with ID: {pet_id}")
            return pet
        except Exception as e:
            logger.error(f"Error getting pet by ID {pet_id}: {str(e)}")
            raise
    
    @staticmethod
    def get_all_pets(page_number: int = 1, page_size: int = 20) -> tuple[List[Pet], int]:
        try:
            total_count = Pet.query.count()
            
            offset = (page_number - 1) * page_size
            pets = Pet.query.options(db.joinedload(Pet.endereco)).order_by(Pet.created_at.desc()).offset(offset).limit(page_size).all()
            
            logger.info(f"Retrieved {len(pets)} pets (page {page_number}, total: {total_count})")
            return pets, total_count
        except Exception as e:
            logger.error(f"Error getting all pets: {str(e)}")
            raise
    
    @staticmethod
    def search_pets_with_filters(filters: dict, page_number: int = 1, page_size: int = 20) -> tuple[List[Pet], int]:
        try:
            base_query = Pet.query.options(db.joinedload(Pet.endereco))
            
            if 'nome' in filters:
                base_query = base_query.filter(Pet.nome.ilike(f'%{filters["nome"]}%'))
            
            if 'tipo' in filters:
                base_query = base_query.filter(Pet.tipo == filters['tipo'])
            
            if 'cidade' in filters:
                base_query = base_query.join(Endereco).filter(
                    Endereco.cidade.ilike(f'%{filters["cidade"]}%')
                )
            
            if 'start_date' in filters and 'end_date' in filters:
                base_query = base_query.filter(
                    Pet.data_desaparecimento.between(filters['start_date'], filters['end_date'])
                )
            
            base_query = base_query.order_by(Pet.created_at.desc())
            
            total_count = base_query.count()
            
            offset = (page_number - 1) * page_size
            pets = base_query.offset(offset).limit(page_size).all()
            
            filter_description = []
            if 'nome' in filters:
                filter_description.append(f"nome: {filters['nome']}")
            if 'tipo' in filters:
                filter_description.append(f"tipo: {filters['tipo']}")
            if 'cidade' in filters:
                filter_description.append(f"cidade: {filters['cidade']}")
            if 'start_date' in filters and 'end_date' in filters:
                filter_description.append(f"data: {filters['start_date']} - {filters['end_date']}")
            
            filter_str = ", ".join(filter_description) if filter_description else "sem filtros"
            logger.info(f"Found {len(pets)} pets with filters ({filter_str}) (page {page_number}, total: {total_count})")
            return pets, total_count
        except Exception as e:
            logger.error(f"Error searching pets with filters: {str(e)}")
            raise

    @staticmethod
    def update_pet_with_endereco(pet_id: int, pet_data: dict) -> Optional[Pet]:
        try:
            pet = Pet.query.get(pet_id)
            if not pet:
                logger.warning(f"Pet not found for update with ID: {pet_id}")
                return None
            
            endereco_data = pet_data.pop('endereco_desaparecimento', None)
            if endereco_data:
                if pet.endereco_id:
                    updated_endereco = EnderecoService.update_endereco(pet.endereco_id, endereco_data)
                    if not updated_endereco:
                        endereco = EnderecoService.create_endereco(endereco_data)
                        pet_data['endereco_id'] = endereco.id
                else:
                    endereco = EnderecoService.create_endereco(endereco_data)
                    pet_data['endereco_id'] = endereco.id
            
            if 'endereco_id' in pet_data:
                endereco = EnderecoService.get_endereco_by_id(pet_data['endereco_id'])
                if not endereco:
                    raise ValueError(f"Endereço não encontrado com ID: {pet_data['endereco_id']}")
            
            for key, value in pet_data.items():
                if hasattr(pet, key) and value is not None:
                    setattr(pet, key, value)
            
            pet.save()
            logger.info(f"Pet updated with endereco with ID: {pet_id}")
            return pet
        except Exception as e:
            logger.error(f"Error updating pet with endereco {pet_id}: {str(e)}")
            db.session.rollback()
            raise
    
    @staticmethod
    def delete_pet(pet_id: int) -> bool:
        try:
            pet = Pet.query.get(pet_id)
            if not pet:
                logger.warning(f"Pet not found for deletion with ID: {pet_id}")
                return False
            
            pet.delete()
            EnderecoService.delete_endereco(pet.endereco_id)
            logger.info(f"Pet deleted with ID: {pet_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting pet {pet_id}: {str(e)}")
            db.session.rollback()
            raise