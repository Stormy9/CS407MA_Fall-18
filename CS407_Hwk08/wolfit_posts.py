from datetime import datetime

# how cool is this?
def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# WOLFIT_POSTS is our module...
# Data (static obviously) to serve with our API:
#   but this could be the start of extracting a 'posts' microservice
#   for Wolfit!
#
WOLFIT_POSTS = {
    "0": {		# <- this is the 'key'
    	"post_id": "987",
		"user_id": "123",
		"author": "Possum",
        "subWolfit": "Learning Python",
        "subject": "Finding prime factors in Python",
        "content": "I'm trying to do a python program to find prime factors...",
        "timestamp": get_timestamp()
    },
    "1": {		# <- swagger.yml orders the data by key
    	"post_id": "876",
		"user_id": "234",
		"author": "Lacey",
        "subWolfit": "Learning Haskell",
        "subject": "optimizing prime factor algorithm in Haskell",
        "content": "I'm trying to speed up the run-time of my Haskell prime factor function...",
        "timestamp": get_timestamp()
    },
    "2": {		# the keys are also 'look-ups' for us
    	"post_id": "765",
		"user_id": "345",
		"author": "Zoey",
        "subWolfit": "Learning Prolog",
        "subject": "Having trouble getting Prolog IDE set up",
        "content": "Why is it such a pain-in-the-ass compared to other languages?",
        "timestamp": get_timestamp()
    },
    "3": {		# keys are not actually returned as
    	"post_id": "654",
		"user_id": "456",
		"author": "Sawyer",
        "subWolfit": "Brushing up on JavaScript",
        "subject": "Finding prime numbers with JavaScript",
        "content": "So it's been a while since I've programmed in javascript...",
        "timestamp": get_timestamp()
    },	# <- note these damned commas! (:
    "4": {		#a part of the data set
    	"post_id": "543",
		"user_id": "567",
		"author": "Jack",
        "subWolfit": "Practicing Java",
        "subject": "Finding prime factors with Java - optimal algorithm",
        "content": "My friend is writing Python to find prime factors, and I want to do the same in Java, but...",
        "timestamp": get_timestamp()
    }
}

# ...read() is our method.
# Create a handler for our read (GET) dogs:
def read():
    #"""
    #This function responds to a request for /api/dogs
    #with the complete lists of dogs
	#
    #:return:        sorted list of people
    #"""
    #
    # Create the list of dogs from our data
    return [WOLFIT_POSTS[key] for key in sorted(WOLFIT_POSTS.keys())]
#
#______________________________________________________________________
#
# notice the module & method/handler names up there...
# and the 'operationId:' in swagger.yml...
# 	'operationId' is formatted 'module.method'
#		connecting the dots between implementation & specification
#
# also note the timestamp helper function - puts timestamp into a string
#	becuase the swagger.yml specifies that it needs to be a string.
#
