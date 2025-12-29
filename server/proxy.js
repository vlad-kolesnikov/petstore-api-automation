const express = require('express');
const cors = require('cors');
const { createProxyMiddleware } = require('http-proxy-middleware');
const morgan = require('morgan');

const app = express();
const PORT = 3000;
const TARGET_API = 'https://petstore.swagger.io/v2';
const API_KEY = 'special-key';

app.use(cors());
app.use(morgan('dev'));

app.use('/', createProxyMiddleware({
  target: TARGET_API,
  changeOrigin: true,
  onProxyReq: (proxyReq, req, res) => {
    proxyReq.setHeader('api_key', API_KEY);
    console.log(`[PROXY] ${req.method} ${req.path}`);
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log(`[RESPONSE] ${proxyRes.statusCode} ${req.method} ${req.path}`);
  },
  onError: (err, req, res) => {
    console.error('[PROXY ERROR]', err.message);
    res.status(500).json({
      error: 'Proxy error',
      message: err.message
    });
  }
}));

app.listen(PORT, () => {
  console.log(`\n🚀 Petstore API Proxy running on http://localhost:${PORT}`);
  console.log(`📡 Proxying to: ${TARGET_API}`);
  console.log(`🔑 API Key: ${API_KEY}\n`);
});
