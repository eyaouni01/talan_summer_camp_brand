from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    return f'Code LinkedIn: {code}<br>State: {state}'
    
if __name__ == '__main__':
    app.run(port=8000)
