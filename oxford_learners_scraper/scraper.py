from typing import Dict, Optional, Union, List

from bs4 import BeautifulSoup

from oxford_learners_scraper.utils import simple_get, mocked_get


class OxfordLearnerScraper:

    def __init__(
        self, word, split_meanings=False, pos=None, senses=0,
        examples=0, idioms=True, phrasal=True, synonyms=True
    ):
        self.BASE_URL = 'https://www.oxfordlearnersdictionaries.com/definition/american_english/'
        self.word = word
        self.split_meanings = split_meanings
        self.url = self.build_url()
        self.html = self.get_html()
        self.pos = pos
        self.senses_limit = senses
        self.examples_limit = examples
        self.idioms = idioms
        self.phrasal = phrasal
        self.synonyms = synonyms

    def build_url(self, variation=1):
        return f"{self.BASE_URL}{self.word}_{variation}"

    def get_html(self):
        raw_html = simple_get(self.url)
        if raw_html is None:
            return None
        return BeautifulSoup(raw_html, 'html.parser')

    def no_more_variations(self):
        """Check if no more part of speech exists"""
        return self.html is None

    @staticmethod
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

    def get_phrasal_verbs(self):
        phrasal_verbs = self.html.select('.pv-gs a')
        return {
            'phrasal': '\n'.join(
                [self.parse_phrasal_verbs(pv) for pv in phrasal_verbs]
            )
        }

    @staticmethod
    def parse_phrasal_verbs(pv):
        href = pv.attrs['href']
        return f'HYPERLINK("{href}", "{pv.text}")'
        # return f"<a href={pv.attrs['href']}>{pv.text}</a>"

    def get_senses(self):
        senses = self.html.select('.top-container')[0].findNextSibling().select('.sn-g')
        if self.split_meanings:
            return [self.handle_senses([s]) for s in senses]
        return [self.handle_senses(senses)]

    def get_idioms(self):
        idioms = self.html.select('.idm-gs .idm-g')
        return {
            'idioms': '\n'.join([self.parse_idiom(i) for i in idioms])
        }

    def parse_idiom(self, idiom):
        value = self.get_text(idiom, 'idm', join_=True)
        extra_label = self.get_text(idiom, 'label-g', raising=False)
        definition = self.get_text(idiom, 'def')
        examples = '\n'.join(el.text for el in idiom.select('.x'))
        # return value, f'{extra_label} {definition}', examples
        return f"{value} - {extra_label} {definition}\n{examples}\n"

    def parse_sense(self, sens):
        sub = ' ' + '_ ' * len(self.word)
        definition = sens.select('.def')[0].text
        examples = [f'"{el.text.replace(self.word, sub)}"' for el in sens.select('.sn-g > .x-gs .x')]
        if self.examples_limit:
            examples = examples[:self.examples_limit]
        examples_str = '\n'.join(examples)
        return {'definition': f"{definition}\n\n{examples_str}"}

    def handle_senses(self, senses):
        res = {"term": self.word, 'link': self.url, 'definition': ''}
        if len(senses) < 2:
            res.update(self.parse_sense(senses[0]))
        else:
            for i, sense in enumerate(senses, start=1):
                if self.senses_limit and i > self.senses_limit:
                    return res
                res['definition'] += f'{i}) '
                res['definition'] += self.parse_sense(sense)['definition']
                res['definition'] += '\n\n'
        return res

    def get_synonyms(self):
        res = {'synonyms': ''}
        synonyms = [l for l in self.html.select('.xr-gs') if 'synonym' in l.text]
        for s in synonyms:
            res['synonyms'] += f"{s.select('.xr-g')[0].text}\n"
        return res

    def parse(self):
        if not self.pos:
            return self._parse()
        result = []
        for i in range(1, 30, 1):
            self.build_url(variation=i)
            self.get_html()
            if self.no_more_variations():
                break
            result.extend(self._parse())
        return result

    def _parse(self) -> List:
        row = {"term": self.word, 'link': self.url}
        current_pos = set(el.text for el in self.html.select('.pos'))
        if self.pos and current_pos not in self.pos:
            return []
        senses = self.get_senses()
        row.update(senses[0])
        if self.idioms:
            row.update(self.get_idioms())
        if self.phrasal:
            row.update(self.get_phrasal_verbs())
        if self.synonyms:
            row.update(self.get_synonyms())
        result = [row]
        if self.split_meanings:
            result.extend(senses[1:])
        return result
