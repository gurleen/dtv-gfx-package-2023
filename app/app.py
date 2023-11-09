from flask import Flask
import webview
from datastore import store, save_store
from loguru import logger
from routes import *

logger.info("Welcome to Hydra Graphics.")
logger.info("Initializing...")


server = Flask(__name__, static_folder="../static", template_folder="./templates")
server.register_blueprint(home, url_prefix="/")


webview.create_window("Hydra", server, frameless=True)
webview.start(debug=True)


logger.info("Closing Hydra.")
save_store()