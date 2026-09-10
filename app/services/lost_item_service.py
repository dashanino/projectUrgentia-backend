from sqlalchemy import select
from app.extensions import db

from app.models.lost_item import LostItem

def create_m1(item_type, campus_location, found_location_description, item_description, 
           delivered_by_name, storage_location, delivered_by_area=None, photo_path=None):

    campus_location = convertLowerCase(campus_location)
    lost_item = LostItem(
        item_type=item_type,
        campus_location=campus_location,
        found_location_description=found_location_description,
        item_description=item_description,
        delivered_by_name=delivered_by_name,
        delivered_by_area=delivered_by_area,
        photo_path=photo_path,
        storage_location=storage_location
    )

    db.session.add(lost_item)
    db.session.commit()

    return lost_item

def getAll():
    lost_items = db.session.execute(
        select(LostItem)
    ).scalars().all()
    return lost_items

def convertLowerCase(campus_location):
    if campus_location:
        return campus_location.lower()
    return campus_location