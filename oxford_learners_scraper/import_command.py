from cleo import Command

from oxford_learners_scraper.scraper import OxfordLearnerScraper
import xlsxwriter


class ImportCommand(Command):
    """
    Imports words from Oxford Learner's Dictionary (American)

    import
        {terms* : What words should we import?}
        {--p|part-of-speech=* : wydaje mi się, że ten słownik automatycznie wybiera część mowy opisaną jako _1 w adresie i chciałbym żeby to printował defaultowo jeśli zostawie to pole puste, jeśli wpiszę to chciałbym żeby crawler wybrał odpowiedni wpis.}
        {--m|meanings= : puste = printuj wszystkie, to samo w “examples to print”}
        {--e|examples= : restrict number of examples}
        {--i|idioms : include idioms}
        {--r|phrasal : include phrasal verbs}
        {--s|synonyms : include synonyms}
        {--x|split-meanings : split meanings into separate terms}
        {--f|file : file name of the generated file}
    """

    def get_kwargs(self):
        return {
            'pos': self.option('p') or None,
            'senses': int(self.option('m') or '0'),
            'examples': int(self.option('e') or '0'),
            'idioms': self.option('idioms'),
            'phrasal': self.option('phrasal'),
            'synonyms': self.option('synonyms'),
            'split_meanings': self.option('x'),
        }

    @staticmethod
    def get_rows(rows, headers):
        result = []
        for row in rows:
            r = []
            for header in headers:
                r.append(row.get(header, ''))
            result.append(r)
        return result

    def handle(self):
        headers = ['term', 'definition', 'link', 'synonyms', 'idioms', 'phrasal verbs']
        filename = self.option('f') or "files/example.xlsx"
        words = self.argument('terms')
        rows = []
        for word in words:
            self.info(f'Obtaining word "{word}"...')
            ols = OxfordLearnerScraper(word, **self.get_kwargs())
            row = ols.parse()
            rows.extend(row)

        xls_rows = self.get_rows(rows, headers)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:F', 30)
        worksheet.write_row(0, 0, headers)
        self.info(f'Generating excel file: {filename}...')
        for i, r_ in enumerate(xls_rows, start=1):
            worksheet.write_row(i, 0, r_)
        workbook.close()
        self.info(f'Done. Have a nice day!')
