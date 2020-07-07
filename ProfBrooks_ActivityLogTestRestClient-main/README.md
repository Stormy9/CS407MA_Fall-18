## Using the ActivityLogger

To run this client, do the following:

1. Create your environment and enter the shell:
    ```sh
    $ pipenv install --three
    $ pipenv shell
    ```
2. Make the activity_logger.py executable:
    ```sh
    $ chmod +x activity_logger.py
    ```
3. Run the activity logger. You can query the command line as follows:
    ```sh
    $ ./activity_logger --help
    ```
    Normally you'll want to run it against localhost:5000, with the default sleep time of 1. The app will keep running and executing each of the three commands until you kill it with `Ctrl-C`. You'll see something like this, assuming you are running your server in a separate shell:
    ```sh
    $ ./activity_logger.py http://localhost:5000
    Get activities SUCCESS at http://localhost:5000/api/activities/
        Get single activity 0 SUCCESS
    {'details': 'Important stuff here', 'id': 0, 'timestamp': 'Mon, 15 Oct 2018 00:23:52 GMT', 'user_id': 1, 'username': 'john'}
    Post new activity SUCCESS at http://localhost:5000/api/activities
    {'details': 'Paul is alive', 'id': 999, 'location': '/api/activities/999', 'timestamp': '2018-10-15 00:25:26.679639', 'user_id': 9, 'username': 'Paul'}
		```