# Oxford Learners Scraper

This is CLI scraper of american dictionary:

> https://www.oxfordlearnersdictionaries.com/definition/american_english/

It generates excel file with definitions, examples, idioms and synonyms for provided words.
It's somewhat customizable.

## Installation

First make sure you have Python 3.6 or newer installed. In your Terminal run:
    
    $ python --version

The recommended way to install is through [pipx](https://pipxproject.github.io/pipx/):

```bash
$ pipx install oxford_learners_scraper
```

If you don't want to use `pipx` you can just use `pip`.

## Configuration

With the `OLS_OUTPUT_DIR` environment variable you can specify the path to the directory where
imported excel files will be saved. Add the following to your `.zshrc`:

```bash
export OLS_OUTPUT_DIR=/absolute/path/to/your/dir
```

## Usage

```bash
$ ols import -h        
USAGE
  ols import [-p <...>] [-m <...>] [-e <...>] [-i] [-r] [-s] [-x] [-f <...>] <terms1> ... [<termsN>]

ARGUMENTS
  <terms>                What words should we import?

OPTIONS
  -p (--part-of-speech)  specify part(s) of speech to import. If omitted the default one ("_1" suffix) will be imported (multiple
                         values allowed)
  -m (--meanings)        restrict number of meanings (default: "3")
  -e (--examples)        restrict number of examples (default: "3")
  -i (--idioms)          exclude idioms
  -r (--phrasal)         exclude phrasal verbs
  -s (--synonyms)        exclude synonyms
  -x (--split-meanings)  split meanings into separate terms
  -f (--file)            file name of the generated file

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for
                         debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question
```

Example:

```bash
$ ols import bridge "dry run" try -f "my_import.xlsx"
Obtaining word "bridge"...
Obtaining word "dry run"...
Obtaining word "try"...
Saving excel file to: my_import.xlsx...
Done. Have a nice day!
```


Made with :heart: for [Talking Heads](http://talking-heads.pl/)
