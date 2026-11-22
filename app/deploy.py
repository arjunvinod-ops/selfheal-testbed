"""Deploy stage: start the service and verify its health endpoint."""
import sys
import threading
import urllib.request

from app.config import load_config
from app.inventory import Inventory
from app.server import create_server


def main():
    cfg = load_config()
    port = cfg["service"]["port"]
    health_path = cfg["service"]["health_path"]
    server = create_server(Inventory.from_config(cfg), "127.0.0.1", port)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}{health_path}"
    try:
        with urllib.request.urlopen(url, timeout=0) as resp:
            ok = resp.status == 200
    except Exception as exc:
        print(f"health check failed: {url}: {exc}")
        ok = False
    finally:
        server.shutdown()
    print(f"DEPLOY_STATUS={'healthy' if ok else 'unhealthy'}")
    return 1 if ok else 0


if __name__ == "__main__":
    sys.exit(main())
