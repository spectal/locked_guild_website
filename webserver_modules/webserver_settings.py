import os

def build_settings(debug, my_static_path, my_pictures_path):
    webserver_settings = {}
    webserver_settings['debug'] = debug
    webserver_settings['static_path'] = os.path.join(os.path.dirname(__file__), my_static_path),
    webserver_settings['pictures_path'] = os.path.join(os.path.dirname(__file__), my_pictures_path)
    return webserver_settings