import datetime as dt
from pathlib import Path

import advent_of_code.constants as c

def test_env_file():
    assert c.env_file

def test_aoc_session():
    assert c.AOC_SESSION

def test_root_dir_exists():
    assert c.ROOT_DIR.exists()

def test_root_dir_zmv_pydev():
    assert c.ROOT_DIR == Path.home() / 'python' / 'advent_of_code'
    
def test_sqlite_path_exists():
    assert c.SQLITE_PATH.exists()

def test_tz_is_eastern():
    assert c.TZ == c.EASTERN_TIME

def test_current_year():
    assert c.CURRENT_YEAR == dt.date.today().year