import React from 'react';
import ReactDOM from 'react-dom';
import QueueStatus from './routes/queue';

const App = () => {
    const rideIds = ['ride1', 'ride2', 'ride3']; // 모니터링할 놀이기구 ID 목록

    return (
        <div>
            <h1>놀이기구 줄서기 모니터링 대시보드</h1>
            {rideIds.map(rideId => (
                <QueueStatus key={rideId} rideId={rideId} />
            ))}
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('root'));
