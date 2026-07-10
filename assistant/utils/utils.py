import datetime
from pathlib import Path

def ensure_dir(path: Path) -> Path:
    """Ensure directory exists, return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path

def timestamp() -> str:
    """Current ISO timestamp."""
    return datetime.now().isoformat()
