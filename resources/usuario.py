from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="O campo 'login' não pode ser branco ")
atributos.add_argument('senha', type=str, required=True, help="O campo 'login' não pode ser branco ")


class User(Resource):
    #Referente a /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Usuário não encontrado.'}, 404 #código do not found

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
                user.delete_user()
                return{'message':'Ocorreu um erro ao deletar o usuário.'}
        return{'message':'Usuário não encontrado.'},404


class UserRegister(Resource):
    def post(self):

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message':"O login '{}' já existe.".format(dados['login'])}
        user = UserModel(**dados)
        user.save_user()
        return{'message':'Usuário criado com sucesso!'}, 201 #criado

class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']): #comparação segura
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message':'O usuário ou senha está incorreto.'}, 401 #Não autorizado
        #instala pip install Flask-JWT-Extended

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #identificador token JWT
        BLACKLIST.add(jwt_id)
        return{'message':'Logout realizado com sucesso'},200
