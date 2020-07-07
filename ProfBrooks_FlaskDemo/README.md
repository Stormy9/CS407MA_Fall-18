## Simple Flask App

This is a very simple Flask application. Do the usual to get this running after cloning it:

``` sh
$ pipenv install
$ pipenv shell
```

There are two different apps here - one in a single file (`simple_hello.py`) and another that uses the start of a typical directory structure for Flask (`hello.py`).

## Running the Apps

Use the `FLASK_APP` environment variable to control which app to run:

``` py
export FLASK_APP=hello.py
flask run

export FLASK_APP=simple_hello.py
flask run
```