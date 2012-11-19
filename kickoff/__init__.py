from flask import Flask, render_template, Response, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

from kickoff.model import Release
from kickoff.views.csrf import CSRFView
from kickoff.views.releases import ReleasesAPI, Releases, ReleaseAPI
from kickoff.views.submit import SubmitRelease

# Ensure X-Frame-Options is set to protect against clickjacking attacks:
# https://wiki.mozilla.org/WebAppSec/Secure_Coding_QA_Checklist#Test:_X-Frame-Options
@app.after_request
def add_xframe_options(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

@app.before_request
def require_login():
    if not request.environ.get('REMOTE_USER'):
        return Response(status=401)

@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    return render_template('base.html')

app.add_url_rule('/csrf_token', view_func=CSRFView.as_view('csrf_token'), methods=['GET'])
app.add_url_rule('/submit_release.html', view_func=SubmitRelease.as_view('submit_release'), methods=['GET', 'POST'])
app.add_url_rule('/releases', view_func=ReleasesAPI.as_view('releases_api'), methods=['GET'])
app.add_url_rule('/releases.html', view_func=Releases.as_view('releases'), methods=['GET', 'POST'])
app.add_url_rule('/releases/<releaseName>', view_func=ReleaseAPI.as_view('release_api'), methods=['GET', 'POST'])
