from flask import Flask, jsonify
from string_data import string_data_dict

app = Flask(__name__)


@app.route('/api/string_data/<input>', methods=["GET"])
def return_string_data(input):
	# make list into dictionary
	#return jsonify({'string things':string_data(input)})
	# note this ^^^ was working  (:
	return jsonify(string_data_dict(input))
	# and so did this!  (:
