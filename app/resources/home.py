from flask import jsonify, Blueprint
from app.mapping.response_schema import ResponseSchema
from app.services.response_message import ResponseBuilder

home = Blueprint('home', __name__)

response_schema = ResponseSchema()

@home.route('/', methods=['GET'])
def index():
    # Construir la respuesta usando ResponseBuilder
    response_builder = ResponseBuilder()
    response_builder.add_message("Bienvenidos").add_status_code(200).add_data({'title': 'API Auth'})
    response = response_builder.build()
    
    # Serializar la respuesta usando ResponseSchema y devolverla como JSON
    json_response = response_schema.dump(response)
    
    return jsonify(json_response), 200