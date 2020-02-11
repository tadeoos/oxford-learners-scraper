#!/usr/bin/env python

from oxford_learners_scraper.import_command import ImportCommand
from cleo import Application

cmd = ImportCommand()

app = Application('ols', '0.1.1')
app.add(cmd.default())


def run():
    app.run()


if __name__ == '__main__':
    run()
