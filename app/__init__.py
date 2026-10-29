"""Small inventory service used as the CI/CD testbed."""
from .config import load_config
from .inventory import Inventory
from .server import create_server