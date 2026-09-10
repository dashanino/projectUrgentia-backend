from flask import Blueprint
from app.controllers.lost_item_controller import (
    create,
    getAll
    )

lost_item_bp = Blueprint('lost_item', __name__)

@lost_item_bp.route('/lost_items', methods=['POST'])
def create_lost_item():
    return create()

@lost_item_bp.route('/lost_items', methods=['GET'])
def list_all_lost_items():
    return getAll()
