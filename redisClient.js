const { createClient } = require('redis');

const client = createClient({
  url: process.env.REDIS_URL || 'redis://redis:6379'
});

client.on('error', (err) => {
  console.error('Redis 클라이언트 에러:', err);
});

(async () => {
  await client.connect();
})();

module.exports = client;
