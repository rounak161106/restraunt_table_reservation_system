from flask import current_app as app
from .models import *
from flask import Flask, render_template, request, url_for

@app.route('/')
def main():
    return render_template("login.html")