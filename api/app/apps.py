from django.apps import AppConfig
import sys, os
from mask.script.objectdetection import load_models


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        if 'process_tasks' not in sys.argv:
            return True
        if os.environ.get('RUN_MAIN', None) == 'true':
            return True
        # you must import your modules here
        # to avoid AppRegistryNotReady exception

        load_models()
        print("Models loaded")