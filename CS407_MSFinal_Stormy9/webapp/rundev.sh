#!/usr/bin/env bash
export FLASK_ENV=development

# originally:
#flask run

flask run --host=0.0.0.0 --port=$@
