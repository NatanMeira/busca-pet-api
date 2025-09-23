#!/usr/bin/env python3

import os
from flask import Flask
from flask_cors import CORS
from db import init_db
from controllers import pet_bp
from logger import get_logger

logger = get_logger(__name__)

def create_app(config_name='default'):
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///pets.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'
    app.config['RESTX_MASK_SWAGGER'] = False
    
    CORS(app)
    init_db(app)
    
    app.register_blueprint(pet_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )
