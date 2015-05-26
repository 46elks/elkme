textme
======

*Command-line texting service provided by 46elks*

This tool is still quite rough, and may behave in strange, un-accounted for
behaviors.

## Basic usage

`./textme.py Wow! I'm sending this message from the terminal!`

## Configuration

Configuration is easiest done by putting your 46elks-credentials and a standard
sender/reciever in the file `~/.textme`

The file is colon-separated, and looks like:

````
username:REPLACE_ME
password:REPLACE_ME
from:textme
to:+46700000000
````

## ToDo

- [ ] Move configuration to "correct" location(s) depending on OS
- [ ] Add quiet mode
