const http = require('http');
const fs = require('fs');
const path = require('path');

const dir = '/Users/valeriejimenez/Desktop/Claude-Code-Work/portfolio';
const port = 4400;

const mimeTypes = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
};

http.createServer((req, res) => {
  // Strip query strings (e.g. ?v=2 cache busters) so local matches Netlify behavior
  const cleanUrl = (req.url === '/' ? '/index.html' : req.url).split('?')[0];
  let filePath = path.join(dir, cleanUrl);
  const ext = path.extname(filePath).toLowerCase();
  const contentType = mimeTypes[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
}).listen(port, () => console.log(`Serving on http://localhost:${port}`));
