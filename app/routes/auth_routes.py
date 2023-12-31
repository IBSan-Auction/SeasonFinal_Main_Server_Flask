from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from ..config.Config import api
from ..services.user_service import UsersService
from ..services.auth_service import AuthService
from ..models.ApiModel import Login_fields

def auth_routes(auth_ns):
    @auth_ns.route('/')
    class Login(Resource):
        @api.expect(Login_fields)
        @auth_ns.doc(description = '로그인 하는 route',)  
        def post(self):
            data = api.payload
            id = data['id']
            password = data['password']

            user = UsersService.get_user_by_id(id)
            if user and user.password == password:
                access_token = create_access_token(identity=id)
                refresh_token = create_refresh_token(identity=id)
                AuthService.set_refreshtoken(refreshtoken=refresh_token,id=id)
                response =  {
                    'message': 'Logged in successfully',
                    'name' : user.name,
                    'nickname' : user.nickname
                },
                # header를 태운다.
                response_headers = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                }
                return response, 200, response_headers
            return {'message': 'Invalid credentials'}, 401
        
        @jwt_required(refresh=True)
        @auth_ns.doc(security = 'Bearer', description = 'ACCESS_TOKEN을 발급 받기 위함.',)  
        def get(self):
            current_user = get_jwt_identity()
            new_access_token = create_access_token(identity=current_user)
            return {'access_token': new_access_token}, 200