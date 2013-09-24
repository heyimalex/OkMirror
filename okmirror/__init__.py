import re
import os
from urllib import quote_plus

from flask import Flask, render_template, request, send_from_directory, g
import requests

app = Flask(__name__)

def login():
    credentials = {'username': '_HeyImAlex', 'password': 'pw'}
    s = requests.Session()
    r = s.post('https://www.okcupid.com/login', data=credentials)
    if '_HeyImAlex' not in r.text:
        return error_response("Sorry, but there is an error with OkMirror. "
                              "Please try again later")
    return s

def error_response(message):
    return "%s" % message

@app.route('/')
def index():
    return render_template('okmirror.html')

@app.route('/check/')
@app.route('/check/<username>')
def check(username=None):
    if username == None:
        return error_response("You have to enter a username")

    username = quote_plus(username.strip())

    if username.lower() == '_heyimalex':
        return error_response("I'm sorry, Dave. I'm afraid I can't do that.")

    lower = 0
    upper = 10000

    diff = '<span class="username">%s</span>' % username
    s = login()

    # Checking full range for existence on first run is unnescessary; we can
    # guess one bound and either a) be correct and skip a whole request or
    # b) have no response and be forced to check for existence on the other
    # end, which ultimately ammounts to the same number of requests as
    # before. If you choose the more prevalent side you'd get more than
    # .5 less requests per run on avg. This is assuming that user-not-founds
    # are fairly rare.

    r = s.get('http://www.okcupid.com/match?filter1=25,0,5000&keywords=%s' % username)

    # Make sure still logged in by response here?
    if 'Join the best dating site on Earth' in r.text:
        return error_response("Sorry, but there was an internal error, please try again")

    if diff in r.text:
        upper = 5000
    else:
        r = s.get('http://www.okcupid.com/match?filter1=25,5000,10000&keywords=%s' % username)
        if diff in r.text:
            lower = 5000
        else:
            return error_response('Sorry, but that account could not be found')
    # Best described as a sort of binary search?
    for i in range(5):
        mid = (upper+lower)/2
        r = s.get('http://www.okcupid.com/match?filter1=25,%d,%d&keywords=%s' % (lower, mid, username))
        if diff in r.text:
            upper = mid
        else:
            lower = mid
    return "%s between %d and %d" % (username, lower, upper)

if __name__ == '__main__':
    app.debug = True
    app.run()