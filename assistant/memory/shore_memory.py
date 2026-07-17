import json
import logging
import threading
import uuid

from pathlib import Path
from typing import Any

from assistant.memory.storage import MemoryStorage

logger = logging.getLogger(__name__)

class ShortMemoryStorage(MemoryStorage):
    """File-based memory storage provider."""

    def __init__(self):
        """user memory: `{base_dir}/users/{user_id}/short_memory.json`."""
        self.repo_root = Path(__file__).parents[2]

    def get_memory_file_path(self, user_id: str) -> Path:
        """user memory: `{base_dir}/users/{user_id}/memory.json`."""
        return self.repo_root / "users" / user_id / "short_memory.json"

    def load_memory_from_file(self, user_id: str) -> str | None:
        """Load memory data from file."""
        file_path = self.get_memory_file_path(user_id=user_id)

        if not file_path.exists():
            return None

        try:
            with open(file_path, encoding="utf-8") as f:
                data = f.read()
            return data
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("Failed to load memory file: %s", e)
            return None

    @staticmethod
    def _cache_key(user_id: str) -> str:
        return user_id

    def load(self, user_id: str) -> str|None:
        """Load memory data (cached with file modification time check)."""

        memory_data = self.load_memory_from_file(user_id=user_id)

        return memory_data

    def reload(self, user_id: str) -> dict[str, Any]:
       pass

    def save(self, memory_data: dict[str, Any] | str, user_id: str) -> bool:
        """Save memory data to file and update cache."""
        file_path = self.get_memory_file_path(user_id=user_id)

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = file_path.with_suffix(f".{uuid.uuid4().hex}.tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(memory_data)
                # json.dump(memory_data, f, indent=2, ensure_ascii=False)

            temp_path.replace(file_path)

            logger.info("Short memory saved to %s", file_path)
            return True
        except OSError as e:
            logger.error("Failed to save short memory file: %s", e)
            return False

    def delete(self, user_id: str) -> bool:
        pass


_storage_instance: MemoryStorage | None = None
_storage_lock = threading.Lock()

def get_short_memory_storage() -> MemoryStorage:
    global _storage_instance
    if _storage_instance is not None:
        return _storage_instance

    _storage_instance = ShortMemoryStorage()

    return _storage_instance
