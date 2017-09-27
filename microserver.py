"""
    TODO: Add description of this script
    TODO: Add license
"""
from __future__ import print_function, division, unicode_literals
import os

from flask import Flask
from flask import render_template, url_for
app = Flask(__name__)

MODELS_DIR = "../models"

def get_best_score(model_name):
    try:
        with open(os.path.join(MODELS_DIR, model_name, "best_score.txt"), mode="r") as f:
            return float(f.read().strip())
    except IOError:
        return(0)


@app.route("/")
def index():
    model_names = os.listdir(MODELS_DIR)
    scores = [get_best_score(model) for model in model_names]
    return render_template('index.html',
                           style_path=url_for('static', filename='style.css'),
                           model_and_scores=zip(model_names, scores))


