import React, { useEffect, useState } from 'react';
import axios from 'axios';

const QueueStatus = ({ rideId }) => {
    const [queue, setQueue] = useState([]);

    useEffect(() => {
        const fetchQueueStatus = () => {
            axios.get(`/status/${rideId}`)
                .then(response => {
                    setQueue(response.data.queue);
                })
                .catch(error => {
                    console.error('줄서기 상태를 불러오는 데 실패했습니다:', error);
                });
        };

        // 초기 데이터 로드
        fetchQueueStatus();

        // 5초마다 상태 업데이트
        const interval = setInterval(fetchQueueStatus, 5000);

        // 컴포넌트 언마운트 시 인터벌 클리어
        return () => clearInterval(interval);
    }, [rideId]);

    return (
        <div>
            <h2>{rideId}의 줄서기 상태</h2>
            <ul>
                {queue.map((userId, index) => (
                    <li key={index}>{index + 1}. 사용자 ID: {userId}</li>
                ))}
            </ul>
        </div>
    );
};

export default QueueStatus;
