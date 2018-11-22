from flask import Flask, render_template

from utils import api

app = Flask(__name__)

@app.route('/')
def index():
    return '<a href=/apitester > Test API calls </a> '

@app.route('/apitester')
def apitester():
    args = {}
    # Dog API by Vincent Lin
    URL = 'https://dog.ceo/api/breeds/image/random'
    args['dogs'] = ('Doggos', api.access_info(URL)['message'])

    # Bored API by Imad Belkbir
    URL = 'https://www.boredapi.com/api/activity'
    args['bored'] = ('Bored', api.access_info(URL)['activity'])


    # NY Times API by Puneet Johal
    URL_STUB = 'http://api.nytimes.com/svc/topstories/v2/home.json?api-key='
    API_KEY = 'a0232fcf73d345d5901d4f850939650b'
    args['nytimes'] = ('New York Times Top Stories', api.access_info(URL_STUB, API_KEY)['results'][0])


    return render_template('apitester.html', **args)

if __name__ == '__main__':
    app.debug=True
    app.run()
