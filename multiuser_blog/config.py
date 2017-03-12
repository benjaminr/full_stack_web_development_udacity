"""
This file contains all of the configuration values for the application.
Update this file with the values for your specific Google Cloud project.
You can create and manage projects at https://console.developers.google.com
"""

# The secret key is used by Flask to encrypt session cookies.
# [START secret_key]
SECRET_KEY = 'your-secret'
# [END secret_key]

# There are three different ways to store the data in the application.
# You can choose 'datastore', 'cloudsql', or 'mongodb'. Be sure to
# configure the respective settings for the one you choose below.
# You do not have to configure the other data backends. If unsure, choose
# 'datastore' as it does not require any additional configuration.
DATA_BACKEND = 'datastore'

# Google Cloud Project ID. This can be found on the 'Overview' page at
# https://console.developers.google.com
PROJECT_ID = 'your-project-id'

# OAuth2 configuration.
# This can be generated from the Google Developers Console at
# https://console.developers.google.com/project/_/apiui/credential.
# Note that you will need to add all URLs that your application uses as
# authorized redirect URIs. For example, typically you would add the following:
#
#  * http://localhost:8080/oauth2callback
#  * https://<your-app-id>.appspot.com/oauth2callback.
#
# If you receive a invalid redirect URI error review you settings to ensure
# that the current URI is allowed.
GOOGLE_OAUTH2_CLIENT_ID = 'your-client-id'
GOOGLE_OAUTH2_CLIENT_SECRET = 'your-client-secret'
