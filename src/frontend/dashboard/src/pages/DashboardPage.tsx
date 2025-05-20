import React, { useState, useEffect } from 'react';
import { fetchSleepData, fetchActivityData, fetchStressData, saveUserFeedback } from '../api/healthConnectApi';
import SleepDashboard from '../components/SleepDashboard';

const DashboardPage: React.FC = () => {
  // 상태 관리
  const [sleepData, setSleepData] = useState([]);
  const [activityData, setActivityData] = useState([]);
  const [stressData, setStressData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 데이터 로드 함수
  const loadData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // 최근 30일 데이터 가져오기
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      
      const dateRange = {
        startDate: thirtyDaysAgo.toISOString().split('T')[0],
        endDate: new Date().toISOString().split('T')[0]
      };
      
      // 병렬로 데이터 요청
      const [sleepResult, activityResult, stressResult] = await Promise.all([
        fetchSleepData(dateRange),
        fetchActivityData(dateRange),
        fetchStressData(dateRange)
      ]);
      
      setSleepData(sleepResult);
      setActivityData(activityResult);
      setStressData(stressResult);
    } catch (err) {
      setError('데이터를 불러오는 중 오류가 발생했습니다.');
      console.error('데이터 로드 오류:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // 피드백 제출 핸들러
  const handleFeedbackSubmit = async (feedback: {
    sleep_satisfaction: number;
    morning_condition: number;
    notes?: string;
  }) => {
    try {
      const today = new Date().toISOString().split('T')[0];
      
      const feedbackData = {
        date: today,
        ...feedback
      };
      
      const success = await saveUserFeedback(feedbackData);
      
      if (success) {
        alert('피드백이 성공적으로 저장되었습니다.');
      } else {
        throw new Error('피드백 저장에 실패했습니다.');
      }
    } catch (err) {
      alert('피드백을 저장하는 중 오류가 발생했습니다.');
      console.error('피드백 저장 오류:', err);
    }
  };

  // 컴포넌트 마운트 시 데이터 로드
  useEffect(() => {
    loadData();
  }, []);

  // 로딩 상태 표시
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">데이터를 불러오는 중입니다...</p>
        </div>
      </div>
    );
  }

  // 에러 상태 표시
  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center p-6 bg-red-50 rounded-lg">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-red-500 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="mt-4 text-red-800">{error}</p>
          <button 
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            onClick={loadData}
          >
            다시 시도
          </button>
        </div>
      </div>
    );
  }

  // 대시보드 렌더링
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">수면 데이터 분석 대시보드</h1>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <SleepDashboard 
            sleepData={sleepData}
            activityData={activityData}
            stressData={stressData}
            onFeedbackSubmit={handleFeedbackSubmit}
            onRefresh={loadData}
          />
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;
