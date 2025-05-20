from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

# Blueprint 정의
health_connect_bp = Blueprint('health_connect', __name__)

# 샘플 데이터 - 실제 구현에서는 Health Connect API와 연동
sample_sleep_data = [
    {
        "id": "sleep_1",
        "start_time": (datetime.now() - timedelta(days=1)).replace(hour=23, minute=0, second=0).isoformat(),
        "end_time": datetime.now().replace(hour=7, minute=15, second=0).isoformat(),
        "duration": 8 * 60 + 15,  # 분 단위
        "efficiency": 85,
        "stages": {
            "deep": 105,  # 분 단위
            "light": 250,
            "rem": 80,
            "awake": 50
        }
    },
    {
        "id": "sleep_2",
        "start_time": (datetime.now() - timedelta(days=2)).replace(hour=23, minute=30, second=0).isoformat(),
        "end_time": (datetime.now() - timedelta(days=1)).replace(hour=6, minute=45, second=0).isoformat(),
        "duration": 7 * 60 + 15,
        "efficiency": 82,
        "stages": {
            "deep": 95,
            "light": 230,
            "rem": 75,
            "awake": 55
        }
    },
    {
        "id": "sleep_3",
        "start_time": (datetime.now() - timedelta(days=3)).replace(hour=22, minute=45, second=0).isoformat(),
        "end_time": (datetime.now() - timedelta(days=2)).replace(hour=6, minute=30, second=0).isoformat(),
        "duration": 7 * 60 + 45,
        "efficiency": 88,
        "stages": {
            "deep": 110,
            "light": 240,
            "rem": 85,
            "awake": 40
        }
    }
]

sample_activity_data = [
    {
        "id": "activity_1",
        "date": (datetime.now() - timedelta(days=1)).date().isoformat(),
        "steps": 8750,
        "active_minutes": 45,
        "calories": 320
    },
    {
        "id": "activity_2",
        "date": (datetime.now() - timedelta(days=2)).date().isoformat(),
        "steps": 10200,
        "active_minutes": 60,
        "calories": 380
    },
    {
        "id": "activity_3",
        "date": (datetime.now() - timedelta(days=3)).date().isoformat(),
        "steps": 7500,
        "active_minutes": 35,
        "calories": 280
    }
]

sample_stress_data = [
    {
        "id": "stress_1",
        "date": (datetime.now() - timedelta(days=1)).date().isoformat(),
        "average_score": 45,
        "max_score": 75,
        "min_score": 20
    },
    {
        "id": "stress_2",
        "date": (datetime.now() - timedelta(days=2)).date().isoformat(),
        "average_score": 52,
        "max_score": 80,
        "min_score": 25
    },
    {
        "id": "stress_3",
        "date": (datetime.now() - timedelta(days=3)).date().isoformat(),
        "average_score": 38,
        "max_score": 65,
        "min_score": 15
    }
]

# 수면 데이터 API 엔드포인트
@health_connect_bp.route('/sleep', methods=['GET'])
def get_sleep_data():
    """
    수면 데이터를 가져오는 API 엔드포인트
    
    Query Parameters:
        start_date (str): 시작 날짜 (YYYY-MM-DD)
        end_date (str): 종료 날짜 (YYYY-MM-DD)
    
    Returns:
        JSON: 수면 데이터 목록
    """
    # 실제 구현에서는 Health Connect API를 통해 데이터 가져오기
    # 현재는 샘플 데이터 반환
    return jsonify({
        "success": True,
        "data": sample_sleep_data
    })

# 활동 데이터 API 엔드포인트
@health_connect_bp.route('/activity', methods=['GET'])
def get_activity_data():
    """
    활동 데이터를 가져오는 API 엔드포인트
    
    Query Parameters:
        start_date (str): 시작 날짜 (YYYY-MM-DD)
        end_date (str): 종료 날짜 (YYYY-MM-DD)
    
    Returns:
        JSON: 활동 데이터 목록
    """
    # 실제 구현에서는 Health Connect API를 통해 데이터 가져오기
    # 현재는 샘플 데이터 반환
    return jsonify({
        "success": True,
        "data": sample_activity_data
    })

# 스트레스 데이터 API 엔드포인트
@health_connect_bp.route('/stress', methods=['GET'])
def get_stress_data():
    """
    스트레스 데이터를 가져오는 API 엔드포인트
    
    Query Parameters:
        start_date (str): 시작 날짜 (YYYY-MM-DD)
        end_date (str): 종료 날짜 (YYYY-MM-DD)
    
    Returns:
        JSON: 스트레스 데이터 목록
    """
    # 실제 구현에서는 Health Connect API를 통해 데이터 가져오기
    # 현재는 샘플 데이터 반환
    return jsonify({
        "success": True,
        "data": sample_stress_data
    })

# Health Connect 연결 상태 확인 API 엔드포인트
@health_connect_bp.route('/status', methods=['GET'])
def get_connection_status():
    """
    Health Connect 연결 상태를 확인하는 API 엔드포인트
    
    Returns:
        JSON: 연결 상태 정보
    """
    # 실제 구현에서는 Health Connect API 연결 상태 확인
    # 현재는 샘플 데이터 반환
    return jsonify({
        "success": True,
        "connected": True,
        "permissions": {
            "sleep": True,
            "activity": True,
            "stress": True
        },
        "last_sync": datetime.now().isoformat()
    })

# 사용자 피드백 저장 API 엔드포인트
@health_connect_bp.route('/feedback', methods=['POST'])
def save_user_feedback():
    """
    사용자 피드백을 저장하는 API 엔드포인트
    
    Request Body:
        date (str): 날짜 (YYYY-MM-DD)
        sleep_satisfaction (int): 수면 만족도 (1-5)
        morning_condition (int): 기상 시 컨디션 (1-5)
        notes (str): 특이사항
    
    Returns:
        JSON: 저장 결과
    """
    # 요청 데이터 가져오기
    data = request.json
    
    # 실제 구현에서는 데이터베이스에 저장
    # 현재는 성공 응답만 반환
    return jsonify({
        "success": True,
        "message": "피드백이 성공적으로 저장되었습니다.",
        "data": data
    })
