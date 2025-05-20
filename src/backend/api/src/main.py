import sys
import os
# 현재 파일(main.py)의 디렉토리: D:\WorkSpaces\python_workspace\sleep_analysis\src\backend\api\src
# 여기서 4번 부모 디렉토리로 올라가면 프로젝트 루트(sleep_analysis)가 된다.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
# 파이썬 모듈 검색 경로 리스트의 맨 앞에 프로젝트 루트를 추가
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, jsonify, send_from_directory
from src.backend.api.src.routes.health_connect import health_connect_bp
from src.backend.api.src.routes.analysis import analysis_bp
from src.backend.api.src.routes.auth import auth_bp

# Flask 앱 초기화
app = Flask(__name__)

# 블루프린트 등록
app.register_blueprint(health_connect_bp, url_prefix='/api/health_connect')
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# 데이터베이스 설정 (필요시 주석 해제)
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS 설정
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 루트 경로
@app.route('/')
def index():
    return jsonify({
        "name": "수면 데이터 분석 API",
        "version": "1.0.0",
        "status": "running"
    })

# 정적 파일 제공 (프론트엔드 배포용)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# 에러 핸들러
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "리소스를 찾을 수 없습니다."
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "서버 내부 오류가 발생했습니다."
    }), 500

# 앱 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
