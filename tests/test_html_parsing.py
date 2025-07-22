from pathlib import Path

import pytest
from bs4 import BeautifulSoup

import advent_of_code.html_parsing as html
import advent_of_code.exceptions as exc
from advent_of_code.constants import LATEST_AOC_YEAR, PART_ONE_SOLVED_TEXT, PART_TWO_SOLVED_TEXT, ROOT_DIR
from advent_of_code.models import Puzzle

TEST_HTML_DIR = ROOT_DIR / 'tests' / 'mock_html'

'''
CHECKLIST: 
    - file with just part 1 (2024 15)
    - file with part 1 and part 2 (2024 13)
    - file with both parts solved (2024 1)
    
    - file with no example (2015 1)
    - file w/ example but not in a "pre" tag?

    - truncated file
    - file with no H2 (title) tag
    - file with no article tags
    

'''

@pytest.fixture
def mock_neither_part_solved():
    with open(TEST_HTML_DIR / 'neither_part_solved.html') as f:
        raw_html = f.read()
    return BeautifulSoup(raw_html, "html.parser")

@pytest.fixture
def mock_part_1_solved():
    with open(TEST_HTML_DIR / 'part_1_solved.html') as f:
        raw_html = f.read()
    return BeautifulSoup(raw_html, "html.parser")

@pytest.fixture
def mock_both_parts_solved():
    with open(TEST_HTML_DIR / 'both_parts_solved.html') as f:
        raw_html = f.read()
    return BeautifulSoup(raw_html, "html.parser")

def test_get_solved_statuses_from_soup_zero(mock_neither_part_solved):
    soup = mock_neither_part_solved
    part_1, part_2 = html.get_solved_statuses_from_soup(soup)
    assert not part_1 and not part_2

def test_get_solved_statuses_from_soup_one(mock_part_1_solved):
    soup = mock_part_1_solved
    part_1, part_2 = html.get_solved_statuses_from_soup(soup)
    assert part_1 and not part_2

def test_get_solved_statuses_from_soup_two(mock_both_parts_solved):
    soup = mock_both_parts_solved
    part_1, part_2 = html.get_solved_statuses_from_soup(soup)
    assert part_1 and part_2

def test_get_puzzle_title_from_soup_zero(mock_neither_part_solved):
    soup = mock_neither_part_solved
    title = html.get_puzzle_title_from_soup(soup)
    assert title

def test_get_puzzle_title_from_soup_one(mock_part_1_solved):
    soup = mock_part_1_solved
    title = html.get_puzzle_title_from_soup(soup)
    assert title

def test_get_puzzle_title_from_soup_two(mock_both_parts_solved):
    soup = mock_both_parts_solved
    title = html.get_puzzle_title_from_soup(soup)
    assert title

def test_get_puzzle_description_from_soup_zero(mock_neither_part_solved):
    soup = mock_neither_part_solved
    part_1, part_2 = html.get_puzzle_description_from_soup(soup)
    assert part_1 and not part_2

def test_get_puzzle_description_from_soup_one(mock_part_1_solved):
    soup = mock_part_1_solved
    part_1, part_2 = html.get_puzzle_description_from_soup(soup)
    assert part_1 and part_2

def test_get_puzzle_description_from_soup_two(mock_both_parts_solved):
    soup = mock_both_parts_solved
    part_1, part_2 = html.get_puzzle_description_from_soup(soup)
    assert part_1 and part_2

def test_get_puzzle_title_and_descriptions_from_soup_zero(mock_neither_part_solved):
    soup = mock_neither_part_solved
    title, part_1, part_2 = html.get_puzzle_title_and_descriptions_from_soup(soup)
    assert title and part_1 and not part_2

def test_get_puzzle_title_and_descriptions_from_soup_one(mock_part_1_solved):
    soup = mock_part_1_solved
    title, part_1, part_2 = html.get_puzzle_title_and_descriptions_from_soup(soup)
    assert title and part_1 and part_2

def test_get_puzzle_title_and_descriptions_from_soup_two(mock_both_parts_solved):
    soup = mock_both_parts_solved
    title, part_1, part_2 = html.get_puzzle_title_and_descriptions_from_soup(soup)
    assert title and part_1 and part_2

def test_get_answers_from_soup_zero(mock_neither_part_solved):
    soup = mock_neither_part_solved
    part_1, part_2 = html.get_answers_from_soup(soup)
    assert not part_1 and not part_2

def test_get_answers_from_soup_one(mock_part_1_solved):
    soup = mock_part_1_solved
    part_1, part_2 = html.get_answers_from_soup(soup)
    assert part_1 and not part_2

def test_get_answers_from_soup_two(mock_both_parts_solved):
    soup = mock_both_parts_solved
    part_1, part_2 = html.get_answers_from_soup(soup)
    assert part_1 and part_2



@pytest.fixture
def mock_no_h2_tag():
    with open(TEST_HTML_DIR / 'no_h2_tag.html') as f:
        raw_html = f.read()
    return BeautifulSoup(raw_html, "html.parser")

def test_get_puzzle_title_from_soup_no_H2_tag(mock_no_h2_tag):
    soup = mock_no_h2_tag
    with pytest.raises(exc.ElementNotFound):
        html.get_puzzle_title_from_soup(soup)



@pytest.fixture
def mock_no_example():
    with open(TEST_HTML_DIR / 'no_example.html') as f:
        raw_html = f.read()
    return BeautifulSoup(raw_html, "html.parser")

def test_get_example_from_soup_no_example(mock_no_example):
    soup = mock_no_example
    with pytest.raises(exc.ElementNotFound):
        html.get_example_from_soup(soup)