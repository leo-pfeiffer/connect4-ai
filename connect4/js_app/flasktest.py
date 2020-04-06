from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    # run code here and return selected move as dict
    return {"row": 1, "col": 2}