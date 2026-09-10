from flask import jsonify
from app.services.health_service import (
    get_health_status, 
    get_health,
    db_status
    )
def db_status_controller():
    try:
        data = db_status()
        return jsonify(data), 200
    except Exception:
        return jsonify({
            "status": "error query status database"
        }), 500

def health():    
    data = get_health()
    return jsonify(data), 200

def health_status_controller():
    data = get_health_status()
    return jsonify(data), 201
