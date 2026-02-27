from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
return "<p><label>fake name online</label><input name=\"name\"/><label>first telegram or tweet content</label><input name=\"message\"/><label>daily budget</label><input name=\"sum\"/><label>phone number</label><input name=\"phone\"/></p>"
