import requests, json, sys, time


def get_stuff():
	get_url = "https://jsonplaceholder.typicode.com/todos"
	get_url_w_id = get_url + "/" + sys.argv[1]

	r = requests.get(get_url)
	if r.status_code == 200 or 201:
		todos = json.loads(r.text)


	r2 = requests.get(get_url_w_id)
	if r.status_code == 200 or 201:
		get_todo = json.loads(r2.text)



	todo_one = todos[0]	#this gets the INDEX, which is zero-based
							#so asking for 0 gets us the 1st one
							#asking for 1 gets us the 2nd one
							#etc
	#data = r.json()
	#id = sys.argv[1]

	#print(todos)
	#print(r.json)
	print()
	print("this is index zero of the list:")
	print(todo_one)
	print()
	print("this is the url you made with the 1st CL argument you entered:")
	print(get_url_w_id)
	print()
	print("this is the result of asking for that url:")
	print(get_todo)
	print()
	#print(data)

def get_loop():
	while True:
		get_stuff()
		time.sleep(3)


get_loop()
#just for fun!
#cat1 = sys.argv[2]
#cat2 = sys.argv[3]
#print("this is just for fun -- whatever the last two CL arguments you put in:")
#print(cat1 + " " + cat2)	# aha!  it just concats.  but it does something.  (:
#print()
