import logging
from os import path
import site

from paste.auth.basic import AuthBasicHandler

mydir = path.dirname(path.abspath(__file__))
site.addsitedir(mydir)
site.addsitedir(path.join(mydir, 'vendor/lib/python'))

from flask import Flask

from kickoff import app, db

if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-d", "--db", dest="db")
    parser.add_option("--host", dest="host")
    parser.add_option("-p", "--port", dest="port", type="int")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true")
    options, args = parser.parse_args()

    log_level = logging.INFO
    if options.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)

    app.config['SQLALCHEMY_DATABASE_URI'] = options.db
    app.config['DEBUG'] = True
    app.config['CSRF_ENABLED'] = False
    with app.test_request_context():
        db.init_app(app)
        db.create_all()
    def auth(environ, username, password):
        return username == password
    app.wsgi_app = AuthBasicHandler(app.wsgi_app, "Release kick-off", auth)
    app.run(port=options.port, host=options.host)
