from flask import Flask
from flask.ext.script import Manager

app = Flask(__name__)

@app.route('/')
def index():
    return "This is sharing homepage"

if __name__ == '__main__':
    manager.run()

