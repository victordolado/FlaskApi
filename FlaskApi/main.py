import os

from werkzeug.serving import run_simple

from project import create_app
from project.config import setup_logger
from project.config import APPLICATION_ROOT

# Select run model.
#
#  * Available modes : 'development', 'testing', 'production'
#
#

# Setting Flask "RUN_MODE" config.
os.environ["RUN_MODE"] = "production"
app = create_app()


# start all the app under a same point localhost/<APPLICATION_ROOT>
class FixScriptName(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        SCRIPT_NAME = APPLICATION_ROOT

        if environ['PATH_INFO'].startswith(SCRIPT_NAME):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(SCRIPT_NAME):]
            environ['SCRIPT_NAME'] = SCRIPT_NAME
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'application.json')])
            return ["The requested URL is not served by your middleware. If you entered the URL manually please check your spelling and try again.".encode()]


# main execution
if __name__ == '__main__':
    app = FixScriptName(app)
    # Set up the logger
    setup_logger()
    # Loading the Flask instance
    run_simple('0.0.0.0', 5000, app, use_reloader=True)
