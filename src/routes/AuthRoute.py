import bcrypt
import hashlib
from flask import Blueprint, jsonify, request
from src.models.entities.auth import Login, SignUp
from src.models.AuthModel import AuthModel
from src.utils.Security import Security
          
main = Blueprint('auth_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hash_password(password):
    # Generar un salt aleatorio y hashear la contraseña con el salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password, hash_password):
    # Verifica si la contraseña en texto plano coincide con la contraseña encriptada
    return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))

@main.route('/login', methods = ['POST'])
def login():
    email = request.json['email']
    pre_password = request.json['password']
    password = hash_password(pre_password)
    login = Login(email, password)
    authenticated_user = AuthModel.login(login)
    if authenticated_user != None and verify_password(pre_password, authenticated_user.password):
        print(authenticated_user.name)
        encoded_token = Security.generate_token(authenticated_user)
        return jsonify({
            'profile_id': authenticated_user.id,
            'email': authenticated_user.email,
            'token': encoded_token
            }), 200
    else:
        response = jsonify({'message': 'No registrado'})
        return response, 401
    
    
@main.route('/signup', methods = ['POST'])
def sign_up():
    try:
        email = request.json['email']
        pre_password = request.json['password']
        password = hash_password(pre_password)
        name = request.json['name']
        
        profile_id = hashlib.shake_256(email.encode('utf-8')).hexdigest(16)
        
        signup = SignUp(profile_id,email,password,name)
        affected_row = AuthModel.signup(signup)

        if affected_row == 1:
            return jsonify({
                'message': 'OK',
                'user': email,
                'profile_id': profile_id
            })
        else:
            response = jsonify({'message': 'Error al registrarse'})
            return response
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500