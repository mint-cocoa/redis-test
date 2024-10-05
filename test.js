import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

// 기본 URL 설정
const BASE_URL = 'http://localhost:8001';

// 놀이기구와 사용자 ID를 생성하는 도구
const rides = ['roller-coaster', 'ferris-wheel', 'bumper-cars', 'carousel', 'log-flume'];
const getRandomRideId = () => rides[randomIntBetween(0, rides.length - 1)];
const getRandomUserId = () => `user_${randomIntBetween(1, 1000)}`;

export const options = {
  vus: 10,          // 가상 사용자의 수
  duration: '50s',  // 테스트 지속 시간
};

// 줄 서기 요청 (POST /enqueue)
export function enqueue() {
  const rideId = getRandomRideId();
  const userId = getRandomUserId();
  
  const payload = JSON.stringify({ rideId, userId });
  const params = { headers: { 'Content-Type': 'application/json' } };
  
  const res = http.post(`${BASE_URL}/enqueue`, payload, params);
  
  check(res, {
    '줄 서기 성공': (r) => r.status === 200,
  });
  
  sleep(1);
}

// 줄에서 제거 요청 (POST /dequeue/{rideId})
export function dequeue() {
  const rideId = getRandomRideId();
  
  const res = http.post(`${BASE_URL}/dequeue/${rideId}`);
  
  check(res, {
    '줄에서 제거 성공': (r) => r.status === 200,
  });
  
  sleep(1);
}

// 특정 사용자의 대기열 위치 확인 (GET /position/{rideId}/{userId})
export function getPosition() {
  const rideId = getRandomRideId();
  const userId = getRandomUserId();
  
  const res = http.get(`${BASE_URL}/position/${rideId}/${userId}`);
  
  check(res, {
    '대기열 위치 확인 성공': (r) => r.status === 200,
  });
  
  sleep(1);
}

// 모든 대기열 상태 확인 (GET /all-queues)
export function getAllQueues() {
  const res = http.get(`${BASE_URL}/all-queues`);
  
  check(res, {
    '모든 대기열 상태 확인 성공': (r) => r.status === 200,
  });
  
  sleep(1);
}

export default function () {
  // 각 엔드포인트를 랜덤하게 호출
  const actions = [enqueue, dequeue, getPosition, getAllQueues];
  const action = actions[randomIntBetween(0, actions.length - 1)];
  action();
}
