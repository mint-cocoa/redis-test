const express = require('express');
const router = express.Router();
const redisClient = require('../redisClient');

// 놀이기구에 사람 추가
router.post('/enqueue', async (req, res) => {
  const { rideId, userId } = req.body;
  if (!rideId || !userId) {
    return res.status(400).json({ message: 'rideId와 userId가 필요합니다.' });
  }
  
  try {
    await redisClient.rPush(`queue:${rideId}`, userId);
    const position = await redisClient.lPos(`queue:${rideId}`, userId, { rank: 0 }) + 1;
    res.status(200).json({ message: '줄에 추가되었습니다.', position });
  } catch (error) {
    console.error('enqueue 에러:', error);
    res.status(500).json({ message: '서버 에러' });
  }
});

// 놀이기구에서 사람 제거
router.post('/dequeue', async (req, res) => {
  const { rideId } = req.body;
  if (!rideId) {
    return res.status(400).json({ message: 'rideId가 필요합니다.' });
  }

  try {
    const userId = await redisClient.lPop(`queue:${rideId}`);
    if (userId) {
      res.status(200).json({ message: '줄에서 제거되었습니다.', userId });
    } else {
      res.status(200).json({ message: '줄에 사람이 없습니다.' });
    }
  } catch (error) {
    console.error('dequeue 에러:', error);
    res.status(500).json({ message: '서버 에러' });
  }
});

// 특정 놀이기구의 줄 상태 조회
router.get('/status/:rideId', async (req, res) => {
  const { rideId } = req.params;

  try {
    const queue = await redisClient.lRange(`queue:${rideId}`, 0, -1);
    res.status(200).json({ rideId, queue });
  } catch (error) {
    console.error('status 조회 에러:', error);
    res.status(500).json({ message: '서버 에러' });
  }
});

module.exports = router;
