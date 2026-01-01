"""Configuration parameters for wikirss."""

from pathlib import Path

from dotenv import dotenv_values
from loguru import logger

# Secrets
user_agent = dotenv_values().get("USER_AGENT")
if user_agent is None:
    logger.warning(
        "USER_AGENT not found in .env file. Wikipedia will block your requests."
    )

# URLs
WIKI_URL = "https://en.wikipedia.org"
MAIN_PAGE_URL = f"{WIKI_URL}/wiki/Main_Page"
MAIN_PAGE_HISTORY_URL = (
    f"{WIKI_URL}/w/index.php?title=Main_Page&action=history"
)

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[2]
"""The project root directory. All other directories should be defined relative to this root."""

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

LOGS_DIR = PROJ_ROOT / "logs"

# If tqdm is installed, configure loguru with tqdm.write
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except (ModuleNotFoundError, ValueError):
    pass
