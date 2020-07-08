#!/usr/bin/env bash
#----------------------------------------------------------------------

# which program we're running

#export FLASK_APP=hwk4_app.py

#export FLASK_APP=hwk6_app.py

export FLASK_APP=hwk7_app.py
# and here is our sleep-time env var (goes w/7):
export SLEEP_TIME=9

#export FLASK_APP=h4_exp_doggie_mongo.py
#export FLASK_APP=h4_exp_doggie_mlab.py

#----------------------------------------------------------------------

export FLASK_ENV=development	# tell it development

#----------------------------------------------------------------------

# trying this out:			# it's not working :/
#export MLAB_WOLFIT_SETTINGS=$(pwd)/mLab_app.settings

#----------------------------------------------------------------------

# but this is working!  (:
# mLab settings for activity logger:
export MLAB_DB=wolfit
export MLAB_HOST=ds037478.mlab.com:37478
export MLAB_USERNAME=stormy9
export MLAB_PASSWORD=stormy9wolfit

# mLab settings for practice dog_log app:
#export MLAB_DB=dog_log
#export MLAB_HOST=ds039027.mlab.com:39027
#export MLAB_USERNAME=stormy
#export MLAB_PASSWORD=dog_log_9

# local mongoDB stuff would look like:
#export DB_HOST_LOCAL=mongodb://localhost:27017/
#export DB_NAME_LOCAL=dog_log

#----------------------------------------------------------------------

flask run --host=0.0.0.0 --port=$@		# run the server on different port
										# than wolfit runs on

										# enter port numbers when starting
										#  up server
