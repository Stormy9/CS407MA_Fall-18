### HAVE THIS RUNNING -- THEN RUN CLIENT TO CALL IT ###

import connexion

# Create the application instance:
app = connexion.App(__name__,
					specification_dir='./')

#______________________________________________________________________
#
# Read the swagger.yml file to configure the endpoints:
app.add_api('swagger_dogs_v2.yml')

#______________________________________________________________________
#
# Create a URL route in our application for "/":

@app.route('/')
def home():
    return "\nhello, world!  WOU-hoo!  woof!\n\n"


#______________________________________________________________________
#
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0',
    		port=5002,
    		debug=True)

#______________________________________________________________________
#
# so if we go to the browser and put in:
#	:5001/		<- or :8080/
#
#	we get our "hello, world!  WOU-hoo!  woof!"
#
#
# if we go to the browser and put in:
#	:5001/api/dogs						<- note no trailing backslash
#		or again, :8080/api/dogs
#
#	we get our list of doggies!

