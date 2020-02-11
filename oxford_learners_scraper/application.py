#!/usr/bin/env python

from oxford_learners_scraper.import_command import ImportCommand
from cleo import Application

application = Application()
application.add(ImportCommand())


def run():
    application.run()


if __name__ == '__main__':
    run()
