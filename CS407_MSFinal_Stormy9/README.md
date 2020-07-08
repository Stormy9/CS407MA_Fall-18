## Instructions for running the microblog app

The web application is in the `webapp` folder. Change to that directory, then install and enter the `pipenv` shell. You can run the app with the `rundev.sh` shell script.

## Creating your microservice

When you are ready to create your microservice, do that in a separate subdirectory off this home directory. This means your project file structure will look something like this:

```
final-microblog/
├── README.md
├── webapp/
|   ├── templates/
|   ├── app.py
|   ├── (etc.)
├── microservice/
|   ├── (your code goes here)
```

Note that you will want to create a distinct `pipenv` for your microservice, which also means you will do your work on the two applications in separate shells.