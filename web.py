from flask import Flask, escape, request, render_template
from main import *

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/search')
def web():
    query = request.args.get('q', '')
    return f'Result: {escape(main(query))}'

