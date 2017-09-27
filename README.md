# Model Nanny

Monitor the progress of training models.

**TODO:** Add a description for this project

**TODO:** Add description of required files and directory structure

**TODO:** Add description of dependencies


## Insatalling Flask
```sh
# ===============================================
# INSTALLING FLASK
# ===============================================
sudo apt-get update
sudo apt-get install -y python-pip python3-pip
pip install --upgrade pip
pip3 install --upgrade pip
pip install Flask
pip3 install Flask
```

## Running Model Nanny

```sh
# ===============================================
# ON COMPUTER HOSTING THE TRAINING MODELS
# ===============================================
PROJECT_DIR="/path/to/project"
cd ${PROJECT_DIR}/model_nanny
export FLASK_APP=microserver.py
flask run --host=0.0.0.0 --port=8080

# Maybe add --threaded=True as an argument to `flask run` if its slow and unresponsive
#  - Actually this doesnt work frm command line - look for a workaround.
```
