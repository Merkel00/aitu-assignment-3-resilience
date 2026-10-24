"""Minimal standard-library demo; deliberately synthetic and stateless."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
import json, os
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.path = urlsplit(self.path).path
        if self.path not in ('/healthz','/readyz','/register'):
            self.send_error(404); return
        if self.path == '/readyz' and os.getenv('DB_AVAILABLE','true').lower() != 'true':
            status, payload = 503, {'ready': False, 'reason': 'database unavailable'}
        elif self.path == '/register' and os.getenv('DB_AVAILABLE','true').lower() != 'true':
            status, payload = 503, {'error': 'database unavailable'}
        else:
            status, payload = 200, {'path': self.path, 'status': 'ok', 'demo': True}
        body = json.dumps(payload).encode()
        self.send_response(status); self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0',8080),Handler).serve_forever()
