# Linux Server Configuration

This server has been configured to host the item_catalog application that is found in this repo. The application was designed to be served from Google Cloud Platform with the Datastore backend. In this instance, I have deployed the application to Amazon Lightsail and I am serving the database content from Google Datastore.

I have spent time installing, creating a database and limiting user for Postgres to demonstrate I can do that too. However, no content is present in that database, and it is not feeding the frontend available below. I made this decision as I don't think refactoring the entire backend was necessary to demonstrate the skills required for this project.

* URL: http://ec2-34-201-196-87.compute-1.amazonaws.com/catalog/
* IP: 34.201.196.87

## Software installed

* Apache
* Postgres
* Python3
* Pip

* Google Cloud Datastore dependencies for item_catalog project app to be hosted.

## Modifications Made
* Disabled remote SSH root login
* Disabled SSH password based login
* Created SSH keys for default user and grader
* Added grader to sudoers
* Disabled all incoming ports, enabled outgoing and selectively opened SSH (reconfigured on 2200), HTTP and NTP.
* Updated all applications
* Installed Apache and configured
* Installed Postgres and configured new user "catalog"
    * User catalog only has access to read from catalog database
* Configured the WSGI app deployment of item-catalog
