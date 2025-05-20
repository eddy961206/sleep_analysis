import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class SleepAnalyzer:
    """
    수면 데이터 분석을 위한 클래스
    """
    
    def __init__(self):
        """
        SleepAnalyzer 초기화
        """
        self.sleep_data = None
        self.activity_data = None
        self.stress_data = None
        self.feedback_data = None
    
    def load_data(self, sleep_data: List[Dict], activity_data: List[Dict] = None, 
                 stress_data: List[Dict] = None, feedback_data: List[Dict] = None):
        """
        분석을 위한 데이터 로드
        
        Args:
            sleep_data: 수면 데이터 리스트
            activity_data: 활동 데이터 리스트 (선택)
            stress_data: 스트레스 데이터 리스트 (선택)
            feedback_data: 사용자 피드백 데이터 리스트 (선택)
        """
        # 수면 데이터를 DataFrame으로 변환
        self.sleep_data = pd.DataFrame(sleep_data)
        
        # 시작 및 종료 시간을 datetime 객체로 변환
        if 'start_time' in self.sleep_data.columns:
            self.sleep_data['start_time'] = pd.to_datetime(self.sleep_data['start_time'])
        if 'end_time' in self.sleep_data.columns:
            self.sleep_data['end_time'] = pd.to_datetime(self.sleep_data['end_time'])
        
        # 날짜 컬럼 추가
        if 'start_time' in self.sleep_data.columns:
            self.sleep_data['date'] = self.sleep_data['start_time'].dt.date
        
        # 활동 데이터가 제공된 경우 DataFrame으로 변환
        if activity_data:
            self.activity_data = pd.DataFrame(activity_data)
            if 'date' in self.activity_data.columns:
                self.activity_data['date'] = pd.to_datetime(self.activity_data['date']).dt.date
        
        # 스트레스 데이터가 제공된 경우 DataFrame으로 변환
        if stress_data:
            self.stress_data = pd.DataFrame(stress_data)
            if 'date' in self.stress_data.columns:
                self.stress_data['date'] = pd.to_datetime(self.stress_data['date']).dt.date
        
        # 피드백 데이터가 제공된 경우 DataFrame으로 변환
        if feedback_data:
            self.feedback_data = pd.DataFrame(feedback_data)
            if 'date' in self.feedback_data.columns:
                self.feedback_data['date'] = pd.to_datetime(self.feedback_data['date']).dt.date
    
    def get_sleep_summary(self) -> Dict:
        """
        수면 데이터 요약 정보 계산
        
        Returns:
            Dict: 수면 요약 정보
        """
        if self.sleep_data is None or len(self.sleep_data) == 0:
            return {
                "average_duration": 0,
                "average_efficiency": 0,
                "average_deep_sleep": 0,
                "average_light_sleep": 0,
                "average_rem_sleep": 0,
                "average_awake_time": 0
            }
        
        # 평균 수면 시간 (분)
        avg_duration = self.sleep_data['duration'].mean()
        
        # 평균 수면 효율
        avg_efficiency = self.sleep_data['efficiency'].mean() if 'efficiency' in self.sleep_data.columns else 0
        
        # 수면 단계별 평균 시간
        avg_deep = 0
        avg_light = 0
        avg_rem = 0
        avg_awake = 0
        
        if 'stages' in self.sleep_data.columns:
            # 수면 단계 데이터가 중첩된 딕셔너리 형태인 경우
            stages_data = self.sleep_data['stages'].tolist()
            deep_values = [stage.get('deep', 0) for stage in stages_data if isinstance(stage, dict)]
            light_values = [stage.get('light', 0) for stage in stages_data if isinstance(stage, dict)]
            rem_values = [stage.get('rem', 0) for stage in stages_data if isinstance(stage, dict)]
            awake_values = [stage.get('awake', 0) for stage in stages_data if isinstance(stage, dict)]
            
            if deep_values:
                avg_deep = sum(deep_values) / len(deep_values)
            if light_values:
                avg_light = sum(light_values) / len(light_values)
            if rem_values:
                avg_rem = sum(rem_values) / len(rem_values)
            if awake_values:
                avg_awake = sum(awake_values) / len(awake_values)
        
        return {
            "average_duration": avg_duration,
            "average_duration_hours": round(avg_duration / 60, 2),
            "average_efficiency": avg_efficiency,
            "average_deep_sleep": avg_deep,
            "average_deep_sleep_hours": round(avg_deep / 60, 2),
            "average_light_sleep": avg_light,
            "average_light_sleep_hours": round(avg_light / 60, 2),
            "average_rem_sleep": avg_rem,
            "average_rem_sleep_hours": round(avg_rem / 60, 2),
            "average_awake_time": avg_awake,
            "average_awake_time_hours": round(avg_awake / 60, 2)
        }
    
    def get_optimal_sleep_time(self) -> Dict:
        """
        최적의 수면 시간 및 패턴 분석
        
        Returns:
            Dict: 최적 수면 시간 정보
        """
        if self.sleep_data is None or len(self.sleep_data) < 3:
            return {
                "optimal_bedtime": "23:00",
                "optimal_waketime": "07:00",
                "optimal_duration": 480  # 8시간 (분)
            }
        
        # 피드백 데이터가 있는 경우, 피드백 점수가 높은 날의 수면 패턴 분석
        if self.feedback_data is not None and len(self.feedback_data) > 0:
            # 피드백 점수가 4 이상인 날짜 추출
            good_days = self.feedback_data[
                (self.feedback_data['sleep_satisfaction'] >= 4) | 
                (self.feedback_data['morning_condition'] >= 4)
            ]['date'].tolist()
            
            # 좋은 날의 수면 데이터 필터링
            good_sleep = self.sleep_data[self.sleep_data['date'].isin(good_days)]
            
            # 좋은 날의 데이터가 충분한 경우
            if len(good_sleep) >= 3:
                bedtimes = good_sleep['start_time'].dt.hour + good_sleep['start_time'].dt.minute / 60
                waketimes = good_sleep['end_time'].dt.hour + good_sleep['end_time'].dt.minute / 60
                durations = good_sleep['duration']
            else:
                # 충분하지 않은 경우 전체 데이터 사용
                bedtimes = self.sleep_data['start_time'].dt.hour + self.sleep_data['start_time'].dt.minute / 60
                waketimes = self.sleep_data['end_time'].dt.hour + self.sleep_data['end_time'].dt.minute / 60
                durations = self.sleep_data['duration']
        else:
            # 피드백 데이터가 없는 경우 전체 데이터 사용
            bedtimes = self.sleep_data['start_time'].dt.hour + self.sleep_data['start_time'].dt.minute / 60
            waketimes = self.sleep_data['end_time'].dt.hour + self.sleep_data['end_time'].dt.minute / 60
            durations = self.sleep_data['duration']
        
        # 평균 취침 시간 및 기상 시간 계산
        avg_bedtime = bedtimes.mean()
        avg_waketime = waketimes.mean()
        avg_duration = durations.mean()
        
        # 시간 형식으로 변환
        bedtime_hour = int(avg_bedtime)
        bedtime_minute = int((avg_bedtime - bedtime_hour) * 60)
        
        waketime_hour = int(avg_waketime)
        waketime_minute = int((avg_waketime - waketime_hour) * 60)
        
        # 취침 시간이 24시를 넘어가는 경우 처리
        if bedtime_hour >= 24:
            bedtime_hour -= 24
        
        # 시간 형식 문자열로 변환
        optimal_bedtime = f"{bedtime_hour:02d}:{bedtime_minute:02d}"
        optimal_waketime = f"{waketime_hour:02d}:{waketime_minute:02d}"
        
        return {
            "optimal_bedtime": optimal_bedtime,
            "optimal_waketime": optimal_waketime,
            "optimal_duration": avg_duration,
            "optimal_duration_hours": round(avg_duration / 60, 2)
        }
    
    def analyze_sleep_trends(self, days: int = 30) -> Dict:
        """
        수면 트렌드 분석
        
        Args:
            days: 분석할 기간 (일)
            
        Returns:
            Dict: 수면 트렌드 분석 결과
        """
        if self.sleep_data is None or len(self.sleep_data) == 0:
            return {
                "trend": "stable",
                "weekly_change": 0,
                "monthly_change": 0
            }
        
        # 날짜별로 정렬
        self.sleep_data = self.sleep_data.sort_values('start_time')
        
        # 최근 데이터만 필터링
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_data = self.sleep_data[self.sleep_data['start_time'] >= cutoff_date]
        
        if len(recent_data) < 7:
            return {
                "trend": "insufficient_data",
                "weekly_change": 0,
                "monthly_change": 0
            }
        
        # 주간 변화 계산
        last_week = recent_data[recent_data['start_time'] >= (datetime.now() - timedelta(days=7))]
        previous_week = recent_data[
            (recent_data['start_time'] < (datetime.now() - timedelta(days=7))) & 
            (recent_data['start_time'] >= (datetime.now() - timedelta(days=14)))
        ]
        
        if len(last_week) > 0 and len(previous_week) > 0:
            last_week_avg = last_week['duration'].mean()
            previous_week_avg = previous_week['duration'].mean()
            weekly_change = last_week_avg - previous_week_avg
        else:
            weekly_change = 0
        
        # 월간 변화 계산
        last_month = recent_data
        previous_month = self.sleep_data[
            (self.sleep_data['start_time'] < cutoff_date) & 
            (self.sleep_data['start_time'] >= (cutoff_date - timedelta(days=days)))
        ]
        
        if len(last_month) > 0 and len(previous_month) > 0:
            last_month_avg = last_month['duration'].mean()
            previous_month_avg = previous_month['duration'].mean()
            monthly_change = last_month_avg - previous_month_avg
        else:
            monthly_change = 0
        
        # 트렌드 결정
        if abs(weekly_change) < 10:  # 10분 미만 변화는 안정적
            trend = "stable"
        elif weekly_change > 0:
            trend = "improving"
        else:
            trend = "declining"
        
        return {
            "trend": trend,
            "weekly_change": weekly_change,
            "weekly_change_hours": round(weekly_change / 60, 2),
            "monthly_change": monthly_change,
            "monthly_change_hours": round(monthly_change / 60, 2)
        }
    
    def analyze_correlations(self) -> Dict:
        """
        수면과 다른 지표 간의 상관관계 분석
        
        Returns:
            Dict: 상관관계 분석 결과
        """
        correlations = {}
        
        # 수면 데이터가 없는 경우
        if self.sleep_data is None or len(self.sleep_data) < 5:
            return {
                "activity_correlation": 0,
                "stress_correlation": 0
            }
        
        # 활동량과 수면의 상관관계
        if self.activity_data is not None and len(self.activity_data) > 0:
            # 날짜를 기준으로 데이터 병합
            merged_activity = pd.merge(
                self.sleep_data[['date', 'duration', 'efficiency']], 
                self.activity_data[['date', 'steps', 'active_minutes']], 
                on='date', 
                how='inner'
            )
            
            if len(merged_activity) >= 5:
                # 상관계수 계산
                corr_steps_duration = merged_activity[['steps', 'duration']].corr().iloc[0, 1]
                corr_active_duration = merged_activity[['active_minutes', 'duration']].corr().iloc[0, 1]
                
                # 효율과의 상관관계도 계산
                corr_steps_efficiency = 0
                corr_active_efficiency = 0
                
                if 'efficiency' in merged_activity.columns:
                    corr_steps_efficiency = merged_activity[['steps', 'efficiency']].corr().iloc[0, 1]
                    corr_active_efficiency = merged_activity[['active_minutes', 'efficiency']].corr().iloc[0, 1]
                
                correlations["activity_correlation"] = {
                    "steps_duration": corr_steps_duration,
                    "active_minutes_duration": corr_active_duration,
                    "steps_efficiency": corr_steps_efficiency,
                    "active_minutes_efficiency": corr_active_efficiency
                }
            else:
                correlations["activity_correlation"] = {
                    "steps_duration": 0,
                    "active_minutes_duration": 0,
                    "steps_efficiency": 0,
                    "active_minutes_efficiency": 0
                }
        
        # 스트레스와 수면의 상관관계
        if self.stress_data is not None and len(self.stress_data) > 0:
            # 날짜를 기준으로 데이터 병합
            merged_stress = pd.merge(
                self.sleep_data[['date', 'duration', 'efficiency']], 
                self.stress_data[['date', 'average_score']], 
                on='date', 
                how='inner'
            )
            
            if len(merged_stress) >= 5:
                # 상관계수 계산
                corr_stress_duration = merged_stress[['average_score', 'duration']].corr().iloc[0, 1]
                
                # 효율과의 상관관계도 계산
                corr_stress_efficiency = 0
                
                if 'efficiency' in merged_stress.columns:
                    corr_stress_efficiency = merged_stress[['average_score', 'efficiency']].corr().iloc[0, 1]
                
                correlations["stress_correlation"] = {
                    "stress_duration": corr_stress_duration,
                    "stress_efficiency": corr_stress_efficiency
                }
            else:
                correlations["stress_correlation"] = {
                    "stress_duration": 0,
                    "stress_efficiency": 0
                }
        
        return correlations
    
    def get_comprehensive_analysis(self) -> Dict:
        """
        종합적인 수면 분석 결과 제공
        
        Returns:
            Dict: 종합 분석 결과
        """
        # 각 분석 결과 통합
        summary = self.get_sleep_summary()
        optimal = self.get_optimal_sleep_time()
        trends = self.analyze_sleep_trends()
        correlations = self.analyze_correlations()
        
        # 종합 분석 결과
        return {
            "summary": summary,
            "optimal_sleep": optimal,
            "trends": trends,
            "correlations": correlations
        }
