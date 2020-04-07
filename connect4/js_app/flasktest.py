from __future__ import print_function
from flask import Flask, render_template, make_response
from flask import redirect, request, jsonify, url_for

import io
import os
import uuid
import numpy as np

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.debug = True
app._static_folder = os.path.abspath("templates/static/")

@app.route('/', methods=['GET'])
def index():
    title = 'Welcome to Teisendorf'
    return render_template('connect_html.html',
                           title=title)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
