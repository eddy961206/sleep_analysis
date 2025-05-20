import React, { useEffect, useState } from 'react';
import { fetchSleepData, fetchActivityData, fetchStressData } from '../api/healthConnectApi';

// 차트 라이브러리 가져오기 (실제 구현 시 설치 필요)
// import { LineChart, Line, BarChart, Bar, PieChart, Pie, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface SleepDataVisualizerProps {
  sleepData: any[];
  activityData: any[];
  stressData: any[];
  onRefresh: () => void;
}

const SleepDataVisualizer: React.FC<SleepDataVisualizerProps> = ({ 
  sleepData, 
  activityData, 
  stressData,
  onRefresh 
}) => {
  const [summaryData, setSummaryData] = useState({
    averageDuration: 0,
    averageEfficiency: 0,
    deepSleepPercentage: 0,
    lightSleepPercentage: 0,
    remSleepPercentage: 0,
    awakePercentage: 0
  });

  const [optimalSleepTime, setOptimalSleepTime] = useState({
    bedtime: '23:00',
    waketime: '07:00',
    duration: '8시간'
  });

  const [sleepTrend, setSleepTrend] = useState({
    weeklyChange: 0,
    monthlyChange: 0,
    trend: 'stable'
  });

  // 데이터 처리 및 계산
  useEffect(() => {
    if (sleepData && sleepData.length > 0) {
      // 평균 수면 시간 계산
      const totalDuration = sleepData.reduce((sum, item) => sum + item.duration, 0);
      const avgDuration = totalDuration / sleepData.length;
      
      // 평균 수면 효율 계산
      const totalEfficiency = sleepData.reduce((sum, item) => sum + item.efficiency, 0);
      const avgEfficiency = totalEfficiency / sleepData.length;
      
      // 수면 단계 비율 계산
      let totalDeep = 0;
      let totalLight = 0;
      let totalRem = 0;
      let totalAwake = 0;
      
      sleepData.forEach(item => {
        if (item.stages) {
          totalDeep += item.stages.deep || 0;
          totalLight += item.stages.light || 0;
          totalRem += item.stages.rem || 0;
          totalAwake += item.stages.awake || 0;
        }
      });
      
      const totalStages = totalDeep + totalLight + totalRem + totalAwake;
      
      setSummaryData({
        averageDuration: avgDuration,
        averageEfficiency: avgEfficiency,
        deepSleepPercentage: totalStages > 0 ? (totalDeep / totalStages) * 100 : 0,
        lightSleepPercentage: totalStages > 0 ? (totalLight / totalStages) * 100 : 0,
        remSleepPercentage: totalStages > 0 ? (totalRem / totalStages) * 100 : 0,
        awakePercentage: totalStages > 0 ? (totalAwake / totalStages) * 100 : 0
      });
      
      // 최적 수면 시간 계산 (간단한 예시)
      // 실제로는 백엔드 API를 통해 분석 결과를 가져와야 함
      const bedtimeHours = sleepData.map(item => {
        const startTime = new Date(item.start_time);
        return startTime.getHours() + startTime.getMinutes() / 60;
      });
      
      const waketimeHours = sleepData.map(item => {
        const endTime = new Date(item.end_time);
        return endTime.getHours() + endTime.getMinutes() / 60;
      });
      
      const avgBedtimeHour = bedtimeHours.reduce((sum, hour) => sum + hour, 0) / bedtimeHours.length;
      const avgWaketimeHour = waketimeHours.reduce((sum, hour) => sum + hour, 0) / waketimeHours.length;
      
      const bedtimeHour = Math.floor(avgBedtimeHour);
      const bedtimeMinute = Math.floor((avgBedtimeHour - bedtimeHour) * 60);
      
      const waketimeHour = Math.floor(avgWaketimeHour);
      const waketimeMinute = Math.floor((avgWaketimeHour - waketimeHour) * 60);
      
      setOptimalSleepTime({
        bedtime: `${bedtimeHour.toString().padStart(2, '0')}:${bedtimeMinute.toString().padStart(2, '0')}`,
        waketime: `${waketimeHour.toString().padStart(2, '0')}:${waketimeMinute.toString().padStart(2, '0')}`,
        duration: `${Math.floor(avgDuration / 60)}시간 ${Math.floor(avgDuration % 60)}분`
      });
      
      // 트렌드 계산 (간단한 예시)
      // 실제로는 백엔드 API를 통해 분석 결과를 가져와야 함
      if (sleepData.length >= 7) {
        const recentData = sleepData.slice(0, 7);
        const olderData = sleepData.slice(7, 14);
        
        if (olderData.length > 0) {
          const recentAvg = recentData.reduce((sum, item) => sum + item.duration, 0) / recentData.length;
          const olderAvg = olderData.reduce((sum, item) => sum + item.duration, 0) / olderData.length;
          
          const weeklyChange = recentAvg - olderAvg;
          
          setSleepTrend({
            weeklyChange,
            monthlyChange: weeklyChange * 4, // 간단한 예시
            trend: weeklyChange > 10 ? 'improving' : weeklyChange < -10 ? 'declining' : 'stable'
          });
        }
      }
    }
  }, [sleepData]);

  // 데이터가 없는 경우
  if (!sleepData || sleepData.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">수면 데이터 시각화</h2>
        <div className="p-8 text-center">
          <p className="text-gray-500">수면 데이터가 없습니다.</p>
          <button 
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            onClick={onRefresh}
          >
            데이터 새로고침
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 수면 요약 섹션 */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">수면 요약</h2>
          <button 
            className="px-3 py-1 bg-blue-100 text-blue-600 rounded hover:bg-blue-200 transition-colors text-sm"
            onClick={onRefresh}
          >
            새로고침
          </button>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded">
            <p className="text-sm text-gray-600">평균 수면 시간</p>
            <p className="text-xl font-semibold">
              {Math.floor(summaryData.averageDuration / 60)}시간 {Math.floor(summaryData.averageDuration % 60)}분
            </p>
          </div>
          
          <div className="bg-green-50 p-4 rounded">
            <p className="text-sm text-gray-600">수면 효율</p>
            <p className="text-xl font-semibold">{Math.round(summaryData.averageEfficiency)}%</p>
          </div>
          
          <div className="bg-purple-50 p-4 rounded">
            <p className="text-sm text-gray-600">최적 취침 시간</p>
            <p className="text-xl font-semibold">{optimalSleepTime.bedtime}</p>
          </div>
          
          <div className="bg-indigo-50 p-4 rounded">
            <p className="text-sm text-gray-600">최적 기상 시간</p>
            <p className="text-xl font-semibold">{optimalSleepTime.waketime}</p>
          </div>
        </div>
      </div>
      
      {/* 수면 단계 섹션 */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">수면 단계</h2>
        <div className="h-64 flex items-center justify-center bg-gray-100 rounded mb-4">
          <p className="text-gray-500">수면 단계 차트가 표시됩니다</p>
          {/* 실제 구현 시 차트 라이브러리 사용
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={[
                  { name: '깊은 수면', value: summaryData.deepSleepPercentage },
                  { name: '얕은 수면', value: summaryData.lightSleepPercentage },
                  { name: 'REM 수면', value: summaryData.remSleepPercentage },
                  { name: '깨어있음', value: summaryData.awakePercentage },
                ]}
                cx="50%"
                cy="50%"
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              />
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
          */}
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-3 border border-blue-200 rounded">
            <p className="text-sm text-gray-600">깊은 수면</p>
            <p className="font-semibold">{Math.round(summaryData.deepSleepPercentage)}%</p>
          </div>
          
          <div className="p-3 border border-green-200 rounded">
            <p className="text-sm text-gray-600">얕은 수면</p>
            <p className="font-semibold">{Math.round(summaryData.lightSleepPercentage)}%</p>
          </div>
          
          <div className="p-3 border border-purple-200 rounded">
            <p className="text-sm text-gray-600">REM 수면</p>
            <p className="font-semibold">{Math.round(summaryData.remSleepPercentage)}%</p>
          </div>
          
          <div className="p-3 border border-gray-200 rounded">
            <p className="text-sm text-gray-600">깨어있음</p>
            <p className="font-semibold">{Math.round(summaryData.awakePercentage)}%</p>
          </div>
        </div>
      </div>
      
      {/* 수면 트렌드 섹션 */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">수면 트렌드</h2>
        <div className="h-64 flex items-center justify-center bg-gray-100 rounded mb-4">
          <p className="text-gray-500">수면 시간 트렌드 차트가 표시됩니다</p>
          {/* 실제 구현 시 차트 라이브러리 사용
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={sleepData.map(item => ({
              date: new Date(item.start_time).toLocaleDateString(),
              duration: item.duration / 60
            }))}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="duration" stroke="#8884d8" name="수면 시간 (시간)" />
            </LineChart>
          </ResponsiveContainer>
          */}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-gray-50 rounded">
            <p className="text-sm text-gray-600">주간 변화</p>
            <p className={`text-lg font-semibold ${sleepTrend.weeklyChange > 0 ? 'text-green-600' : sleepTrend.weeklyChange < 0 ? 'text-red-600' : 'text-gray-600'}`}>
              {sleepTrend.weeklyChange > 0 ? '+' : ''}{Math.round(sleepTrend.weeklyChange)}분
            </p>
          </div>
          
          <div className="p-4 bg-gray-50 rounded">
            <p className="text-sm text-gray-600">월간 변화</p>
            <p className={`text-lg font-semibold ${sleepTrend.monthlyChange > 0 ? 'text-green-600' : sleepTrend.monthlyChange < 0 ? 'text-red-600' : 'text-gray-600'}`}>
              {sleepTrend.monthlyChange > 0 ? '+' : ''}{Math.round(sleepTrend.monthlyChange)}분
            </p>
          </div>
          
          <div className="p-4 bg-gray-50 rounded">
            <p className="text-sm text-gray-600">트렌드</p>
            <p className={`text-lg font-semibold ${
              sleepTrend.trend === 'improving' ? 'text-green-600' : 
              sleepTrend.trend === 'declining' ? 'text-red-600' : 
              'text-gray-600'
            }`}>
              {sleepTrend.trend === 'improving' ? '개선 중' : 
               sleepTrend.trend === 'declining' ? '감소 중' : 
               '안정적'}
            </p>
          </div>
        </div>
      </div>
      
      {/* 상관관계 섹션 */}
      {(activityData && activityData.length > 0) || (stressData && stressData.length > 0) ? (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">수면과 다른 지표의 상관관계</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {activityData && activityData.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-3">활동량과 수면</h3>
                <div className="h-48 flex items-center justify-center bg-gray-100 rounded mb-3">
                  <p className="text-gray-500">활동량-수면 상관관계 차트가 표시됩니다</p>
                </div>
                <p className="text-sm text-gray-600">
                  활동량이 많은 날에는 수면의 질이 향상되는 경향이 있습니다.
                </p>
              </div>
            )}
            
            {stressData && stressData.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-3">스트레스와 수면</h3>
                <div className="h-48 flex items-center justify-center bg-gray-100 rounded mb-3">
                  <p className="text-gray-500">스트레스-수면 상관관계 차트가 표시됩니다</p>
                </div>
                <p className="text-sm text-gray-600">
                  스트레스 지수가 높은 날에는 수면의 질이 저하되는 경향이 있습니다.
                </p>
              </div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default SleepDataVisualizer;
