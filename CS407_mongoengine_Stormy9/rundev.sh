#!/usr/bin/env bash

export MLAB_DB=dog_log
export MLAB_HOST=ds039027.mlab.com:39027
export MLAB_USERNAME=stormy
export MLAB_PASSWORD=dog_log_9

python my_dogs_mongoengine.py
