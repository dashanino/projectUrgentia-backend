
from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db, migrate, jwt

from app.routes.health_routes import health_bp
from app.routes.user_routes import user_bp
from app.routes.patient_routes import patient_bp
from app.routes.pretriage_routes import pretriage_bp
from app.routes.auth_routes import auth_bp
from app.routes.role_routes import role_bp
from app.routes.poblacion_routes import poblacion_bp
from app.routes.patient_antecedente_routes import patient_antecedente_bp
from app.routes.pretriage_agent_routes import pretriage_agent_bp
from app.routes.sintoma_routes import sintoma_bp
from app.routes.tramite_routes import tramite_bp
from app.routes.institution_routes import institution_bp
from app.routes.location_routes import location_bp


def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.config.from_object(Config)

    # Permitir conexiones desde Angular
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:4200",
                    "http://localhost:4201",
                    "http://localhost:59289",
                    "http://127.0.0.1:4200",
                    "http://127.0.0.1:4201",
                ]
            }
        },
        allow_headers=["Content-Type", "Authorization"],
    )

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app import models

    # Registrar rutas
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(patient_bp, url_prefix='/api')
    app.register_blueprint(pretriage_bp, url_prefix='/api')
    app.register_blueprint(role_bp, url_prefix='/api')
    app.register_blueprint(poblacion_bp, url_prefix='/api')
    app.register_blueprint(patient_antecedente_bp, url_prefix='/api')
    app.register_blueprint(pretriage_agent_bp, url_prefix='/api')
    app.register_blueprint(sintoma_bp, url_prefix='/api')
    app.register_blueprint(tramite_bp)
    app.register_blueprint(institution_bp, url_prefix='/api')
    app.register_blueprint(location_bp, url_prefix='/api')

    return app
