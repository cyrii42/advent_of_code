from bs4 import BeautifulSoup

from advent_of_code.constants import PART_ONE_SOLVED_TEXT, PART_TWO_SOLVED_TEXT
from advent_of_code.exceptions import ElementNotFound

def get_puzzle_title_from_soup(soup: BeautifulSoup) -> str:
    title = soup.find('h2')

    if not title:
        raise ElementNotFound("Could not find title tag (\"<h2>\")")

    return title.get_text()

def get_solved_statuses_from_soup(soup: BeautifulSoup) -> tuple[bool, bool]:
    if PART_TWO_SOLVED_TEXT in soup.get_text():
        return (True, True)
    elif PART_ONE_SOLVED_TEXT in soup.get_text():
        return (True, False)
    else:
        return (False, False)

def get_puzzle_description_from_soup(soup: BeautifulSoup) -> tuple[str, str]:
    articles = soup.find_all('article')
    try:
        return (articles[0].get_text(), articles[1].get_text())
    except IndexError:
        return (articles[0].get_text(), '')

def get_example_from_soup(soup: BeautifulSoup) -> str:
    example = soup.find('pre')
    
    if not example:
        raise ElementNotFound("Could not find example tag (\"<pre>\")")

    return example.get_text()

def get_answers_from_soup(soup: BeautifulSoup) -> tuple[str, str]:
    # success_tags = soup.find_all('p', attrs={'class':'day-success'})
    # print(success_tags)

    # if not success_tags:
    #     return ('', '')  
    
    answer_p_tags = [p for p in soup.find_all('p') if 'Your puzzle answer was' in p.get_text()]

    if not answer_p_tags:
        return ('', '')

    answer_list = [tag.find('code').get_text() for tag in answer_p_tags]  # type: ignore

    if len(answer_list) == 1:
        return (answer_list[0], '')
    else:
        return (answer_list[0], answer_list[1])