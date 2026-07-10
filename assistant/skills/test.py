import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

from assistant.memory.storage import utc_now_iso_z

BUILTIN_SKILLS_DIR = Path(__file__).parents[2] / "skills"
print(BUILTIN_SKILLS_DIR)

