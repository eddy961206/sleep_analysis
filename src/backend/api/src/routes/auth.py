from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

# Blueprint 정의
auth_bp = Blueprint('auth', __name__)

# 샘플 사용자 데이터 - 실제 구현에서는 데이터베이스에서 관리
users = {
    "test@example.com": {
        "password": generate_password_hash("password123"),
        "name": "테스트 사용자"
    }
}

# JWT 시크릿 키 - 실제 구현에서는 환경 변수로 관리
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev_secret_key')

# 로그인 API 엔드포인트
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    사용자 로그인 API 엔드포인트
    
    Request Body:
        email (str): 사용자 이메일
        password (str): 사용자 비밀번호
    
    Returns:
        JSON: 로그인 결과 및 JWT 토큰
    """
    data = request.json
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({
            "success": False,
            "message": "이메일과 비밀번호를 모두 입력해주세요."
        }), 400
    
    email = data.get('email')
    password = data.get('password')
    
    # 사용자 확인
    user = users.get(email)
    
    if not user or not check_password_hash(user['password'], password):
        return jsonify({
            "success": False,
            "message": "이메일 또는 비밀번호가 올바르지 않습니다."
        }), 401
    
    # JWT 토큰 생성
    token = jwt.encode({
        'email': email,
        'name': user['name'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({
        "success": True,
        "message": "로그인 성공",
        "token": token,
        "user": {
            "email": email,
            "name": user['name']
        }
    })

# 회원가입 API 엔드포인트
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    사용자 회원가입 API 엔드포인트
    
    Request Body:
        email (str): 사용자 이메일
        password (str): 사용자 비밀번호
        name (str): 사용자 이름
    
    Returns:
        JSON: 회원가입 결과
    """
    data = request.json
    
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({
            "success": False,
            "message": "이메일, 비밀번호, 이름을 모두 입력해주세요."
        }), 400
    
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    # 이메일 중복 확인
    if email in users:
        return jsonify({
            "success": False,
            "message": "이미 등록된 이메일입니다."
        }), 400
    
    # 사용자 등록
    users[email] = {
        "password": generate_password_hash(password),
        "name": name
    }
    
    return jsonify({
        "success": True,
        "message": "회원가입이 완료되었습니다.",
        "user": {
            "email": email,
            "name": name
        }
    })

# 토큰 검증 API 엔드포인트
@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """
    JWT 토큰 검증 API 엔드포인트
    
    Headers:
        Authorization (str): Bearer 토큰
    
    Returns:
        JSON: 토큰 검증 결과
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({
            "success": False,
            "message": "유효한 인증 토큰이 필요합니다."
        }), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        # 토큰 디코딩 및 검증
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        return jsonify({
            "success": True,
            "message": "유효한 토큰입니다.",
            "user": {
                "email": payload['email'],
                "name": payload['name']
            }
        })
    except jwt.ExpiredSignatureError:
        return jsonify({
            "success": False,
            "message": "토큰이 만료되었습니다."
        }), 401
    except jwt.InvalidTokenError:
        return jsonify({
            "success": False,
            "message": "유효하지 않은 토큰입니다."
        }), 401
