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

# SETTINGS
VALIDATION_METRIC = "valid_acc"
TRAIN_METRIC = "train_acc"
MODELS_DIR = "../models"
PORT = 8080
HOST = "0.0.0.0"
THREADED = True
DEBUG = False     # Put the server in debug mode?
                  # DANGER! Setting to True makes the system vulnerable to
                  # attack. Should not be used on a publically accesible
                  # IP addresss.
                  # Remember to turn it back to False as soon as you are done.

# TODO: For some reason it requires numpy to open the pickles.
#      I want to get rid of this dependency.

# TODO: Chose which metrics to show on the models page plots using a dict, eg:
#       {"Accuracies over time":
#           {
#           "train": "train_acc",
#           "valid": VALIDATION_METRIC,
#           },
#        "Loss over time":
#           {
#           "train": "train_loss",
#           "valid": "valid_loss",
#           }
#       }
#    This should perhaps be put in a config file, so user does not have to
#    mess around with the python code here.

# TODO: make use of a file `training.txt` that lets you know what file/files
#       is/are currently in the process of being trained.
#       The existence of the file means it is training.
#       The absesnse of the file will mean it is no longer training.
#       Put some icon on the index, and model page to indicate it is training

# TODO: Use a more responsive html style. Text looks huge on desktop but tiny
#       on mobile

# TODO: Make use of log files in model directory, and have a text panel that
#       Allows you to scroll through all the logs of the model.

def pickle2obj(file):
    with open(file, mode="rb") as fileObj:
        obj = pickle.load(fileObj)
    return obj


def get_train_status_file(model_name):
    try:
        with open(os.path.join(MODELS_DIR, model_name, "train_status.txt"), mode="r") as f:
            return f.read().strip()
    except:
        return ""


def get_best_score(model_name):
    try:
        with open(os.path.join(MODELS_DIR, model_name, "best_score.txt"), mode="r") as f:
            contents = f.read().strip()
            return float(contents)
    except ValueError:
        print("WARNING! Incorrect best score file format for model", model_name)
        print("- Expected a value that could be converted to a float.")
        print('- Instead got:   "{}"'.format(contents))
        return 0
    except IOError:
        return 0


def get_evals_dict(model_name):
    try:
        pickle_file = os.path.join(MODELS_DIR, model_name, "evals.pickle")
        evals = pickle2obj(pickle_file)
    except:
        print("WARNING: Could not load {} \n - Returning blank evals dict instead".format(pickle_file))
        evals = {VALIDATION_METRIC: [], TRAIN_METRIC:[]}
    return evals


@app.route("/")
def index():
    model_names = os.listdir(MODELS_DIR)
    # TODO: use a better sorting method. Does not do too well with filenames
    #       contianing numbers that are not fixed length and preceded by 0s
    model_names.sort(key=lambda item: item.lower()) # Put in alphabetical order
    scores = [get_best_score(model) for model in model_names]
    statuses = [get_train_status_file(model) for model in model_names]
    # Sort by score in descending order
    model_score_statuses = sorted(zip(model_names,scores, statuses), key=lambda x: x[1], reverse=True)
    return render_template('index.html',
                           style_path=url_for('static', filename='style.css'),
                           model_score_statuses=model_score_statuses)


@app.route('/models/<model_name>')
def model_page(model_name):
    score = get_best_score(model_name)
    evals = get_evals_dict(model_name)
    return render_template('model.html',
                           style_path=url_for('static', filename='style.css'),
                           model_name=model_name,
                           x=list(range(len(evals[VALIDATION_METRIC]))),
                           acc_plot_title="Accuracy over time",
                           train_acc=evals.get(TRAIN_METRIC, []),
                           valid_acc=evals.get(VALIDATION_METRIC, []),
                           loss_plot_title="Loss over time",
                           train_loss=evals.get("train_loss", []),
                           valid_loss=evals.get("valid_loss", []),
                           )

app.run(host=HOST, port=PORT, threaded=THREADED, debug=DEBUG)
