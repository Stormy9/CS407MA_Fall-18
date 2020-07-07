### this is hwk4 version ###
from flask import Flask, jsonify, request, url_for, abort
from mongoengine import connect, Document, IntField, StringField, DateTimeField
from datetime import datetime
import logging

app = Flask(__name__)

#______________________________________________________________________
#
# name & host of mongoDB to connect to:
connect(db="wolfit_activity_log",
		host="localhost")

#______________________________________________________________________
#
# class definition declaring our schema:
class ActivityLog(Document):
	# mongoDB will add a unique object '_id' for each 'Document'
	user_id=IntField(required=True)
	username=StringField(required=True, max_length=64)
	timestamp=DateTimeField(default=datetime.utcnow())
	details=StringField(required=True)

#______________________________________________________________________
#
# define routes for our API...
#	how 'models.ActivityLog.log_event' accesses the activity log,
#     after 'log_event' is called by the various functions in 'routes'
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# GET ACTIVITIES -- returns whole list of activities FROM
#   the db specified up top:

@app.route('/api/activities/', methods=["GET"])
def activity_log_list():

	activities = ActivityLog.objects.all().order_by('-timestamp').limit(10)
		# note you call the Class/schema name --
			# NOT the collection name from the mongoDB up top

	activity_list = []	# set up empty list
	for a in activities:
		a_dict = a.to_mongo().to_dict()	# handle each 'a', assign to 'a_dict'
		a_dict.pop("_id")	# remove OID from our new mongo/dict object
		a_dict["id"] = str(a.pk)	# 'pk' = 'primary key' (mongoengine)
								# stringify the pk & put it in new key 'id'
		a_dict["location"] = url_for("activity_log_by_id", id=a_dict["id"])
		activity_list.append(a_dict)	# ^- call on method name
										# the CORRECT method name (:
	return jsonify({'wolfit activity log': activity_list}), 201

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# GET ACTIVITY BY ID -- returns a specific activity FROM
#	the db specified up top:

@app.route('/api/activities/<string:id>', methods=["GET"])
def activity_log_by_id(id):
	# can't call this anymore -- not right type:
	#if id < 0 or id >= len(activity_log):
	#	abort(404, "no such thing exists on Wolfit")

	a = ActivityLog.objects.get(id=id)

	a_one = a.to_mongo().to_dict()
	a_one.pop("_id")
	a_one["id"] = str(a.pk)
	a_one["location"] = url_for("activity_log_by_id", id = a_one["id"])

	#activity = ActivityLog.objects.get(id=id).to_json()
	#logging.critical(ActivityLog.objects.get(id=id).to_json())
		# ^- did NOT work  (:
		# (although i think it did something, just not what i wanted)
	return jsonify(a_one), 201

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# "POST" -- register new Wolfit user *OR* log new activity of some kind
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

	# like a JSON 'template', following our schema/Class up-top,
	#	for new activities being POST'd, to be passed into:
	activity_log_entry = ActivityLog(
		user_id=new_activity["user_id"],
		username=new_activity["username"],
		#timestamp=new_activity["timestamp"], # <- nope (:
		details=new_activity["details"],
	)


	# save newly POST'd activities to the mongoDB up top:
	activity_log_entry.save()	# <-- note you save 'activity_log_entry'
								#     NOT 'new_activity'


	# NOTE this has to go AFTER '.save()' --
	#	in order to be able to pull in DB's id... (i mean, duh)
	#
	# add all this crap to 'new_activity',
	# so that when it returns, it's all in there:
	new_activity['timestamp'] = datetime.utcnow()
	new_activity['id'] = str(activity_log_entry.pk)
	#new_activity['location'] = url_for("new_wolfit_activity", id=new_activity['id'])
		# no, not THIS method, the GET one method (like you did for GET all)
	new_activity['location'] = url_for("activity_log_by_id", id=new_activity['id'])


	# now jsonify & return our new activity + status code:
	return jsonify(new_activity), 201
		# note we have the 'request.get_json()' thing up there
#______________________________________________________________________
