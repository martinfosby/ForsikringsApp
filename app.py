from os import name
from flask import Flask, render_template, request, redirect, session,flash,url_for
import secrets


app = Flask (__name__)
app.secret_key = secrets.token_urlsafe(16)


@app.route('/')
def index():
    return render_template('base.html', title='test')


if name == "__main__":
    app.run(debug=True)


