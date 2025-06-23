from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
cache = Cache()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URL')
    app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = False
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_URL'] = os.getenv('CACHE_REDIS_URL')
    app.config['CACHE_REDIS_PORT'] = os.getenv('CACHE_REDIS_PORT')
    app.config['CACHE_DEFAULT_TIMEOUT'] = os.getenv('CACHE_DEFAULT_TIMEOUT')
    db.init_app(app)
    cache.init_app(app)
    from app.routes import sentiment_bp
    app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')
    return app
