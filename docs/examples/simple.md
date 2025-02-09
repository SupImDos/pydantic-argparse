### Define Model
```python title="simple.py"
--8<-- "examples/simple.py"
```

### Check Help
```console
$ python3 simple.py --help
usage: Example Program [-h] [-v] [-s STRING] [-i INTEGER] [-f | --flag | --no-flag]
                       [--second-flag] [--no-third-flag]

Example Description

required arguments:
  -s STRING, --string STRING
                        a required string
  -i INTEGER, --integer INTEGER
                        a required integer
  -f, --flag, --no-flag
                        a required flag

optional arguments:
  --second-flag         an optional flag (default: False)
  --no-third-flag       an optional flag (default: True)

help:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Example Epilog
```

### Parse Arguments
```console
$ python3 simple.py --string hello -i 42 -f
string='hello' integer=42 flag=True second_flag=False third_flag=True
```
