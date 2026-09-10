from flask import Flask
from app.routes.health_routes import health_bp
from config import Config
from app.extensions import db, migrate, jwt
from app.routes.lost_item_routes import lost_item_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app import models

    app.register_blueprint(
        health_bp,
        url_prefix='/api'
    )

    app.register_blueprint(
            lost_item_bp,
            url_prefix='/api'
        )
    return app