from flask import Flask, g, redirect, url_for
from flask_oidc import OpenIDConnect
from okta import UsersClient
app = Flask(__name__)


app.config['OIDC_CLIENT_SECRETS'] = 'client_secrets.json'
app.config['OIDC_COOKIE_SECURE'] = False
app.config['OIDC_CALLBACK_ROUTE'] = '/oidc/callback'
app.config['OIDC_SCOPES'] = ['openid', 'email', 'profile']
app.config['SECRET_KEY'] = 'rAnd0mL0ngStr1ng'
oidc = OpenIDConnect(app)
okta_client = UsersClient('https://dev-78526377.okta.com', '00QeMpEkXdCKlarGmwQXhJ-ZfFppbZ94y0w1J2Eqo6')


@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield('sub'))
    else:
        g.user = None


@app.route('/')
def index():
    return 'Welcome'


@app.route('/greet')
@oidc.require_login
def greet():
    return 'User first name is {} and id is {}'.format(g.user.profile.firstName, g.user.id)


@app.route('/login')
@oidc.require_login
def login():
    return redirect(url_for('.greet'))


@app.route('/logout')
def logout():
    oidc.logout()
    return redirect(url_for('.index'))