
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required


class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} #SELECT*FROM hoteis

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="O campo nome não pode ser branco")
    atributos.add_argument('estrelas')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel não encontrado.'}, 404 #código do not found

    @jwt_required #toda alteração feita, precisa estar logado
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message":"Esse hotel id '{}' já existe.".format(hotel_id)}, 400 #Bad RequestParser

        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id,**dados)
        try:
            hotel.save_hotel()
        except:
            return{'message':'Erro interno, tente novamente'}, 500 #erro interno do servidor
        return hotel.json(),201

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        hotel_encontrado= Hotel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json, 200
        hotel.save_hotel()
        return hotel.json(), 201 #hotel criado

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
                hotel.delete_hotel()
                return{'message':'Hotel deletado.'}

        return{'message':'Hotel não encontrado.'},404

        #global hoteis #para não dar erro de referência
        #hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        #return {'message':'Hotel deletado.'}
