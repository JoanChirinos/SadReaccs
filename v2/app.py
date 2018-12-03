import os
from time import strftime

from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify

from utils import api, db

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

    if not db.isUser(username):
        flash('Invalid username or password!')
        return redirect(url_for('login'))

    if db.getPw(username) == password:
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

    if db.isUser(username):
        flash('Username already in use')
        return redirect(url_for('create'))

    # if you get here, ur successful!
    db.register(username, password)

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
    '''
    Dynamic routing for results page
    Shows weather information for a given city, lat, and long
    '''
    args = dict()
    args['city'] = city
    args['username'] = ''
    if 'username' in session:
        args['login_info'] = 'SNIPPET_user_info_navbar.html'
        args['username'] = session['username']
    else:
        args['login_info'] = 'SNIPPET_login_create_bar_navbar.html'

    weather_dict = api.return_historical_weather(lat, long)
    today = weather_dict['today']
    args['today'] = today
    print('\n\nTODAY\'S WEATHER\n\n{}\n\n'.format(today))
    for item in today.items():
        print('{}:\n\t{}'.format(item[0], item[1]))

    args['old_weather'] = weather_dict
    # print('\n\nOLD WEATHER\n{}\n\n'.format(weather_dict))
    # for item in weather_dict.items():
    #     print('{}\n\n'.format(item))
    # print('\n\nEND OLD WEATHER\n\n')


    args['today_date'] = weather_dict['date'][-1]
    args['today_max_temp'] = weather_dict['temp']['max'][-1]
    args['today_min_temp'] = weather_dict['temp']['min'][-1]

    time_chunk = int((int(strftime('%H')) / 3) - 1)
    args['today_image'] = weather_dict['today'][time_chunk]['weather_icon']

    forecast = api.return_weather(lat, long)
    # print('\n\nSTARTING FORECAST\n')
    # print('\n{}\n\n'.format(forecast))
    # for i in forecast.items():
    #     print('{}\n'.format(i))
    # print('\n\nEND FORECAST\n')

    args['time_chunks'] = ['12:00&nbsp;am&nbsp;-&nbsp;2:59&nbsp;am', '3:00 am - 5:59 am', '6:00 am - 8:59 am', '9:00 am - 11:59 am', '12:00 pm - 2:59 pm', '3:00 pm - 5:59 pm', '6:00 pm - 8:59 pm', '9:00 pm - 11:59 pm']

    args['daily_forecast'] = forecast
    args['lat'] = lat
    args['long'] = long
    return render_template('results.html', **args)

@app.route('/save/<city>/<lat>/<long>')
def save(city, lat, long):
    if 'username' in session:
        db.addSearch(session['username'], long, lat, city)
        return redirect(url_for('results', city=city, long=long, lat=lat))
    else:
        print('\n\n\nYEETING\n\n\n')
        flash('You must be logged in to do that!')
        return redirect(url_for('results', city=city, long=long, lat=lat))

@app.route('/saved_searches')
def saved_searches():
    if 'username' in session:
        searches = db.getSearches(session['username'])
        print('\n\nSEARCHES:\n\n{}\n\n'.format(searches))
        return render_template('saved_searches.html')
    else:
        flash('You must be logged in to to that!')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = os.urandom(32)
    app.debug=True
    app.run()
