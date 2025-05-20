/**
 * Health Connect API 클라이언트
 * 백엔드 API와 통신하여 수면, 활동, 스트레스 데이터를 가져옵니다.
 */

// API 기본 URL
const API_BASE_URL = 'http://localhost:5000/api';

// 날짜 범위 타입 정의
interface DateRange {
  startDate?: string;
  endDate?: string;
}

// 수면 데이터 타입 정의
interface SleepData {
  id: string;
  start_time: string;
  end_time: string;
  duration: number;
  efficiency: number;
  stages: {
    deep: number;
    light: number;
    rem: number;
    awake: number;
  };
}

// 활동 데이터 타입 정의
interface ActivityData {
  id: string;
  date: string;
  steps: number;
  active_minutes: number;
  calories: number;
}

// 스트레스 데이터 타입 정의
interface StressData {
  id: string;
  date: string;
  average_score: number;
  max_score: number;
  min_score: number;
}

// 사용자 피드백 타입 정의
interface UserFeedback {
  date: string;
  sleep_satisfaction: number;
  morning_condition: number;
  notes?: string;
}

// API 응답 타입 정의
interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

/**
 * 수면 데이터를 가져오는 함수
 * @param dateRange 날짜 범위 (선택)
 * @returns 수면 데이터 배열
 */
export const fetchSleepData = async (dateRange?: DateRange): Promise<SleepData[]> => {
  try {
    let url = `${API_BASE_URL}/health_connect/sleep`;
    
    // 날짜 범위가 제공된 경우 쿼리 파라미터 추가
    if (dateRange) {
      const params = new URLSearchParams();
      if (dateRange.startDate) params.append('start_date', dateRange.startDate);
      if (dateRange.endDate) params.append('end_date', dateRange.endDate);
      url += `?${params.toString()}`;
    }
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`API 요청 실패: ${response.status}`);
    }
    
    const result: ApiResponse<SleepData[]> = await response.json();
    
    if (!result.success) {
      throw new Error(result.message || '데이터를 가져오는데 실패했습니다.');
    }
    
    return result.data;
  } catch (error) {
    console.error('수면 데이터 가져오기 오류:', error);
    return [];
  }
};

/**
 * 활동 데이터를 가져오는 함수
 * @param dateRange 날짜 범위 (선택)
 * @returns 활동 데이터 배열
 */
export const fetchActivityData = async (dateRange?: DateRange): Promise<ActivityData[]> => {
  try {
    let url = `${API_BASE_URL}/health_connect/activity`;
    
    // 날짜 범위가 제공된 경우 쿼리 파라미터 추가
    if (dateRange) {
      const params = new URLSearchParams();
      if (dateRange.startDate) params.append('start_date', dateRange.startDate);
      if (dateRange.endDate) params.append('end_date', dateRange.endDate);
      url += `?${params.toString()}`;
    }
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`API 요청 실패: ${response.status}`);
    }
    
    const result: ApiResponse<ActivityData[]> = await response.json();
    
    if (!result.success) {
      throw new Error(result.message || '데이터를 가져오는데 실패했습니다.');
    }
    
    return result.data;
  } catch (error) {
    console.error('활동 데이터 가져오기 오류:', error);
    return [];
  }
};

/**
 * 스트레스 데이터를 가져오는 함수
 * @param dateRange 날짜 범위 (선택)
 * @returns 스트레스 데이터 배열
 */
export const fetchStressData = async (dateRange?: DateRange): Promise<StressData[]> => {
  try {
    let url = `${API_BASE_URL}/health_connect/stress`;
    
    // 날짜 범위가 제공된 경우 쿼리 파라미터 추가
    if (dateRange) {
      const params = new URLSearchParams();
      if (dateRange.startDate) params.append('start_date', dateRange.startDate);
      if (dateRange.endDate) params.append('end_date', dateRange.endDate);
      url += `?${params.toString()}`;
    }
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`API 요청 실패: ${response.status}`);
    }
    
    const result: ApiResponse<StressData[]> = await response.json();
    
    if (!result.success) {
      throw new Error(result.message || '데이터를 가져오는데 실패했습니다.');
    }
    
    return result.data;
  } catch (error) {
    console.error('스트레스 데이터 가져오기 오류:', error);
    return [];
  }
};

/**
 * Health Connect 연결 상태를 확인하는 함수
 * @returns 연결 상태 정보
 */
export const checkConnectionStatus = async (): Promise<{
  connected: boolean;
  permissions: {
    sleep: boolean;
    activity: boolean;
    stress: boolean;
  };
  last_sync: string;
}> => {
  try {
    const url = `${API_BASE_URL}/health_connect/status`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`API 요청 실패: ${response.status}`);
    }
    
    const result = await response.json();
    
    if (!result.success) {
      throw new Error(result.message || '상태를 확인하는데 실패했습니다.');
    }
    
    return result;
  } catch (error) {
    console.error('연결 상태 확인 오류:', error);
    return {
      connected: false,
      permissions: {
        sleep: false,
        activity: false,
        stress: false
      },
      last_sync: new Date().toISOString()
    };
  }
};

/**
 * 사용자 피드백을 저장하는 함수
 * @param feedback 사용자 피드백 데이터
 * @returns 저장 결과
 */
export const saveUserFeedback = async (feedback: UserFeedback): Promise<boolean> => {
  try {
    const url = `${API_BASE_URL}/health_connect/feedback`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(feedback)
    });
    
    if (!response.ok) {
      throw new Error(`API 요청 실패: ${response.status}`);
    }
    
    const result = await response.json();
    
    return result.success;
  } catch (error) {
    console.error('피드백 저장 오류:', error);
    return false;
  }
};
