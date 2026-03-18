from flask import current_app as app
from flask import Flask, render_template, request, url_for

@app.route('/')
def 