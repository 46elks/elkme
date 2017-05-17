elkme
======

*Command-line texting service provided by 46elks*

This tool is still quite rough, and may behave in strange, un-accounted for
behaviors. It is also prone for random breaking changes, although we'll
try to keep that to a minimum ;)

## Basic usage

`python -m elkme.main "Wow, I'm sending this message from the terminal :)"`

or (if installed)

`elkme "Good morning, upper east side"`

## Installation

Prefered way of installation is by PyPI

`pip install elkme`

## Configuration

The easiest way of configuring `elkme` is by entering your API credentials from
[the 46elks dashboard](https://www.46elks.com/) into the command-line
application and adding `--saveconf` like 
`elkme -u APIUSERNAME -p APIPASSWORD --saveconf`. You can also add a default
sender and receiver by adding the `--to` and `--sender` options.

The configuration file is ini-ish, and looks like:

````
[46elks]
username = REPLACE_ME
password = REPLACE_ME
from = elkme
to = +46700000000
````

## ToDo

- [x] Port to Python 3
- [ ] Write a covering test suite
- [x] Add support for calls

