"""
CSC310 Web App for CSV data-sets
"""

# Imports
import os
from flask import Flask, request, render_template, flash, redirect , url_for
from datetime import datetime
import pandas as pd
import numpy as np

# Initialize app and database
app = Flask(__name__)

# Home Page
ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html') 

# @app.route('/analysis', methods=["POST"])
# def analysis():
#     file = request.files['file']
#     df = pd.read_csv(file)
#     json_data = df.to_json()
#     return json_data

# @app.route('/analysis', methods=["POST"])
# def analysis():
#     file = request.files['file']
#     if file and allowed_file(file.filename):
#         df = pd.read_csv(file)
#         return render_template("csv-head.html", df=df)
#     else:
#         flash("Error: Invalid file type")
#         return redirect("/")

# @app.route('/csv-head', methods=["GET"])
# def csv_head():
#     # read the uploaded file and render the template with the data
#     df = pd.read_csv(request.files['file'])
#     return render_template("csv-head.html", df=df)

import base64
import io

app.config['UPLOAD_FOLDER'] = "uploads"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    print(request.files)

    if "file" not in request.files:
        print("no file part")
    else:
        file = request.files["file"]
        print(request.files['file'])
        df = pd.read_csv(file)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return render_template('csv-head.html', df=df)
    
    # return "hello"
    # print("here")
    df = pd.read_csv("/Users/ericchin/DataScienceApp/DataScienceApp/tests_csv/test_1.csv")
    # df = pd.read_csv(request.files["file"])

    # files = os.listdir("uploads")
    # if (len(files)) > 0:
    #     file = "uploads/"+files[0]
    #     df = pd.read_csv(file)

    #     # remove all files from the folder
    #     for stuff in files:
    #         os.remove("uploads/"+stuff)

    return render_template('csv-head.html', df=df)
    

    # return redirect('/')




# @app.route('/analysis', methods=["POST"])
# def analysis():
#     # read the uploaded file and pass it as a URL parameter to the csv_head route
#     df = pd.read_csv(request.files['file'])
#     encoded_data = df.to_csv(index=False, encoding='utf-8')
#     return redirect('/', data=encoded_data)

# @app.route('/csv-head', methods=["GET"])
# def csv_head():
#     # return "hello eric"
#     # get the encoded file data from the URL parameter and decode it
#     # encoded_data = request.args.get('data', '')
#     # decoded_data = base64.b64decode(encoded_data)

#     df = pd.read_csv(request.files['file'])
#     # encoded_data = df.to_csv(index=False, encoding='utf-8')

#     # # convert the decoded data to a pandas dataframe
#     # df = pd.read_csv(io.StringIO(decoded_data.decode('utf-8')))
#     # render the csv-head template with the dataframe
#     return render_template("csv-head.html", df=df)



# @app.route('/analysis', methods=["POST"])
# def analysis():

#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         contents = file.read().decode('utf-8')
#         df = pd.read_csv(io.StringIO(contents))
#         # do something with the DataFrame here
#         return render_template('csv-head.html', df=df)
#     else:
#         flash('Invalid file type')
#         return redirect('/')
    
    # if request.method == "POST":
    #     print("post")
    # if 'file' not in request.files:
    #     print("No file part")
    #     return redirect('/')
    # file = request.files['file']
    # if file.filename == '':
    #     print("No selected file")
    #     return redirect('/')
    # if file and allowed_file(file.filename):
    #     # filename = file.filename
    #     # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     df = pd.read_csv(file)
    #     print("succesful")
    #     return render_template('csv-head.html', df=df)
    #     # return "successful"
    #     # return redirect('/csv-head')
    # print("render")

    # return "hello"

# Debug mode
if __name__ == '__main__':
    app.run(debug=True)