#!/usr/bin/env python

from import_command import GreetCommand
from cleo import Application

application = Application()
application.add(GreetCommand())

if __name__ == '__main__':
    application.run()