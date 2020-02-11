# Oxford Learners Scraper

This is CLI scraper of american dictionary:

> https://www.oxfordlearnersdictionaries.com/definition/american_english/

It generates excel file with definitions, examples, idioms and synonyms for provided words.
It's somewhat customizable.

```bash
>>> python application.py import -h        
USAGE
  console import [-p <...>] [-m <...>] [-e <...>] [-i] [-r] [-s] [-x] [-f] <terms1> ... [<termsN>]

ARGUMENTS
  <terms>                What words should we import?

OPTIONS
  -p (--part-of-speech)  wydaje mi się, że ten słownik automatycznie wybiera część mowy opisaną jako _1 w adresie i chciałbym żeby to printował defaultowo jeśli zostawie to pole puste, jeśli wpiszę to chciałbym żeby crawler wybrał
                         odpowiedni wpis. (multiple values allowed)
  -m (--meanings)        puste = printuj wszystkie, to samo w “examples to print”
  -e (--examples)        restrict number of examples
  -i (--idioms)          include idioms
  -r (--phrasal)         include phrasal verbs
  -s (--synonyms)        include synonyms
  -x (--split-meanings)  split meanings into separate terms
  -f (--file)            file name of the generated file

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question
```


Made with <3 for [Talking Heads](http://talking-heads.pl/)
