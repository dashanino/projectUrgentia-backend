from flask import Flask
from app.routes.health_routes import health_bp
from app.routes.user_routes import user_bp
from app.routes.patient_routes import patient_bp
from app.routes.pretriage_routes import pretriage_bp
from app.routes.auth_routes import auth_bp
from app.routes.role_routes import role_bp
from app.routes.poblacion_routes import poblacion_bp
from app.routes.patient_antecedente_routes import patient_antecedente_bp
from app.routes.pretriage_agent_routes import pretriage_agent_bp
from config import Config
from app.extensions import db, migrate, jwt

def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app import models

    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(patient_bp, url_prefix='/api')
    app.register_blueprint(pretriage_bp, url_prefix='/api')

    app.register_blueprint(role_bp, url_prefix='/api')

    app.register_blueprint(poblacion_bp, url_prefix='/api')
    app.register_blueprint(patient_antecedente_bp, url_prefix='/api')
    app.register_blueprint(pretriage_agent_bp, url_prefix='/api')
    

    return app