from flask import Flask, abort, render_template


app = Flask(__name__)

posts = [
    {
        'id': 0,
        'title': "Interesting post",
        'content': 'Lorem ipsum etc.',
        'author': 'Poe',
    },
    {
        'id': 1,
        'title': "Storing data from csv file",
        'content': 'So I wanted a project that included a gui so I decided to write a script that would help me calculate wind adjustments (and maybe other stuff down the line) for playing Golf Clash. Basically every club has an "accuracy" and is affected differently depending on wind strength. I created a spreadsheet containing all the attributes for each club and saved it as a csv file. Here is a small sample...',  # noqa: E501
        'author': 'Joe',
    },
    {
        'id': 2,
        'title': "Django Rest Framework serialisation",
        'content': "I'm new to Python/Django and having trouble trying to serialize a N-N relation using Django Rest Framework.",  # noqa: E501
        'author': 'Moe',
    },
]

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


@app.route('/')
def index():
    return render_template(
        "index.html",
        title="Microblog for Microservices",
        posts=posts,
        votes=votes,
    )


@app.route('/post/<int:post_id>')
def post(post_id):
    if post_id < 0 or post_id >= len(posts):
        abort(404)
    post = posts[post_id]
    vote_count = votes[post_id]['vote_count']
    return render_template(
        "post.html",
        title=post['title'],
        post=post,
        vote_count=vote_count,
    )
