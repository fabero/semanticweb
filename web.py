from flask import Flask, escape, request, render_template, jsonify
from main import *
from suggestions import *

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/search')
def web():
    query = request.args.get('q', '')
    return f'Result: {escape(main(query))}'

@app.route('/suggestions')
def ajax():
    query = request.args.get('query', '')
    results = suggestions(query)
    return jsonify(results)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(8080), debug=False)
