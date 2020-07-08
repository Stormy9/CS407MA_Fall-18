import requests, json

get_url = "http://reqres.in/api/users/"
#try:
r = requests.get(get_url)

if r.status_code==200:
	user_data=json.loads(r.text)
	user_list=user_data["data"]

	user=user_list[1]

#except:

print({user['first_name'],user['last_name']})
print(user)
