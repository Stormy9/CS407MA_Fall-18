from datetime import datetime

# how cool is this?
def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# DOGS is our module...
# Data (static obviously) to serve with our API:
DOGS = {
    "Possum": {         		# <- this is the 'key'
        "name": "Possum",
		"color": "silvery bi-blue with patches",
        "tag": "bossy pointy-eared princess",
        #"timestamp": get_timestamp(),
        "version": "2"
    },
    "Lacey": {          		# <- swagger.yml orders the data by key
        "name": "Lacey",
        "color": "tricolor with a 1/2 blaze",
        "tag": "boings happy kangaroo boings",
        #"timestamp": get_timestamp(),
        "version": "2"
    },
    "Zoey": {           		# the keys are also 'look-ups' for us
        "name": "Zoey",
        "color": "steely blue with speckles",
        "tag": "gravity-defying hover abilities",
        #"timestamp": get_timestamp(),
        "version": "2"
    },
    "Sawyer": {         		# keys are not actually returned as
        "name": "Sawyer",
        "color": "tricolor with tiny blaze",
        "tag": "can't hold his licker",
        #"timestamp": get_timestamp(),
        "version": "2"
    },  # commas!
    "Jack": {           		# a part of the data set
        "name": "Jack",
        "color": "blue with one blue eye, one brown",
        "tag": "codename Baby-Jack Like the Cheese",
        #"timestamp": get_timestamp(),
        "version": "2"
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
    return [DOGS[key] for key in sorted(DOGS.keys())]
#
#______________________________________________________________________
#
# notice the module & method/handler names up there...
# and the 'operationId:' in swagger.yml...
#       'operationId' is formatted 'module.method'
#               connecting the dots between implementation & specification
#
# also note the timestamp helper function - puts timestamp into a string
#       becuase the swagger.yml specifies that it needs to be a string.
