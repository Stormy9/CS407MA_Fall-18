import requests, json, sys, time
#______________________________________________________________________
#
# client to fetch our doggies:

def get_dogs():

	url = "http://localhost:8080"
	get_url = url + "/api/dogs"

	r = requests.get(get_url)

	if r.status_code == 200 or 201:
		dogs = json.loads(r.text)

		dog = dogs[1]
									# holy fuck, this actually worked.
									# ha!  (:  how fun!
	print()
	print(dog)
	#print()
#______________________________________________________________________
#
# fetch doggies every 3 seconds --
# 	this should alternate between versions:

def get_loop():
	while True:
		get_dogs()
		time.sleep(3)
#______________________________________________________________________
#
# get things going:

get_loop()
