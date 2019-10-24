from flask import Flask, escape, request, render_template
from main import *

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/search/<query>')
def web(query):
    return f'Result: {escape(main(query))}'
