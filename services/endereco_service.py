from typing import List, Optional
from models import Endereco
from db import db
from logger import get_logger

logger = get_logger(__name__)


class EnderecoService:
    
    @staticmethod
    def create_endereco(endereco_data: dict) -> Endereco:
        try:
            endereco = Endereco(**endereco_data)
            endereco.save()
            logger.info(f"Endereco created with ID: {endereco.id}")
            return endereco
        except Exception as e:
            logger.error(f"Error creating endereco: {str(e)}")
            db.session.rollback()
            raise
    
    @staticmethod
    def get_endereco_by_id(endereco_id: int) -> Optional[Endereco]:
        try:
            endereco = Endereco.query.get(endereco_id)
            if endereco:
                logger.info(f"Endereco found with ID: {endereco_id}")
            else:
                logger.warning(f"Endereco not found with ID: {endereco_id}")
            return endereco
        except Exception as e:
            logger.error(f"Error getting endereco by ID {endereco_id}: {str(e)}")
            raise
    
    @staticmethod
    def update_endereco(endereco_id: int, endereco_data: dict) -> Optional[Endereco]:
        try:
            endereco = Endereco.query.get(endereco_id)
            if not endereco:
                logger.warning(f"Endereco not found for update with ID: {endereco_id}")
                return None
            
            for key, value in endereco_data.items():
                if hasattr(endereco, key):
                    setattr(endereco, key, value)
            
            endereco.save()
            logger.info(f"Endereco updated with ID: {endereco_id}")
            return endereco
        except Exception as e:
            logger.error(f"Error updating endereco {endereco_id}: {str(e)}")
            db.session.rollback()
            raise

    @staticmethod
    def delete_endereco(endereco_id: int) -> bool:
        try:
            endereco = Endereco.query.get(endereco_id)
            if not endereco:
                logger.warning(f"Endereco not found for deletion with ID: {endereco_id}")
                return False
            
            endereco.delete()
            logger.info(f"Endereco deleted with ID: {endereco_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting endereco {endereco_id}: {str(e)}")
            db.session.rollback()
            raise
    
