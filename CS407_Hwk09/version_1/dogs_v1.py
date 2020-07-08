from datetime import datetime

# how cool is this?
def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# DOGS is our module...
# data (static obviously) to serve with our API:
DOGS = {
    "Possum": {         		# <- this is the 'key'
        "name": "Possum",
        "tag": "bossy pointy-eared princess",
        #"timestamp": get_timestamp(),
        "version": "1"
    },
    "Lacey": {          		# <- swagger.yml orders the data by key
        "name": "Lacey",
        "tag": "boings happy kangaroo boings",
        #"timestamp": get_timestamp(),
        "version": "1"
    },
    "Zoey": {           		# the keys are also 'look-ups' for us
        "name": "Zoey",
        "tag": "gravity-defying hover abilities",
        #"timestamp": get_timestamp(),
        "version": "1"
    },
    "Sawyer": {         		# keys are not actually returned as
        "name": "Sawyer",
        "tag": "can't hold his licker",
        #"timestamp": get_timestamp(),
        "version": "1"
    },  # <- commas!
    "Jack": {           		# a part of the data set
        "name": "Jack",
        "tag": "codename Baby-Jack Like the Cheese",
        #"timestamp": get_timestamp(),
        "version": "1"
    }
}

# ...read() is our method.
# Create a handler for our read (GET) dogs:
def read():
    #"""
    #This function responds to a request for /api/dogs
    #with the complete lists of dogs
        #
    #:return:        sorted list of doggies
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
