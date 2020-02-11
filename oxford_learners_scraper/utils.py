from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


BASE_URL = 'https://www.oxfordlearnersdictionaries.com/definition/american_english/'


def save_site(word):
    url = BASE_URL + word
    raw_html = simple_get(url)
    with open(f'files/{word}_dump.html', 'wb') as f:
        f.write(raw_html)


def load_site(word):
    with open(f'files/{word}_dump.html', 'rb') as f:
        raw_html = f.read()
    return BeautifulSoup(raw_html, 'html.parser')


def mocked_get(url):
    word = url.split('/')[-1]
    if word == 'cut_3':
        return None
    if not word.startswith('cut'):
        word = word[:-2]
    return load_site(word)
