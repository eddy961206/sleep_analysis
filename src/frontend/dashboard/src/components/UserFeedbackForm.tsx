import React, { useState } from 'react';
import { saveUserFeedback } from '../api/healthConnectApi';

interface UserFeedbackFormProps {
  onFeedbackSubmit: (feedback: {
    sleep_satisfaction: number;
    morning_condition: number;
    notes?: string;
  }) => void;
}

const UserFeedbackForm: React.FC<UserFeedbackFormProps> = ({ onFeedbackSubmit }) => {
  const [sleepSatisfaction, setSleepSatisfaction] = useState<number | null>(null);
  const [morningCondition, setMorningCondition] = useState<number | null>(null);
  const [notes, setNotes] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (sleepSatisfaction === null || morningCondition === null) {
      alert('수면 만족도와 기상 시 컨디션을 모두 선택해주세요.');
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      await onFeedbackSubmit({
        sleep_satisfaction: sleepSatisfaction,
        morning_condition: morningCondition,
        notes: notes.trim() || undefined
      });
      
      // 성공적으로 제출됨
      setSubmitSuccess(true);
      
      // 폼 초기화
      setSleepSatisfaction(null);
      setMorningCondition(null);
      setNotes('');
      
      // 3초 후 성공 메시지 숨기기
      setTimeout(() => {
        setSubmitSuccess(false);
      }, 3000);
    } catch (error) {
      console.error('피드백 제출 오류:', error);
      alert('피드백을 저장하는 중 오류가 발생했습니다.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">오늘의 컨디션 평가</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* 수면 만족도 */}
        <div>
          <label className="block text-gray-700 mb-2 font-medium">수면 만족도</label>
          <div className="flex space-x-4">
            {[1, 2, 3, 4, 5].map((rating) => (
              <button
                key={rating}
                type="button"
                className={`w-12 h-12 rounded-full flex items-center justify-center transition-colors ${
                  sleepSatisfaction === rating
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 hover:bg-blue-100'
                }`}
                onClick={() => setSleepSatisfaction(rating)}
              >
                {rating}
              </button>
            ))}
          </div>
          <div className="flex justify-between mt-2 text-xs text-gray-500">
            <span>매우 불만족</span>
            <span>매우 만족</span>
          </div>
        </div>
        
        {/* 기상 시 컨디션 */}
        <div>
          <label className="block text-gray-700 mb-2 font-medium">기상 시 컨디션</label>
          <div className="flex space-x-4">
            {[1, 2, 3, 4, 5].map((rating) => (
              <button
                key={rating}
                type="button"
                className={`w-12 h-12 rounded-full flex items-center justify-center transition-colors ${
                  morningCondition === rating
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-200 hover:bg-green-100'
                }`}
                onClick={() => setMorningCondition(rating)}
              >
                {rating}
              </button>
            ))}
          </div>
          <div className="flex justify-between mt-2 text-xs text-gray-500">
            <span>매우 피곤함</span>
            <span>매우 상쾌함</span>
          </div>
        </div>
        
        {/* 특이사항 */}
        <div>
          <label className="block text-gray-700 mb-2 font-medium">특이사항 (선택)</label>
          <textarea
            className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={3}
            placeholder="수면에 영향을 미친 요소가 있다면 기록해주세요. (예: 카페인 섭취, 운동, 스트레스 등)"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          ></textarea>
        </div>
        
        {/* 제출 버튼 */}
        <div>
          <button
            type="submit"
            className={`w-full py-3 px-4 rounded font-medium transition-colors ${
              isSubmitting
                ? 'bg-gray-400 text-white cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
            disabled={isSubmitting}
          >
            {isSubmitting ? '저장 중...' : '피드백 저장하기'}
          </button>
        </div>
        
        {/* 성공 메시지 */}
        {submitSuccess && (
          <div className="p-3 bg-green-100 text-green-700 rounded text-center">
            피드백이 성공적으로 저장되었습니다!
          </div>
        )}
      </form>
    </div>
  );
};

export default UserFeedbackForm;
