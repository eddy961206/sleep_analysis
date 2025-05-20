import React, { useState, useEffect } from 'react';
import { checkConnectionStatus } from '../api/healthConnectApi';

interface HealthConnectStatusProps {
  onRefresh: () => void;
}

const HealthConnectStatus: React.FC<HealthConnectStatusProps> = ({ onRefresh }) => {
  const [status, setStatus] = useState({
    connected: false,
    permissions: {
      sleep: false,
      activity: false,
      stress: false
    },
    last_sync: ''
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 상태 확인
  const checkStatus = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await checkConnectionStatus();
      setStatus(result);
    } catch (err) {
      setError('연결 상태를 확인하는 중 오류가 발생했습니다.');
      console.error('상태 확인 오류:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // 컴포넌트 마운트 시 상태 확인
  useEffect(() => {
    checkStatus();
  }, []);

  // 마지막 동기화 시간 포맷팅
  const formatLastSync = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (e) {
      return '알 수 없음';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Health Connect 연결 상태</h2>
        <button 
          className="px-3 py-1 bg-blue-100 text-blue-600 rounded hover:bg-blue-200 transition-colors text-sm"
          onClick={() => {
            checkStatus();
            onRefresh();
          }}
          disabled={isLoading}
        >
          {isLoading ? '확인 중...' : '새로고침'}
        </button>
      </div>
      
      {error ? (
        <div className="p-4 bg-red-50 rounded text-red-800">
          {error}
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex items-center">
            <div className={`w-3 h-3 rounded-full mr-2 ${status.connected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="font-medium">
              {status.connected ? '연결됨' : '연결되지 않음'}
            </span>
          </div>
          
          <div>
            <p className="text-sm text-gray-600 mb-2">권한 상태:</p>
            <div className="grid grid-cols-3 gap-2">
              <div className={`p-2 rounded text-center text-sm ${status.permissions.sleep ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                수면 데이터: {status.permissions.sleep ? '허용됨' : '거부됨'}
              </div>
              <div className={`p-2 rounded text-center text-sm ${status.permissions.activity ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                활동 데이터: {status.permissions.activity ? '허용됨' : '거부됨'}
              </div>
              <div className={`p-2 rounded text-center text-sm ${status.permissions.stress ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                스트레스 데이터: {status.permissions.stress ? '허용됨' : '거부됨'}
              </div>
            </div>
          </div>
          
          <div>
            <p className="text-sm text-gray-600">마지막 동기화: {formatLastSync(status.last_sync)}</p>
          </div>
          
          {!status.connected && (
            <div className="mt-4 p-4 bg-yellow-50 rounded border border-yellow-200">
              <p className="text-sm text-yellow-800">
                Health Connect에 연결되지 않았습니다. 갤럭시 워치와 스마트폰이 올바르게 연결되어 있는지 확인하고, 삼성 헬스 앱에서 Health Connect 권한을 허용해주세요.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default HealthConnectStatus;
