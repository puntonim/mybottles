# MyBottles [![Build Status](https://travis-ci.org/puntonim/mybottles.svg?branch=master)](https://travis-ci.org/puntonim/mybottles)


## Development
Create a virtual environment:
```bash
$ make venv
```
Or install the requirements in the active venv:
```bash
$ make requirements
```
Use a handy `postactivate` script for `virtualenvwrapper`: copy the file
`~/workspace/mybottles/conf/postactivate.template` to `postactivate_paolo` and edit it. Then:
```bash
$ ln -sf ~/workspace/mybottles/conf/postactivate_paolo ~/.virtualenvs/mybottles/bin/postactivate
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