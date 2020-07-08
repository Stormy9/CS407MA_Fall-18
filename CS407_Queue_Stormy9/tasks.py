from celery import Celery

# this is from assignment instructions --
#	so this is right way to connect to redis:
#	  ADDED the backend per the Celery 1st Steps:
app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')

@app.task
def add(x, y):
	return x + y
