### this is hwk7 version ###
from flask import Flask, jsonify, request, url_for, abort
from mongoengine import connect, Document, IntField, StringField, DateTimeField
from datetime import datetime
import logging
import os
import time

app = Flask(__name__)

#______________________________________________________________________
#
# connect to mLab mongoDB:

mLab_db = os.getenv('MLAB_DB')
mLab_host = os.getenv('MLAB_HOST')
mLab_username = os.getenv('MLAB_USERNAME')
mLab_password = os.getenv('MLAB_PASSWORD')

connect(db=mLab_db,
		host=mLab_host,
		username=mLab_username,
		password=mLab_password)

# next goal: get env vars out of .rundev.sh and into .settings file
#______________________________________________________________________
#
# add simulated latency to our microservice -- by putting
# a 'sleep' function call, into the POST function...
#	-- which is why we imported 'time' up top.
#
# we want duration of the sleep (nap-time) as an env var,
# to be kept in with our mLab env vars, so we can turn it on/off...
#   -- add a os.variable here, to be loaded from env var:

sleep_time = os.getenv('SLEEP_TIME', default =0)

# so this works exactly as expected, adding noticeable latency to POST
# actions while interacting with Wolfit, which would be super-annoying
# to users... BUT -- Wolfit still totally works and things are going
# through the Acitivity Log Microservice and into mLab as expected.

#______________________________________________________________________
#
# class definition -- declaring our schema:
class ActivityLog(Document):
	user_id=IntField(required=True)
	username=StringField(required=True, max_length=64)
	timestamp=DateTimeField(default=datetime.utcnow())
	details=StringField(required=True)

#______________________________________________________________________
#
# define routes for our API...
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# GET ACTIVITIES -- returns whole list of activities FROM
#   the db specified up top:

@app.route('/api/activities/', methods=["GET"])
def activity_log_list():

	activities = ActivityLog.objects.all().order_by('-timestamp').limit(10)
	activity_list = []
	for a in activities:
		a_dict = a.to_mongo().to_dict()
		a_dict.pop("_id")
		a_dict["id"] = str(a.pk)
		a_dict["location"] = url_for("activity_log_by_id", id=a_dict["id"])
		activity_list.append(a_dict)

	return jsonify({'wolfit activity log': activity_list}), 201

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# GET ACTIVITY BY ID -- returns a specific activity FROM
#   the db specified up top:

@app.route('/api/activities/<string:id>', methods=["GET"])
def activity_log_by_id(id):

	a = ActivityLog.objects.get(id=id)

	a_one = a.to_mongo().to_dict()
	a_one.pop("_id")
	a_one["id"] = str(a.pk)
	a_one["location"] = url_for("activity_log_by_id", id = a_one["id"])

	return jsonify(a_one), 201

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# "POST" -- register a new Wolfit user *OR* log activity of some kind
#	 		(login/out... post/comment... vote) -- expects JSON input

@app.route('/api/activities/', methods=["POST"])
def new_wolfit_activity():

	if not request.json:
		abort(400, "POST activity not in json format")

	# validation... call 'get.json()' on our new_activity:
	new_activity = request.get_json()

	# verify main important stuff is getting passed in:
	if 'user_id' not in new_activity or 'username' not in new_activity or 'details' not in new_activity:
		abort(400, "can't POST -- missing important stuff")


	# kinda like a JSON 'template', following our schema up-top,
	#	for new activities being POST'd, to be passed into
	activity_log_entry = ActivityLog(
		user_id=new_activity["user_id"],
		username=new_activity["username"],
		timestamp=datetime.utcnow(),
		details=new_activity["details"],
	)


	# save the newly POST'd activity to the mongoDB up top:
	activity_log_entry.save()	# <-- note you save 'activity_log_entry'
								#     NOT 'new_activity'


	# add this to 'new_activity' so that it all returns:
	new_activity['timestamp'] = datetime.utcnow()
	new_activity['id'] = str(activity_log_entry.pk)
	new_activity['location'] = url_for("activity_log_by_id", id=new_activity['id'])


	# make a call to the sleep() function AFTER saving the object
	# to mLab -- simulate latency in response:
	time.sleep(int(sleep_time))

	# now jsonify & return our new activity + status code:
	return jsonify(new_activity), 201

#______________________________________________________________________
#
# just of interest -- and this makes total sense after a moment's thought --
# but the Celery thing doesn't get invoked with Curl POST calls... only with
# Wolfit activity.  Curl POST you still totally notice the latency.  (:
#
# you don't, though, with GET one/all in browser or Curl.  Just POST.
# which makes sense.
