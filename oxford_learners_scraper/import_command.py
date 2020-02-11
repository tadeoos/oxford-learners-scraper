import os
from datetime import datetime

from cleo import Command
import xlsxwriter

from oxford_learners_scraper.scraper import OxfordLearnerScraper


class ImportCommand(Command):
    """
    Imports words from Oxford Learner's Dictionary (American)

    import
        {terms* : What words should we import?}
        {--p|part-of-speech=* : specify part(s) of speech to import. If omitted the default one ("_1" suffix) will be imported}
        {--m|meanings=3 : restrict number of meanings}
        {--e|examples=3 : restrict number of examples}
        {--i|idioms : exclude idioms}
        {--r|phrasal : exclude phrasal verbs}
        {--s|synonyms : exclude synonyms}
        {--x|split-meanings : split meanings into separate terms}
        {--f|file= : file name of the generated file, you can omit `.xlsx` suffix. Defaults to `ols_import_TIMESTAMP` }
    """

    def get_kwargs(self):
        return {
            'pos': self.option('p') or None,
            'senses': int(self.option('m') or '3'),
            'examples': int(self.option('e') or '3'),
            'idioms': not self.option('idioms'),
            'phrasal': not self.option('phrasal'),
            'synonyms': not self.option('synonyms'),
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
        output_dir = os.environ.get("OLS_OUTPUT_DIR", '.')
        filename = os.path.join(output_dir, self.option('f') or f"ols_import_{datetime.now()}.xlsx")
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
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
        self.info(f'Saving excel file to: {filename}...')
        for i, r_ in enumerate(xls_rows, start=1):
            worksheet.write_row(i, 0, r_)
        workbook.close()
        self.info(f'Done. Have a nice day!')
