import React, { useState, useEffect } from 'react';
import SleepDataVisualizer from './SleepDataVisualizer';
import UserFeedbackForm from './UserFeedbackForm';

interface SleepDashboardProps {
  sleepData: any[];
  activityData: any[];
  stressData: any[];
  onFeedbackSubmit: (feedback: {
    sleep_satisfaction: number;
    morning_condition: number;
    notes?: string;
  }) => void;
  onRefresh: () => void;
}

const SleepDashboard: React.FC<SleepDashboardProps> = ({
  sleepData,
  activityData,
  stressData,
  onFeedbackSubmit,
  onRefresh
}) => {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div>
      {/* 탭 네비게이션 */}
      <div className="mb-6 border-b border-gray-200">
        <nav className="-mb-px flex">
          <button
            className={`py-4 px-6 font-medium text-sm ${
              activeTab === 'dashboard'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
            onClick={() => setActiveTab('dashboard')}
          >
            대시보드
          </button>
          <button
            className={`py-4 px-6 font-medium text-sm ${
              activeTab === 'feedback'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
            onClick={() => setActiveTab('feedback')}
          >
            컨디션 평가
          </button>
        </nav>
      </div>

      {/* 탭 콘텐츠 */}
      <div>
        {activeTab === 'dashboard' && (
          <SleepDataVisualizer
            sleepData={sleepData}
            activityData={activityData}
            stressData={stressData}
            onRefresh={onRefresh}
          />
        )}
        
        {activeTab === 'feedback' && (
          <UserFeedbackForm onFeedbackSubmit={onFeedbackSubmit} />
        )}
      </div>
    </div>
  );
};

export default SleepDashboard;
