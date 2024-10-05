const express = require('express');
const bodyParser = require('body-parser');
const queueRoutes = require('./routes/queue');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());

app.use('/queue', queueRoutes);

// 기본 라우트
app.get('/', (req, res) => {
  res.send('놀이기구 줄서기 서비스에 오신 것을 환영합니다!');
});

app.listen(PORT, () => {
  console.log(`서버가 포트 ${PORT}에서 실행 중입니다.`);
});
