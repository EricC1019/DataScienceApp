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
@app.route('/', methods=["GET", "POST"])
def home():
    return "hello world"

# Debug mode
if __name__ == '__main__':
    app.run(debug=True)