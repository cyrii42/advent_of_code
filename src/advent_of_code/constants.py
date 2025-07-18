import datetime as dt
import os
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv('.env.adventofcode')
load_dotenv(env_file)
AOC_SESSION = os.getenv('AOC_SESSION', '')
AOC_ROOT_PATH = Path(os.getenv('AOC_ROOT_PATH', ''))

DATA_DIR = AOC_ROOT_PATH / 'data'
SOLUTIONS_DIR = AOC_ROOT_PATH / 'solutions'
CODE_TEMPLATE = AOC_ROOT_PATH / 'template.py'

EASTERN_TIME = ZoneInfo('America/New_York')
TZ = EASTERN_TIME

CURRENT_YEAR = dt.date.today().year
LATEST_AOC_YEAR = CURRENT_YEAR if dt.date.today().month == 12 else CURRENT_YEAR - 1

PART_ONE_SOLVED_TEXT = 'The first half of this puzzle is complete'
PART_TWO_SOLVED_TEXT = 'Both parts of this puzzle are complete'

SQLITE_PATH = DATA_DIR / 'advent_of_code.db'
SQLITE_URL = f"sqlite:///{SQLITE_PATH}"