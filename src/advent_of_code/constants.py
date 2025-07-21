import datetime as dt
import os
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv('.env.adventofcode')
load_dotenv(env_file)
AOC_SESSION = os.getenv('AOC_SESSION', '')

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()  # assumes that we're in ROOT/src/advent_of_code/constants.py

DATA_DIR = ROOT_DIR / 'data'
LOGS_DIR = ROOT_DIR / 'logs'
SOLUTIONS_DIR = ROOT_DIR / 'solutions'
CODE_TEMPLATE = ROOT_DIR / 'template.py'

EASTERN_TIME = ZoneInfo('America/New_York')
TZ = ZoneInfo(os.getenv('TZ', 'America/New_York'))

CURRENT_YEAR = dt.date.today().year
LATEST_AOC_YEAR = CURRENT_YEAR if dt.date.today().month == 12 else CURRENT_YEAR - 1

PART_ONE_SOLVED_TEXT = 'The first half of this puzzle is complete'
PART_TWO_SOLVED_TEXT = 'Both parts of this puzzle are complete'

SQLITE_PATH = ROOT_DIR / 'advent_of_code.db'
SQLITE_URL = f"sqlite:///{SQLITE_PATH}"