from flask import Flask
app = None

def create_app():
    app = Flask()
    app.debug = True
    
