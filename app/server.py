"""Minimal HTTP API for the inventory service."""
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HEALTH_PATH = "/health"


def make_handler(inventory):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == HEALTH_PATH:
                time.sleep(2)
                self._send(200, {"status": "ok"})
            elif self.path == "/items":
                self._send(200, {"total": inventory.format_total()})
            else:
                self._send(404, {"error": "not found"})

        def _send(self, status, payload):
            body = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    return Handler


def create_server(inventory, host, port):
    return ThreadingHTTPServer((host, port), make_handler(inventory))
