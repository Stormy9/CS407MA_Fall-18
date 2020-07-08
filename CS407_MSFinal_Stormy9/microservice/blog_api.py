from flask import Flask, jsonify, request, url_for, abort

app = Flask(__name__)


votes = [
	{
		'post_id': 0,
		'vote_count': -1,
	},
	{
		'post_id': 1,
		'vote_count': 5,
	},
	{
		'post_id': 2,
		'vote_count': 42,
	},
]


# define routes for our api:

@app.route('/api/vote_count/', methods=["GET"])
def blog_get_all():
	return jsonify ({'blog': votes})

@app.route('/api/vote_count/<int:post_id>', methods=["GET"])
def blog_get_one(post_id):
	if post_id < 0 or post_id > len(votes):
		abort(404)

	return jsonify (votes[post_id])
