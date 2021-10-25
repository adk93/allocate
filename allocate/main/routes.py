# Standard library imports
import os

# Third party imports
from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required

# Local application imports

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route('/<path:filename>')
@login_required
def upload(filename):
    heads, tails = os.path.split(filename)
    return send_from_directory("uploads/1/thumbnails", tails)
