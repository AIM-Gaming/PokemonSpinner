import sys
from pathlib import Path

def resource_path(name: str) -> str:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return str(base / name)