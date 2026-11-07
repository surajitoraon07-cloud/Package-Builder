"""Package Builder server (Python 3 standard library only).
Run:  python server.py     then open http://127.0.0.1:8000
Packages are stored in the SQLite database file 'packages.db' next to this file.
Use  python server.py lan  to let other computers on your Wi-Fi/office network open it."""
import glob, json, os, re, sqlite3, sys, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(ROOT, 'packages.db')

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()) or 'pkg'

def q(sql, args=()):
    c = sqlite3.connect(DB)
    try:
        with c:
            return c.execute(sql, args).fetchall()
    finally:
        c.close()

def put(name, html, replace=True):
    q('INSERT OR ' + ('REPLACE' if replace else 'IGNORE') +
      " INTO packages(slug, name, html, updated_at) VALUES(?, ?, ?, datetime('now'))",
      (slug(name), name, html))

def init():
    q('CREATE TABLE IF NOT EXISTS packages (slug TEXT PRIMARY KEY, name TEXT NOT NULL, '
      'html TEXT NOT NULL, updated_at TEXT NOT NULL)')
    # one-time import of packages saved as .json files by the older version
    for f in glob.glob(os.path.join(ROOT, 'packages', '*.json')):
        try:
            with open(f, encoding='utf-8') as fh:
                d = json.load(fh)
            put(d['name'], d['html'], replace=False)
            os.replace(f, f + '.imported')
        except Exception:
            pass

class H(BaseHTTPRequestHandler):
    def _send(self, code, body=b'', ctype='application/json'):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/api/packages':
            rows = q('SELECT name, html FROM packages ORDER BY name')
            return self._send(200, json.dumps([{'name': n, 'html': h} for n, h in rows]).encode())
        if self.path in ('/', '/index.html'):
            with open(os.path.join(ROOT, 'index.html'), 'rb') as fh:
                return self._send(200, fh.read(), 'text/html; charset=utf-8')
        self._send(404)

    def do_POST(self):
        if self.path != '/api/packages':
            return self._send(404)
        try:
            d = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
            name, html = str(d['name']).strip(), str(d['html'])
            if not name or not html:
                raise ValueError
        except Exception:
            return self._send(400)
        put(name, html)
        self._send(200, b'{}')

    def do_DELETE(self):
        m = re.match(r'^/api/packages/([^/]+)$', self.path)
        if not m:
            return self._send(404)
        q('DELETE FROM packages WHERE slug = ?', (slug(m.group(1)),))
        self._send(200, b'{}')

    def log_message(self, *a):
        pass

if __name__ == '__main__':
    init()
    host = '8000' if 'lan' in sys.argv else '127.0.0.1'
    srv = ThreadingHTTPServer((host, 8000), H)
    print('Package Builder running at http://127.0.0.1:8000  (Ctrl+C to stop)')
    if host == '127.0.0.1':
        threading.Timer(1, lambda: webbrowser.open('http://127.0.0.1:8000')).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
