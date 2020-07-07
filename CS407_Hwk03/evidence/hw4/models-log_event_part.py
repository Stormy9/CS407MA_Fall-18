# THIS IS JUST FOR REFERENCE PURPOSES
#______________________________________________________________________

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    details = db.Column(db.Text)
    # tutorial: DON'T CHANGE ANYTHING IN THIS ^^^ ActivityLog schema!
    #   could trigger loss of our mySQL stuff, which we don't want.
        #--------------------------------------------------------------
        #
        # DELETED            | no longer needed -- not using this
        #def __repr__(self): | activity log instance anymore <notes>
        #--------------------------------------------------------------
        #
        # DELETED               | no longer needed -- helper method to
        #def latest_entry(cls): | verify logging was happening <notes>
        #--------------------------------------------------------------
        #
        # log_event:
        # replace original code <notes> that wrote to the local mySQL db,
        #   with code calling ('invoking') our new microservice
        #     (which is essentially lifted out of 'activity_logger.py',
        #        with a few adjustments...)

    @classmethod
    def log_event(cls, user, details):  # pass in full user object
        url = 'http://localhost:5001'
        post_url = url + "/api/activities/"

        #extract from passed-in user object
        new_activity = {
            "user_id":user.id,                     # <see notes>
            "username": user.username,
            "timestamp": str(datetime.utcnow()),   # fine as-is
            "details": details,         		   # passed in directly
        }

        try:
            r = requests.post(post_url, json=new_activity)
            if r.status_code == 201 or 200:    # everything worked
                logging.info(f"post new activity SUCCESS! at {post_url}")
                logging.critical(r.text)
                #logging.info(json.loads(r.text))
            else:	# talking to server -- but not getting a 201
                logging.critical(f"post new activity FAILURE! at {post_url}: {r.text}")
                    # diff between {r.text} here & up there?
                    # ^^^ use 'logging' instead of 'print'
                    #               note 'levels' of logging...
        except requests.exceptions.RequestException:
            # for if service not available
            print(f"could not connect to activity log service at {url}")

        #--------------------------------------------------------------
