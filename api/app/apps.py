from django.apps import AppConfig
from mask.script.objectdetection import load_models
import sys, os

"""
Middleware to configure the server to spin up and load the Tensorflow models upon starting.
"""
class AppConfig(AppConfig):
    name = 'app'

    """
    Once the Django server app has started and is ready, load the models
    """
    def ready(self):
        # Checks if the server run is the API or the queue. If its the API, we dont need to load models to return True
        if 'process_tasks' not in sys.argv:
            return True

        # Django runs two instances of the server, one for initial one and one is a background to allow recompilation on
        # save. If the instance is the background one, return True. If its the main instance, load the models.
        if os.environ.get('RUN_MAIN', None) == 'true':
            return True
        # you must import your modules here
        # to avoid AppRegistryNotReady exception

        load_models()
        print("Models loaded")