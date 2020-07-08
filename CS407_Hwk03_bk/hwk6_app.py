from flask import Flask, jsonify, request, url_for, abort
from mongoengine import connect, Document, IntField, StringField, DateTimeField
from datetime import datetime
import logging
import os

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
# class definition declaring our schema:
class ActivityLog(Document):
	# mLab will insert unique object '_id' for each 'Document'
	user_id=IntField(required=True)
	username=StringField(required=True, max_length=64)
	timestamp=DateTimeField(default=datetime.utcnow())
	details=StringField(required=True)


# just here to test if entry will go into mLab...
test = ActivityLog(
	user_id=11,
	username="Zoey",
	details="WoofWoofWoof!",
)

# comment out unless testing:
# and save it (hopefully we are, anyway...)
#test.save()
# and see if it returns to shell:	# can turn this on when you
#print(test.to_json())				# want to test stuff

#______________________________________________________________________
#
# define routes for our API...
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def handle_activity(activity):
	a_item = activity.to_mongo().to_dict()
	a_item.pop("_id")
	a_item["id"] = str(activity.pk)
	a_item["location"] = url_for("activity_log_by_id", id=a_item["id"])
	return a_item

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# WORKING - PULLS IN mLAB DATA!
#
# GET ACTIVITIES -- returns whole list of activities FROM
#   the db specified up top:

@app.route('/api/activities/', methods=["GET"])
def activity_log_list():

	activities = ActivityLog.objects.all().order_by('-timestamp').limit(10)

	activity_list = []

	for a in activities:
		activity_list.append(handle_activity(a))

	return jsonify({'wolfit activity log': activity_list}), 201

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# GET ACTIVITY BY ID -- returns a specific activity FROM
#   the db specified up top:

@app.route('/api/activities/<string:id>', methods=["GET"])
def activity_log_by_id(id):

	a = ActivityLog.objects.get(id=id)

	return jsonify(handle_activity(a)), 201

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Obviously (from notes up top) this is working just fine...
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


	# add all this crap to 'new_activity',
	# so that when it returns, it's all in there:
	new_activity['timestamp'] = datetime.utcnow()
	new_activity['id'] = str(activity_log_entry.pk)
	new_activity['location'] = url_for("activity_log_by_id", id=new_activity['id'])


	# now jsonify & return our new activity + status code:
	return jsonify(new_activity), 201
		# note we have the 'request.get_json()' thing up there

#______________________________________________________________________
