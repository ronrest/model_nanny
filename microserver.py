"""
    TODO: Add description of this script
    TODO: Add license
"""
from __future__ import print_function, division, unicode_literals
import os
import pickle

from flask import Flask
from flask import render_template, url_for
app = Flask(__name__)

MODELS_DIR = "../models"

def pickle2obj(file):
    with open(file, mode="rb") as fileObj:
        obj = pickle.load(fileObj)
    return obj


def get_best_score(model_name):
    try:
        with open(os.path.join(MODELS_DIR, model_name, "best_score.txt"), mode="r") as f:
            return float(f.read().strip())
    except IOError:
        return(0)


def get_evals_dict(model_name):
    try:
        evals = pickle2obj(os.path.join(MODELS_DIR, model_name, "evals.pickle"))
    except:
        print("WARNING: Could not load {} \n - Returning blank evals dict instead")
        evals = {"valid_acc": [], "train_acc":[]}
    return evals


@app.route("/")
def index():
    model_names = os.listdir(MODELS_DIR)
    model_names.sort(key=lambda item: item.lower()) # Put in alphabetical order
    scores = [get_best_score(model) for model in model_names]
    return render_template('index.html',
                           style_path=url_for('static', filename='style.css'),
                           model_and_scores=zip(model_names, scores))


@app.route('/models/<model_name>')
def show_user_profile(model_name):
    score = get_best_score(model_name)
    evals = get_evals_dict(model_name)
    return render_template('model.html',
                           style_path=url_for('static', filename='style.css'),
                           model_name=model_name,
                           x=list(range(len(evals["valid_acc"]))),
                           acc_plot_title="Accuracy over time",
                           train_acc=evals["train_acc"],
                           valid_acc=evals["valid_acc"],
                           loss_plot_title="Loss over time",
                           train_loss=evals["train_loss"],
                           valid_loss=evals["valid_loss"],
                           )
