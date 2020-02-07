from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from pprint import pprint


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


def get_text(obj, klass, raising=True, join_=False):
    res = obj.select(f'.{klass}')
    if len(res) != 1:
        if join_ and len(res) > 1:
            return ','.join(r.text for r in res)
        elif raising:
            raise ValueError(f"Res: {res}")
        else:
            return ''
    return res[0].text


def parse_sense(sens, word, limit=0):
    sub = '_ ' * len(word)
    definition = sens.select('.def')[0].text
    examples = [f'"{el.text.replace(word, sub)}"' for el in sens.select('.x')]
    if limit:
        examples = examples[:limit]
    examples_str = '\n'.join(examples)
    return {'definition': f"{definition}\n\n{examples_str}"}


def handle_senses(senses, word, split=False, limit=0):
    res = {'definition': ''}
    if len(senses) < 2:
        return parse_sense(senses[0], word, limit)
    for i, sense in enumerate(senses, start=1):
        res['definition'] += f'{i}) '
        res['definition'] += parse_sense(sense, word, limit)['definition']
        res['definition'] += '\n\n'
    return res


def get_synonyms(html):
    res = {'synonyms': ''}
    synonyms = [l for l in html.select('.xr-gs') if 'synonym' in l.text]
    for s in synonyms:
        res['synonyms'] += f"{s.select('.xr-g')[0].text}\n"
    return res


def parse(word, pos=None, senses=0, examples=0, idioms=True,
          phrasal=True, synonyms=True, split_meanings=False):
    url = BASE_URL + word
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    senses = html.select('.top-container')[0].findNextSibling().select('.sn-g')
    idioms = html.select('.idm-gs .idm-g')
    phrasal_verbs = html.select('.pv-gs a')
    row = {"term": word, 'link': url}
    try:
        row.update(handle_senses(senses, word))
        row['idioms'] = '\n'.join([parse_idiom(i) for i in idioms])
        row['phrasal'] = '\n'.join([parse_phrasal_verbs(pv) for pv in phrasal_verbs])
        row.update(get_synonyms(html))
    except (ValueError, KeyError) as e:
        raise
        # return html
    return row


def parse_phrasal_verbs(pv):
    href = pv.attrs['href']
    return f'HYPERLINK("{href}", "{pv.text}")'
    # return f"<a href={pv.attrs['href']}>{pv.text}</a>"


def parse_idiom(idiom):
    value = get_text(idiom, 'idm', join_=True)
    extra_label = get_text(idiom, 'label-g', raising=False)
    definition = get_text(idiom, 'def')
    examples = '\n'.join(el.text for el in idiom.select('.x'))
    # return value, f'{extra_label} {definition}', examples
    return f"{value} - {extra_label} {definition}\n{examples}\n"
