import json
import logging

import httplib2
from flask import current_app, Flask, redirect, request, session, url_for
from oauth2client.contrib.flask_util import UserOAuth2

# init oath2
oauth2 = UserOAuth2()


def create_flask_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        model = get_model()
        model.init_app(app)

    # [START init_app]
    # Initalize the OAuth2 helper.
    oauth2.init_app(
            app,
            scopes=['email', 'profile'],
            authorize_callback=_request_user_info)

    # [END init_app]

    # [START logout]
    # Add a logout handler.
    @app.route('/logout')
    def logout():
        # Delete the user's profile and the credentials stored by oauth2.
        del session['profile']
        session.modified = True
        oauth2.storage.delete()
        return redirect(request.referrer or '/')

    # [END logout]

    # Register the CRUD blueprint.
    from .crud import crud
    app.register_blueprint(crud, url_prefix='/catalog')

    # Add a default root route.
    @app.route("/")
    def index():
        return redirect(url_for('crud.list'))

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app


def get_model():
    """
    Sets the backend model to datastor and grabs it from the local dir. This
    provides all the methods that can be called on the data.
    """
    model_backend = current_app.config['DATA_BACKEND']
    if model_backend == 'datastore':
        from . import model_datastore
        model = model_datastore
    else:
        raise ValueError(
                "No appropriate databackend configured. "
                "Please specify datastore, cloudsql, or mongodb")

    return model


# [START request_user_info]
def _request_user_info(credentials):
    """
    Makes an HTTP request to the Google+ API to retrieve the user's basic
    profile information, including full name and photo, and stores it in the
    Flask session.
    """
    http = httplib2.Http()
    credentials.authorize(http)
    resp, content = http.request(
            'https://www.googleapis.com/plus/v1/people/me')

    if resp.status != 200:
        current_app.logger.error(
                "Error while obtaining user profile: %s" % resp)
        return None
    session['profile'] = json.loads(content.decode('utf-8'))

# [END request_user_info]
