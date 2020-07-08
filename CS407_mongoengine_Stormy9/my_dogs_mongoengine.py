from mongoengine import connect, StringField, IntField, DateTimeField, Document
from datetime import datetime
import os


# pull in environment variables:
mLab_db = os.getenv('MLAB_DB')
mLab_host = os.getenv('MLAB_HOST')
mLab_username = os.getenv('MLAB_USERNAME')
mLab_password = os.getenv('MLAB_PASSWORD')


# connect to mLab mongoDB:
connect(db=mLab_db,
		host=mLab_host,
		username=mLab_username,
		password=mLab_password)

#______________________________________________________________________
#
# declare our schema:
class dog_log(Document):
	dog_id=IntField(required=True)
	dog_name=StringField(required=True, max_length=36)
	breed=StringField(required=True, max_length=36)
	color=StringField(required=True, max_length=36)
	details=StringField(required=True)
	timestamp=DateTimeField(default=datetime.utcnow())


# create an entry based on our schema:
dog = dog_log(
	dog_id=999,
	dog_name="Sawyer",
	breed="Sheltie",
	color="tricolor",
	details="can't hold his licker (woof!)",
)

# save new entry:
dog.save()

# return summary of our entry:
print(dog.to_json())

#______________________________________________________________________
#
# so this is creating 'dog_log' mLab mongoDB and writing to it!  (:
