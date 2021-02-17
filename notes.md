Jake Rieger
https://www.youtube.com/watch?v=Z1RJmh_OqeA
https://github.com/jakerieger/FlaskIntroduction

# The most basic app includes
* from flask import Flask
app = Flask(__main__)
* a route  use dedorator @ app.route('/')

app.run(dubug=True)
## Add static and templates subdirectory
* in app.py import render_template and return render_template("index.html")
* Create templates/index.html

## template inheritance
* {% block head %} {% endblck  %}
{% extends base.html %}

## linking
* ```<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">```
* Also had to import url_for in app.py
    * Evidently {{}} runs the code inside the relavant module and has access to the global variables and imports from that module
    