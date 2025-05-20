import os
import sys
import json
from datetime import datetime, timedelta
import requests

class HealthConnectClient:
    """
    Health Connect API 클라이언트
    실제 Health Connect API와 통신하여 수면, 활동, 스트레스 데이터를 가져옵니다.
    """
    
    def __init__(self, base_url=None, api_key=None):
        """
        HealthConnectClient 초기화
        
        Args:
            base_url (str): Health Connect API 기본 URL (선택)
            api_key (str): Health Connect API 키 (선택)
        """
        self.base_url = base_url or os.environ.get('HEALTH_CONNECT_URL', 'https://healthconnect-api.example.com')
        self.api_key = api_key or os.environ.get('HEALTH_CONNECT_API_KEY', '')
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def get_sleep_data(self, start_date=None, end_date=None):
        """
        수면 데이터 가져오기
        
        Args:
            start_date (str): 시작 날짜 (YYYY-MM-DD)
            end_date (str): 종료 날짜 (YYYY-MM-DD)
            
        Returns:
            list: 수면 데이터 목록
        """
        try:
            # 날짜 범위 설정
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            # API 요청 URL 및 파라미터
            url = f"{self.base_url}/sleep"
            params = {
                'start_date': start_date,
                'end_date': end_date
            }
            
            # 실제 구현에서는 API 요청
            # response = requests.get(url, headers=self.headers, params=params)
            # response.raise_for_status()
            # return response.json()
            
            # 현재는 샘플 데이터 반환
            return self._get_sample_sleep_data(start_date, end_date)
        except Exception as e:
            print(f"수면 데이터 가져오기 오류: {e}")
            return []
    
    def get_activity_data(self, start_date=None, end_date=None):
        """
        활동 데이터 가져오기
        
        Args:
            start_date (str): 시작 날짜 (YYYY-MM-DD)
            end_date (str): 종료 날짜 (YYYY-MM-DD)
            
        Returns:
            list: 활동 데이터 목록
        """
        try:
            # 날짜 범위 설정
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            # API 요청 URL 및 파라미터
            url = f"{self.base_url}/activity"
            params = {
                'start_date': start_date,
                'end_date': end_date
            }
            
            # 실제 구현에서는 API 요청
            # response = requests.get(url, headers=self.headers, params=params)
            # response.raise_for_status()
            # return response.json()
            
            # 현재는 샘플 데이터 반환
            return self._get_sample_activity_data(start_date, end_date)
        except Exception as e:
            print(f"활동 데이터 가져오기 오류: {e}")
            return []
    
    def get_stress_data(self, start_date=None, end_date=None):
        """
        스트레스 데이터 가져오기
        
        Args:
            start_date (str): 시작 날짜 (YYYY-MM-DD)
            end_date (str): 종료 날짜 (YYYY-MM-DD)
            
        Returns:
            list: 스트레스 데이터 목록
        """
        try:
            # 날짜 범위 설정
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            # API 요청 URL 및 파라미터
            url = f"{self.base_url}/stress"
            params = {
                'start_date': start_date,
                'end_date': end_date
            }
            
            # 실제 구현에서는 API 요청
            # response = requests.get(url, headers=self.headers, params=params)
            # response.raise_for_status()
            # return response.json()
            
            # 현재는 샘플 데이터 반환
            return self._get_sample_stress_data(start_date, end_date)
        except Exception as e:
            print(f"스트레스 데이터 가져오기 오류: {e}")
            return []
    
    def check_connection_status(self):
        """
        Health Connect 연결 상태 확인
        
        Returns:
            dict: 연결 상태 정보
        """
        try:
            # API 요청 URL
            url = f"{self.base_url}/status"
            
            # 실제 구현에서는 API 요청
            # response = requests.get(url, headers=self.headers)
            # response.raise_for_status()
            # return response.json()
            
            # 현재는 샘플 데이터 반환
            return {
                "connected": True,
                "permissions": {
                    "sleep": True,
                    "activity": True,
                    "stress": True
                },
                "last_sync": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"연결 상태 확인 오류: {e}")
            return {
                "connected": False,
                "permissions": {
                    "sleep": False,
                    "activity": False,
                    "stress": False
                },
                "last_sync": datetime.now().isoformat()
            }
    
    def _get_sample_sleep_data(self, start_date, end_date):
        """
        샘플 수면 데이터 생성
        
        Args:
            start_date (str): 시작 날짜 (YYYY-MM-DD)
            end_date (str): 종료 날짜 (YYYY-MM-DD)
            
        Returns:
            list: 샘플 수면 데이터 목록
        """
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        sleep_data = []
        current_date = start
        
        while current_date <= end:
            # 임의의 수면 데이터 생성
            sleep_start = current_date.replace(hour=23, minute=0, second=0)
            sleep_end = (current_date + timedelta(days=1)).replace(hour=7, minute=0, second=0)
            
            # 일부 변동성 추가
            sleep_start = sleep_start - timedelta(minutes=(current_date.day % 5) * 10)
            sleep_end = sleep_end + timedelta(minutes=(current_date.day % 3) * 15)
            
            # 수면 시간 계산 (분 단위)
            duration = int((sleep_end - sleep_start).total_seconds() / 60)
            
            # 수면 효율 (75-95% 범위)
            efficiency = 85 + (current_date.day % 10)
            if efficiency > 95:
                efficiency = 95
            
            # 수면 단계
            deep_sleep = int(duration * 0.2) + (current_date.day % 10)
            light_sleep = int(duration * 0.5) + (current_date.day % 15)
            rem_sleep = int(duration * 0.2) + (current_date.day % 5)
            awake_time = duration - deep_sleep - light_sleep - rem_sleep
            
            sleep_data.append({
                "id": f"sleep_{current_date.strftime('%Y%m%d')}",
                "start_time": sleep_start.isoformat(),
                "end_time": sleep_end.isoformat(),
                "duration": duration,
                "efficiency": efficiency,
                "stages": {
                    "deep": deep_sleep,
                    "light": light_sleep,
                    "rem": rem_sleep,
                    "awake": awake_time
                }
            })
            
            current_date += timedelta(days=1)
        
        return sleep_data
    
    def _get_sample_activity_data(self, start_date, end_date):
        """
        샘플 활동 데이터 생성
        
        Args:
            start_date (str): 시작 날짜 (YYYY-MM-DD)
            end_date (str): 종료 날짜 (YYYY-MM-DD)
            
        Returns:
            list: 샘플 활동 데이터 목록
        """
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        activity_data = []
        current_date = start
        
        while current_date <= end:
            # 임의의 활동 데이터 생성
            base_steps = 8000
            steps = base_steps + (current_date.day * 100) + (current_date.weekday() * 500)
            
            # 주말에는 활동량 감소
            if current_date.weekday() >= 5:  # 5: 토요일, 6: 일요일
                steps = int(steps * 0.8)
            
            # 활동 시간 (분 단위)
            active_minutes = int(steps / 100) + (current_date.day % 20)
            
            # 소모 칼로리
            calories = int(active_minutes * 5) + (current_date.day * 10)
            
            activity_data.append({
                "id": f"activity_{current_date.strftime('%Y%m%d')}",
                "date": current_date.date().isoformat(),
                "steps": steps,
                "active_minutes": active_minutes,
                "calories": calories
            })
            
            current_date += timedelta(days=1)
        
        return activity_data
    
    def _get_sample_stress_data(self, start_date, end_date):
        """
        샘플 스트레스 데이터 생성
        
        Args:
            start_date (str): 시작 날짜 (YYYY-MM-DD)
            end_date (str): 종료 날짜 (YYYY-MM-DD)
            
        Returns:
            list: 샘플 스트레스 데이터 목록
        """
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        stress_data = []
        current_date = start
        
        while current_date <= end:
            # 임의의 스트레스 데이터 생성
            base_score = 40
            
            # 주중에는 스트레스 증가
            if 0 <= current_date.weekday() <= 4:  # 0-4: 월-금
                base_score += 10
            
            # 일부 변동성 추가
            avg_score = base_score + (current_date.day % 15)
            max_score = avg_score + 20 + (current_date.day % 10)
            min_score = avg_score - 15 - (current_date.day % 10)
            
            # 범위 제한
            if max_score > 100:
                max_score = 100
            if min_score < 0:
                min_score = 0
            
            stress_data.append({
                "id": f"stress_{current_date.strftime('%Y%m%d')}",
                "date": current_date.date().isoformat(),
                "average_score": avg_score,
                "max_score": max_score,
                "min_score": min_score
            })
            
            current_date += timedelta(days=1)
        
        return stress_data

# 테스트 코드
if __name__ == "__main__":
    client = HealthConnectClient()
    
    # 수면 데이터 테스트
    sleep_data = client.get_sleep_data()
    print(f"수면 데이터 샘플: {sleep_data[0]}")
    
    # 활동 데이터 테스트
    activity_data = client.get_activity_data()
    print(f"활동 데이터 샘플: {activity_data[0]}")
    
    # 스트레스 데이터 테스트
    stress_data = client.get_stress_data()
    print(f"스트레스 데이터 샘플: {stress_data[0]}")
    
    # 연결 상태 테스트
    status = client.check_connection_status()
    print(f"연결 상태: {status}")
