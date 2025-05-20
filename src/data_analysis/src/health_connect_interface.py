import pandas as pd
import numpy as np
from datetime import datetime, timedelta
# from src.analysis.sleep_analyzer import SleepAnalyzer # 이 줄을 아래처럼 바꿔!
from src.data_analysis.src.analysis.sleep_analyzer import SleepAnalyzer  # 현재 폴더(.)의 analysis 폴더에서 가져와!

class HealthConnectInterface:
    """
    Health Connect API와 데이터 분석 모듈 간의 인터페이스
    """
    
    def __init__(self):
        """
        HealthConnectInterface 초기화
        """
        self.analyzer = SleepAnalyzer()
    
    def process_data(self, sleep_data, activity_data=None, stress_data=None, feedback_data=None):
        """
        Health Connect API에서 가져온 데이터를 처리하고 분석
        
        Args:
            sleep_data: 수면 데이터
            activity_data: 활동 데이터 (선택)
            stress_data: 스트레스 데이터 (선택)
            feedback_data: 사용자 피드백 데이터 (선택)
            
        Returns:
            Dict: 분석 결과
        """
        # 데이터 로드
        self.analyzer.load_data(
            sleep_data=sleep_data,
            activity_data=activity_data,
            stress_data=stress_data,
            feedback_data=feedback_data
        )
        
        # 종합 분석 실행
        return self.analyzer.get_comprehensive_analysis()
    
    def get_sleep_summary(self, sleep_data):
        """
        수면 데이터 요약 정보 계산
        
        Args:
            sleep_data: 수면 데이터
            
        Returns:
            Dict: 수면 요약 정보
        """
        self.analyzer.load_data(sleep_data=sleep_data)
        return self.analyzer.get_sleep_summary()
    
    def get_optimal_sleep_time(self, sleep_data, feedback_data=None):
        """
        최적의 수면 시간 및 패턴 분석
        
        Args:
            sleep_data: 수면 데이터
            feedback_data: 사용자 피드백 데이터 (선택)
            
        Returns:
            Dict: 최적 수면 시간 정보
        """
        self.analyzer.load_data(sleep_data=sleep_data, feedback_data=feedback_data)
        return self.analyzer.get_optimal_sleep_time()
    
    def analyze_sleep_trends(self, sleep_data, days=30):
        """
        수면 트렌드 분석
        
        Args:
            sleep_data: 수면 데이터
            days: 분석할 기간 (일)
            
        Returns:
            Dict: 수면 트렌드 분석 결과
        """
        self.analyzer.load_data(sleep_data=sleep_data)
        return self.analyzer.analyze_sleep_trends(days=days)
    
    def analyze_correlations(self, sleep_data, activity_data=None, stress_data=None):
        """
        수면과 다른 지표 간의 상관관계 분석
        
        Args:
            sleep_data: 수면 데이터
            activity_data: 활동 데이터 (선택)
            stress_data: 스트레스 데이터 (선택)
            
        Returns:
            Dict: 상관관계 분석 결과
        """
        self.analyzer.load_data(
            sleep_data=sleep_data,
            activity_data=activity_data,
            stress_data=stress_data
        )
        return self.analyzer.analyze_correlations()

# 테스트 코드
if __name__ == "__main__":
    # 샘플 데이터
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
        }
    ]
    
    # 인터페이스 초기화 및 테스트
    interface = HealthConnectInterface()
    result = interface.get_sleep_summary(sample_sleep_data)
    print("수면 요약:", result)
