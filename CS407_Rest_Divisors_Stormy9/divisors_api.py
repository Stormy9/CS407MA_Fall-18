from flask import Flask, jsonify
from divisors import divisors
app = Flask(__name__)

@app.route('/api/divisors/<int:num>', methods=["GET"])
def return_divisors_list(num):
	# make list into dictionary
	return jsonify({'divisors':divisors(num)})



# remember to be in pipenv shell
# do export FLASK _APP=divisors_api.py
# do export FLASK_ENV=development
# do flask run --host=0.0.0.0
# dont' forget to change the path in the browser (duh)
# -- including whatever 'num' you wanna input

