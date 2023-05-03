"""
CSC310 Web App for CSV data-sets
"""

# Imports
import os
from flask import Flask, request, render_template, flash, redirect 
from datetime import datetime
import pandas as pd
import numpy as np

# Initialize app and database
app = Flask(__name__)

# Home Page
ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print("post")
        if 'file' not in request.files:
            print("No file part")
            return redirect('/')
        file = request.files['file']
        if file.filename == '':
            print("No selected file")
            return redirect('/')
        if file and allowed_file(file.filename):
            # filename = file.filename
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = pd.read_csv(file)
            print("succesful")
            return render_template('csv-head.html', df=df)
            # return "successful"
            # return redirect('/csv-head')
    print("render")
    return render_template('index.html') 


# Debug mode
if __name__ == '__main__':
    app.run(debug=True)