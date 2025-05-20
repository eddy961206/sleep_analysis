from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../data_analysis/src')))
from src.data_analysis.src.health_connect_interface import HealthConnectInterface

# Blueprint 정의
analysis_bp = Blueprint('analysis', __name__)

# Health Connect 인터페이스 초기화
health_interface = HealthConnectInterface()

# 샘플 데이터 - 실제 구현에서는 데이터베이스에서 가져옴
sample_feedback_data = [
    {
        "date": (datetime.now() - timedelta(days=1)).date().isoformat(),
        "sleep_satisfaction": 4,
        "morning_condition": 4,
        "notes": "잘 잤음"
    },
    {
        "date": (datetime.now() - timedelta(days=2)).date().isoformat(),
        "sleep_satisfaction": 3,
        "morning_condition": 3,
        "notes": "평범했음"
    },
    {
        "date": (datetime.now() - timedelta(days=3)).date().isoformat(),
        "sleep_satisfaction": 5,
        "morning_condition": 4,
        "notes": "매우 잘 잤음"
    }
]

# 종합 분석 API 엔드포인트
@analysis_bp.route('/comprehensive', methods=['GET'])
def get_comprehensive_analysis():
    """
    종합적인 수면 분석 결과를 제공하는 API 엔드포인트
    
    Query Parameters:
        start_date (str): 시작 날짜 (YYYY-MM-DD)
        end_date (str): 종료 날짜 (YYYY-MM-DD)
    
    Returns:
        JSON: 종합 분석 결과
    """
    try:
        # 실제 구현에서는 Health Connect API 및 데이터베이스에서 데이터 가져오기
        # 현재는 샘플 데이터 사용
        from src.routes.health_connect import sample_sleep_data, sample_activity_data, sample_stress_data
        
        # 데이터 분석 실행
        analysis_result = health_interface.process_data(
            sleep_data=sample_sleep_data,
            activity_data=sample_activity_data,
            stress_data=sample_stress_data,
            feedback_data=sample_feedback_data
        )
        
        return jsonify({
            "success": True,
            "data": analysis_result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# 수면 요약 API 엔드포인트
@analysis_bp.route('/sleep_summary', methods=['GET'])
def get_sleep_summary():
    """
    수면 데이터 요약 정보를 제공하는 API 엔드포인트
    
    Query Parameters:
        start_date (str): 시작 날짜 (YYYY-MM-DD)
        end_date (str): 종료 날짜 (YYYY-MM-DD)
    
    Returns:
        JSON: 수면 요약 정보
    """
    try:
        # 실제 구현에서는 Health Connect API에서 데이터 가져오기
        # 현재는 샘플 데이터 사용
        from src.routes.health_connect import sample_sleep_data
        
        # 데이터 분석 실행
        summary_result = health_interface.get_sleep_summary(sample_sleep_data)
        
        return jsonify({
            "success": True,
            "data": summary_result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# 최적 수면 시간 API 엔드포인트
@analysis_bp.route('/optimal_sleep', methods=['GET'])
def get_optimal_sleep():
    """
    최적의 수면 시간 및 패턴을 제공하는 API 엔드포인트
    
    Query Parameters:
        start_date (str): 시작 날짜 (YYYY-MM-DD)
        end_date (str): 종료 날짜 (YYYY-MM-DD)
    
    Returns:
        JSON: 최적 수면 시간 정보
    """
    try:
        # 실제 구현에서는 Health Connect API 및 데이터베이스에서 데이터 가져오기
        # 현재는 샘플 데이터 사용
        from src.routes.health_connect import sample_sleep_data
        
        # 데이터 분석 실행
        optimal_result = health_interface.get_optimal_sleep_time(
            sleep_data=sample_sleep_data,
            feedback_data=sample_feedback_data
        )
        
        return jsonify({
            "success": True,
            "data": optimal_result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# 수면 트렌드 API 엔드포인트
@analysis_bp.route('/trends', methods=['GET'])
def get_sleep_trends():
    """
    수면 트렌드 분석 결과를 제공하는 API 엔드포인트
    
    Query Parameters:
        days (int): 분석할 기간 (일)
    
    Returns:
        JSON: 수면 트렌드 분석 결과
    """
    try:
        # 분석 기간 파라미터 가져오기
        days = request.args.get('days', default=30, type=int)
        
        # 실제 구현에서는 Health Connect API에서 데이터 가져오기
        # 현재는 샘플 데이터 사용
        from src.routes.health_connect import sample_sleep_data
        
        # 데이터 분석 실행
        trends_result = health_interface.analyze_sleep_trends(
            sleep_data=sample_sleep_data,
            days=days
        )
        
        return jsonify({
            "success": True,
            "data": trends_result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# 상관관계 분석 API 엔드포인트
@analysis_bp.route('/correlations', methods=['GET'])
def get_correlations():
    """
    수면과 다른 지표 간의 상관관계 분석 결과를 제공하는 API 엔드포인트
    
    Returns:
        JSON: 상관관계 분석 결과
    """
    try:
        # 실제 구현에서는 Health Connect API에서 데이터 가져오기
        # 현재는 샘플 데이터 사용
        from src.routes.health_connect import sample_sleep_data, sample_activity_data, sample_stress_data
        
        # 데이터 분석 실행
        correlations_result = health_interface.analyze_correlations(
            sleep_data=sample_sleep_data,
            activity_data=sample_activity_data,
            stress_data=sample_stress_data
        )
        
        return jsonify({
            "success": True,
            "data": correlations_result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
