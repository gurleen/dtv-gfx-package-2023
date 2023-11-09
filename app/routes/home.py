from flask import Blueprint, request, render_template
from datetime import datetime
from app.datastore import store


home = Blueprint("home", __name__, template_folder="../templates")


@home.route("/")
def index():
    return render_template("home.html")


@home.route("/home")
def home_partial():
    now = datetime.now()
    return render_template("home_partial.html", time=now)


@home.route("/graphics")
def graphics():
    graphics = store.graphics
    return render_template("graphics_partial.html", graphics=graphics)