from app.helpers import pretty_date
from datetime import datetime, time, timedelta

def test_just_now():
     assert pretty_date(datetime.utcnow()) == "just now"

def test_seconds_ago():
	assert (pretty_date(datetime.utcnow() - timedelta(seconds=30))) ==  "30 seconds ago"

def test_a_minute_ago():
	assert (pretty_date(datetime.utcnow() - timedelta(seconds=90))) == "a minute ago"

def test_minutes_ago():
	assert (pretty_date(datetime.utcnow() - timedelta(seconds=3400))) == "56 minutes ago" 

def test_an_hour_ago():
	assert (pretty_date(datetime.utcnow() - timedelta(seconds=7199))) == "an hour ago"

def test_hours_ago():
	assert (pretty_date(datetime.utcnow() - timedelta(seconds=83299))) == "23 hours ago"

#_______________________________________________________________________________________

def test_just_about_now():
	assert (pretty_date(datetime.utcnow() - timedelta(days=-1))) == "just about now"

def test_yesterday():
    assert (pretty_date(datetime.utcnow() - timedelta(days=1))) == "Yesterday"

def test_days_ago():
	assert (pretty_date(datetime.utcnow() - timedelta(days=3))) == "3 days ago"
	
def test_weeks_ago():
	assert (pretty_date(datetime.utcnow() - timedelta(days=18))) == "2 weeks ago"

def test_months_ago():
	assert (pretty_date(datetime.utcnow() - timedelta(days=72))) == "2 months ago"
	
def test_years_ago():
	assert (pretty_date(datetime.utcnow() - timedelta(days=456))) == "1 years ago"
