# Multiuser-blog
This blog has been based heavily on the Google App Engine example of the bookshelf app.

It's registration and login is based on Google+ OAuth.

The live public version can be found at https://bens-blog.appspot.com

## Prereqs
Ensure you have Git, Python and Google App Engine SDK installed on your machine. For further information about GAE installation see: https://cloud.google.com/appengine/docs/standard/python/download 

## Local Usage
Clone this repo, cd into the cloned repo directory and execute the following:
```bash
python main.py
```
This will launch a local Flask webserver at 127.0.0.1:8080

# Deploying to the cloud
With the GAE SDK installed, execute the following in the root directory of the project:
```bash
gcloud app deploy
```
For further information regarding deployment to Google Cloud Platform, see the following: https://cloud.google.com/appengine/docs/flexible/python/testing-and-deploying-your-app
