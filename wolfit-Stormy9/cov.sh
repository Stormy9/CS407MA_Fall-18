#!/bin/bash
export WOLFIT_SETTINGS=$(pwd)/test.settings
export FLASK_ENV=test
export FLASK_DEBUG=0
coverage run --source "." -m py.test 
coverage html --omit='load_reddit_posts.py'
open htmlcov/index.html
coverage report -m --omit='load_reddit_posts.py'
