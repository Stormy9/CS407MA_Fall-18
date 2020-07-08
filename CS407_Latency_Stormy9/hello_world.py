import time

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello_world():
	time.sleep(5)
	return "hello, world!! like how long it took just to say that? (:"
