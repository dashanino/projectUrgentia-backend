from flask import jsonify, request
from app.services.lost_item_service import create_m1, getAll

def create():
    ## Obtiene la información de lo que envía el usuario en formato JSON
    data = request.get_json(silent=True) or {}

    item_type = data.get("item_type")
    campus_location = data.get("campus_location")
    found_location_description = data.get("found_location_description")
    item_description = data.get("item_description")
    delivered_by_name = data.get("delivered_by_name")
    delivered_by_area = data.get("delivered_by_area")
    photo_path = data.get("photo_path")        
    storage_location = data.get("storage_location")

    if not storage_location or not photo_path or not item_type or not campus_location or not found_location_description or not item_description or not delivered_by_name:
        return jsonify({
            "message": "storage_location, photo_path, item_type, campus_location, found_location_description, item_description and delivered_by_name are required"
        }), 400

    lost_item = create_m1(
        item_type=item_type,
        campus_location=campus_location,
        found_location_description=found_location_description,
        item_description=item_description,
        delivered_by_name=delivered_by_name,
        storage_location=storage_location,
        delivered_by_area=delivered_by_area,
        photo_path=photo_path
    )

    return jsonify({
        "id": lost_item.id,
        "item_type": lost_item.item_type,
        "campus_location": lost_item.campus_location,
        "found_location_description": lost_item.found_location_description,
        "item_description": lost_item.item_description,
        "delivered_by_name": lost_item.delivered_by_name,
        "delivered_by_area": lost_item.delivered_by_area,
        "photo_path": lost_item.photo_path,
        "storage_location": lost_item.storage_location
    }), 201

def listAll():
    lost_items = getAll()
    lost_items_list = []
    for item in lost_items:
        lost_items_list.append({
            "id": item.id,
            "item_type": item.item_type,
            "campus_location": item.campus_location,
            "found_location_description": item.found_location_description,
            "item_description": item.item_description,
            "delivered_by_name": item.delivered_by_name,
            "delivered_by_area": item.delivered_by_area,
            "photo_path": item.photo_path,
            "storage_location": item.storage_location
        })
    return jsonify(lost_items_list), 200