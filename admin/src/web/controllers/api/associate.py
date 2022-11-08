from flask import Blueprint, jsonify
from src.web.helpers.build_response import response
from src.core.board import list_disciplines, get_associate_by_id
from datetime import datetime
from src.web.helpers.auth import jwt_required
from src.web.helpers.associate import is_up_to_date
from src.web.helpers.associate import generate_associate_card
import base64
import os

associate_api_blueprint = Blueprint(
    "associate_api", __name__, url_prefix=""
)


@associate_api_blueprint.get("/disciplines/<id>")
@jwt_required
def index_api(id):
    """Args:
        id (int): id of the associate
    Returns:
        JSON: list of disciplines
    """
    associate = get_associate_by_id(id)
    if associate.disciplines:
        # transform associates IntrumentedLIst into dict
        disciplines = [
            {
                "name": discipline.name,
                "days": discipline.dates,
                "time": discipline.dates,
                "teacher": discipline.instructors,
                "price": discipline.monthly_cost,
            }
            for discipline in associate.disciplines
        ]
        return response(200, disciplines)
    else:
        return response(200, [])
    

#make an api for the associate card
@associate_api_blueprint.get("/license/<id>") 
def associate_card_api(id):
    """Args:
        id (int): id of the associate
    Returns:
        JSON: associate card
    """
    associate = get_associate_by_id(id)
    if associate:
        CARD_PATH = os.path.join(os.getcwd(), "public", "associate_card.png")
        QR_PATH = os.path.join(os.getcwd(), "public", "qr.png")
        generate_associate_card(associate,CARD_PATH,associate.profile_pic,QR_PATH)
        
        with open(associate.profile_pic, "rb") as img_file:
                profile_pic_in64 = base64.b64encode(img_file.read())
        with open(CARD_PATH, "rb") as img_file:
                card_in64 = base64.b64encode(img_file.read())
        card_data={
            "name":associate.name,
            "surname":associate.surname,
            "dni":associate.DNI_number,
            "entry_date": f"{associate.entry_date.day}/{associate.entry_date.month}/{associate.entry_date.year}",
            "associate_number":associate.id,
            "status":"Al dia" if is_up_to_date(associate) else "Moroso",
            "profile_pic":str(profile_pic_in64),
            "associate_card":str(card_in64)        
        }
        return response(200,card_data)
    return response(200,[])
        