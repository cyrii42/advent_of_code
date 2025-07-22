import pytest

from advent_of_code.helpers import validate_year_and_day
from advent_of_code.constants import LATEST_AOC_YEAR

DUMMY_YEAR = 2015
DUMMY_DAY = 1

YEAR_RANGE_END = LATEST_AOC_YEAR + 1


@pytest.mark.parametrize('year', [year for year in range(2015, YEAR_RANGE_END)])
def test_aoc_valid_years(year):
    assert not validate_year_and_day(year, DUMMY_DAY)

@pytest.mark.parametrize('year', [-1, 0, 1, 1948, 2014, -2015, -2025,
                                  LATEST_AOC_YEAR+1, LATEST_AOC_YEAR+2, 1-LATEST_AOC_YEAR])
def test_aoc_invalid_years(year):
    with pytest.raises(ValueError):
        validate_year_and_day(year, DUMMY_DAY)

@pytest.mark.parametrize('day', [day for day in range(1, 26)])
def test_aoc_valid_days(day):
    assert not validate_year_and_day(DUMMY_YEAR, day) 

@pytest.mark.parametrize('day', [-1, 0, 26, 27, 28, 29, 30, 31, 32])
def test_aoc_invalid_days(day):
    with pytest.raises(ValueError):
        validate_year_and_day(DUMMY_YEAR, day)

@pytest.mark.parametrize('year_str', [str(year) for year in range(2015, YEAR_RANGE_END)])
def test_aoc_valid_years_str(year_str):
    assert not validate_year_and_day(year_str, DUMMY_DAY)

@pytest.mark.parametrize('day_str', [str(day) for day in range(1, 26)])
def test_aoc_valid_days_str(day_str):
    assert not validate_year_and_day(DUMMY_YEAR, day_str)

@pytest.mark.parametrize('year', ['year', 'year2015', '2015year', '201d5'])
def test_non_digit_str_year(year):
    with pytest.raises(ValueError):
        validate_year_and_day(year, DUMMY_DAY)

@pytest.mark.parametrize('day', ['day', 'day15', '15day', '1d5'])
def test_non_digit_str_day(day):
    with pytest.raises(ValueError):
        validate_year_and_day(DUMMY_YEAR, day)


