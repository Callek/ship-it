from mozilla.release.info import getReleaseName

from kickoff import db

def getReleaseTable(release):
    if release.startswith('Fennec'):
        return FennecRelease
    elif release.startswith('Firefox'):
        return FirefoxRelease
    elif release.startswith('Thunderbird'):
        return ThunderbirdRelease
    else:
        raise ValueError("Can't find release table for release %s" % release)

class Release(object):
    name = db.Column(db.String(100), primary_key=True)
    submitter = db.Column(db.String(250), nullable=False)
    version = db.Column(db.String(10), nullable=False)
    buildNumber = db.Column(db.Integer(), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    mozillaRevision = db.Column(db.String(100), nullable=False)
    l10nChangesets = db.Column(db.String(250), nullable=False)
    complete = db.Column(db.Boolean(), nullable=False, default=False)

    def __init__(self, submitter, version, buildNumber, branch,
                 mozillaRevision, l10nChangesets):
        self.name = getReleaseName(self.product, version, buildNumber)
        self.submitter = submitter
        self.version = version
        self.buildNumber = buildNumber
        self.branch = branch
        self.mozillaRevision = mozillaRevision
        self.l10nChangesets = l10nChangesets
    
    def toDict(self):
        me = {'product': self.product}
        for c in self.__table__.columns:
            me[c.name] = getattr(self, c.name)
        return me

    def __repr__(self):
        return '<Release %r>' % self.name

class FennecRelease(Release, db.Model):
    __tablename__ = 'fennec_release'
    product = 'fennec'

class DesktopRelease(Release):
    partials = db.Column(db.String(100))

    def __init__(self, partials, *args, **kwargs):
        self.partials = partials
        Release.__init__(self, *args, **kwargs)

class FirefoxRelease(DesktopRelease, db.Model):
    __tablename__ = 'firefox_release'
    product = 'firefox'

class ThunderbirdRelease(DesktopRelease, db.Model):
    __tablename__ = 'thunderbird_release'
    product = 'thunderbird'
    commRevision = db.Column(db.String(100))

    def __init__(self, commRevision, *args, **kwargs):
        self.commRevision = commRevision
        DesktopRelease.__init__(self, *args, **kwargs)
