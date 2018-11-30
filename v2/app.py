import os
from time import strftime

from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify

from utils import api, db as dbm

app = Flask(__name__) #create instance of class Flask

# app.secret_key = os.urandom(32)

app = Flask(__name__)

@app.route('/')
def index():
    '''
    Displays landing page
    If the user is logged in, displays the user-toolbar
    Otherwise, displays login and create_account buttons
    '''
    if 'username' in session:
        print('LOGGED IN')
        return render_template('index.html', login_info='SNIPPET_user_info.html', username=session['username'])
    else:
        print('NOT LOGGED IN!')
        return render_template('index.html', login_info='SNIPPET_login_create_bar.html')

@app.route('/logout')
def logout():
    '''
    Logs user out, then redirects to landing page
    '''
    if 'username' in session:
        print('LOGGING OUT')
        session.pop('username')
    return redirect(url_for('index'))

@app.route('/account-redirect')
def account_redirect():
    '''
    Redirection on login/create buttons
    If login button pressed, redirect to login page
    If create_account button pressed, redirect to create_account page
    Otherwise, flash user then redirect to landing
    '''
    action = request.args['action']
    if action == 'login':
        return redirect(url_for('login'))
    elif action == 'create':
        return redirect(url_for('create'))
    else:
        flash('Invalid action!')
        return redirect(url_for('index'))

@app.route('/login')
def login():
    '''
    Login route
    If user is logged in, redirects them to root
    Otherwise, renders login template
    '''
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/auth', methods=["POST"])
def auth():
    '''
    Authenticates user
    If username password are correct, store username in session and redirect to landing
    Else, flash user and redirect back to login page
    '''
    username = request.form['username']
    password = request.form['password']

    if not dbm.isUser(username):
        flash('Invalid username or password!')
        return redirect(url_for('login'))

    if dbm.getPw(username) == password:
        session['username'] = username
        return redirect(url_for('index'))

    else:
        flash('Incorrect username or password!')
        return redirect(url_for('login'))

@app.route('/create_account')
def create():
    '''
    If user is logged in, redirects to landing
    Otherwise, renders create_account template
    '''
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template('create_account.html')

@app.route('/create_account_action', methods=["POST"])
def create_action():
    '''
    Attemps to create an account using given username and Password
    Fails if
        Either field contains a space
        The username already exists
        The passwords don't match
    On failure, flashes user and redirects to create_account
    On success
        Stores credentials in DB
        flashes user
        Redirects user to landing
    '''

    username = request.form['username']
    password = request.form['password']
    password_check = request.form['password_check']

    print("USERNAME: {}\nPASSWORD: {}\nPASSWORD2: {}".format(username, password, password_check))

    if ' ' in username or username.strip() == '':
        flash('Username invalid!')
        return redirect(url_for('create'))

    if ' ' in password or password.strip() == '':
        flash('Password invalid')
        return redirect(url_for('create'))

    if password != password_check:
        flash('Passwords don\'t match!')
        return redirect(url_for('create'))

    if dbm.isUser(username):
        flash('Username already in use')
        return redirect(url_for('create'))

    # if you get here, ur successful!
    dbm.register(username, password)

    print('CREATE ACCOUNT SUCCESS')

    flash('You can now log in!')
    return redirect(url_for('index'))

@app.route('/search', methods=["GET"])
def search():
    '''
    Uses the query from the search bar to search for places.
    Returns a list of places that match the query.
    '''
    username = ''
    if 'username' in session:
        login_info = 'SNIPPET_user_info_navbar.html'
        username = session['username']
    else:
        login_info = 'SNIPPET_login_create_bar_navbar.html'
    # query and empty string check
    query = request.args['query']
    result = api.search_city(query)
    if result:
        return render_template('search.html', cities=result, login_info=login_info, username=username)
    elif result == []:
        flash('No cities found!')
        return redirect(url_for('index'))
    else:
        flash('No query inputted!')
        return redirect(url_for('index'))

@app.route('/city/<city>/<lat>/<long>')
def results(city, lat, long):
    args = dict()

    args['city'] = city
    args['username'] = ''
    if 'username' in session:
        args['login_info'] = 'SNIPPET_user_info_navbar.html'
        args['username'] = session['username']
    else:
        args['login_info'] = 'SNIPPET_login_create_bar_navbar.html'

    weather_dict = api.return_historical_weather(lat, long)

    args['today_date'] = weather_dict['date'][-1]
    args['today_max_temp'] = weather_dict['temp']['max'][-1]
    args['today_min_temp'] = weather_dict['temp']['min'][-1]

    time_chunk = int((int(strftime('%H')) - 1) / 3)
    args['today_image'] = weather_dict['today']['weather_icon'][time_chunk]
    args['hour_array'] = weather_dict['today']
    print(args['hour_array'])

    args['historical_weather'] = weather_dict[-8:-1]

    return render_template('results.html', **args)

if __name__ == '__main__':
    app.secret_key = os.urandom(32)
    app.debug=True
    app.run()
