# MYBOTTLES


## Development
Create a virtual environment:
```bash
$ make venv
```
Or install the requirements in the active venv:
```bash
$ make requirements
```
Use a handy `postactivate` script for `virtualenvwrapper`:
```bash
$ ln -sf ~/workspace/mybottles/conf/postactivate ~/.virtualenvs/mybottles/bin/postactivate
```
Migrate:
```bash
$ manage migrate
```
Serve at http://127.0.0.1:8000:
```bash
$ make serve
```


## Copyright
Copyright 2019 puntonim (https://github.com/puntonim). No License.