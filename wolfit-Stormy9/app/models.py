from datetime import datetime
from dateutil import tz
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import markdown
from app import db, login
from app.helpers import pretty_date
import requests
import logging
import json
from celery import Celery	# <- hwk8

#_______________________________________________________________________
#
# Celery part for hwk8:

celery = Celery('models',	# should this be celery = Celery? <-YES
			 backend='redis://localhost',
			 broker='redis://localhost'
)

# celery=Celery() -and- @celery.task  <-- must map
#	i.e., could be: app=Celery() -and- @app.task (per Prof Brooks VT)

# PART ONE of the Celery thing for Hwk7 (hwk 8 & 9 = non-Wolfit):
# 	per Prof Brooks (and thinking) put the Celery task OUTSIDE of the
# 	ActivityLog class -- so i put it here w/the celery parameters --
#		"o/w you'll need to make it a class or static method, which is
#	 	more trouble than it's worth"
#
# remember when you run the celery worker, do fully-qualified path
#	AND use '.' not '/' -- so like:
# celery -A app.models worker --loglevel=info

@celery.task					# this is where we move the call
def post_activity(activity):	   # to 'requests.post' ( the r = )
	url = 'http://localhost:8080'
	post_url = url + "/api/activities/"

	try:					# 'activity' is passed in up there
		r = requests.post(post_url, json=activity)
		if r.status_code == 201 or 200:
			logging.info(f"post new activity SUCCESS! at {post_url}")
			logging.critical(r.text)	# this is what that's from! (:
			#logging.info(json.loads(r.text))	# on the server trace!

		else:	# if talking to server but not getting a 201:
			logging.critical(f"post new activity FAILED! at {post_url}: {r.text}")
			# note how we're using 'logging' instead of 'print',
			# and the different levels we're calling

	except requests.exceptions.RequestException:
		# for if the Activity Logging Microservice isn't available:
		print(f"couldn't connect to activity log service at {post_url}")

#______________________________________________________________________

user_vote = db.Table(
    "user_vote",
    db.Column("user.id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("post.id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
)

comment_vote = db.Table(
    "comment_vote",
    db.Column("user.id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("comment.id", db.Integer, db.ForeignKey("comment.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship(
        "Post", order_by="desc(Post.timestamp)", backref="author", lazy="dynamic"
    )
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    post_votes = db.relationship(
        "Post", secondary=user_vote, back_populates="user_votes"
    )
    comments = db.relationship(
        "Comment",
        order_by="desc(Comment.timestamp)",
        backref="author",
        lazy="dynamic"
    )
    comment_votes = db.relationship(
        "Comment", secondary=comment_vote, back_populates="user_votes"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User id {self.id} - {self.username}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.Text)
    link = db.Column(db.Boolean, default=False)
    url = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    vote_count = db.Column(db.Integer, default=0)
    user_votes = db.relationship(
        "User", secondary=user_vote, back_populates="post_votes"
    )
    comments = db.relationship(
        "Comment", order_by="desc(Comment.timestamp)", back_populates="post"
    )

    def __repr__(self):
        return f"<Post id {self.id} - {self.title}>"

    @classmethod
    def recent_posts(cls):
        return cls.query.order_by(Post.timestamp.desc())

    def body_as_html(self):
        if not self.body:
            return None
        return markdown.markdown(self.body)

    def pretty_timestamp(self):
        return pretty_date(self.timestamp)

    def already_voted(self, user):
        return user in self.user_votes

    def adjust_vote(self, amount):
        if self.vote_count is None:
            self.vote_count = 0
        self.vote_count += amount
        db.session.add(self)

    def up_vote(self, user):
        if self.already_voted(user):
            return
        self.user_votes.append(user)
        self.adjust_vote(1)
        db.session.commit()

    def down_vote(self, user):
        if self.already_voted(user):
            return
        self.user_votes.append(user)
        self.adjust_vote(-1)
        db.session.commit()

    def add_comment(self, comment, user):
        comment = Comment(body=comment,
                          user_id=user.id)
        self.comments.append(comment)
        db.session.commit()
        comment.up_vote(user)
        return comment

    def comment_count(self):
        return len(self.comments)


class Category(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    posts = db.relationship(
        "Post", order_by="desc(Post.timestamp)", backref="category", lazy="dynamic"
    )


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    post = db.relationship("Post", back_populates="comments")
    vote_count = db.Column(db.Integer, default=0)
    user_votes = db.relationship(
        "User", secondary=comment_vote, back_populates="comment_votes"
    )

    def __repr__(self):
        return f"<Comment id {self.id} - {self.body[:20]}>"

    def pretty_timestamp(self):
        return pretty_date(self.timestamp)

    def already_voted(self, user):
        return user in self.user_votes

    def adjust_vote(self, amount):
        if self.vote_count is None:
            self.vote_count = 0
        self.vote_count += amount
        db.session.add(self)

    def up_vote(self, user):
        if self.already_voted(user):
            return
        self.user_votes.append(user)
        self.adjust_vote(1)
        db.session.commit()

    def down_vote(self, user):
        if self.already_voted(user):
            return
        self.user_votes.append(user)
        self.adjust_vote(-1)
        db.session.commit()

#______________________________________________________________________
#
# this is the part we work with for our homeworks/microservice...
#______________________________________________________________________

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    details = db.Column(db.Text)
    # remember LEAVE THIS ALONE for now! (old mySQL schema)
#______________________________________________________________________
#
# PART TWO of the celery thing for hwk7...
#
# class ActivityLog code stays essentially the same -- except for adding
# in the '.delay()' call to 'log_event()'...
#
#   BUT -- split it up, with the user's Wolfit activity getting passed
#	into 'log_event()' as before...
#
#	THEN -- 'log_event()', once it's collected the user's activity,
#	calls our new celery task, 'post_activity()', via the '.delay()'
#	call... (other celery stuff up top)
#
#	AND -- the new '@celery.task/post_activity()' contains the same code
#	that was at the end of 'log_event()' before -- the code that actually
#	posts what the user did to Wolfit and returns a status code
#
#----------------------------------------------------------------------
#
    @classmethod
    def log_event(cls, user, details):	# need to pass in full user object

		# extract new_activity from passed-in user object (activity):
        new_activity = {
            "user_id":user.id,				# <see notes>
            "username": user.username,
            "timestamp": str(datetime.utcnow()),	# fine as-is
            "details": details,		# passed in directly -- see?
        }
        post_activity.delay(new_activity)

#---------------------------------------------------------------------
#
# THIS is the way it was for hwk4-hwk6   <- that was working, btw (:
#______________________________________________________________________
#    @classmethod
#    def log_event(cls, user, details):	# need to pass in full user object
#        url = 'http://localhost:8080'
#        post_url = url + "/api/activities/"
#
#		#extract from passed-in user object (activity):
#        new_activity = {
#            "user_id":user.id,
#            "username": user.username,
#            "timestamp": str(datetime.utcnow()),
#            "details": details,
#        }
#
#        try:						# new_activity from right up there
#            r = requests.post(post_url, json=new_activity)
#            if r.status_code == 201 or 200:
#                logging.info(f"post new activity SUCCESS! at {post_url}")
#                logging.critical(r.text)
#                #logging.info(json.loads(r.text))
#
#            else:   # if talking to server -- but not getting a 201:
#                logging.critical(f"post new activity FAILED! at {post_url}: {r.text}")
#
#        except requests.exceptions.RequestException:
#            	# for if the Activity Logging Microservice isn't available:
#                print(f"could not connect to activity log service at {post_url}")
#______________________________________________________________________

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
