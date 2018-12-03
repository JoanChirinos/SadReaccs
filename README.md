# SadReaccs - Joan Chirinos, Raunak Chowdhuy, Susan Lin

welcome! the title of our project is **weatherbois** and in short, it allows users to search cities by name and view the current/past/future climate and weather. the app will also provide historical data on the country in question. This is intended to help travelers can make the most informed decisions about the climate of where they want to go.

## Dependencies:
1. We are using **Python3**
2. a virtual environment (aka venv)
3. flask
   - launch the venv using ". path/<venv name>/bin/activate"
   - pip install flask

## Instructions for launch:
   1. start up your venv by typing the command . path/<venv name>/bin/activate
   2. cd to the project repository
   3. type in python app.py
   4. go to the localhost:5000 address on your chosen browser

## API Key Instructions

### GeoDB
1. Sign up through GeoDB's host, RapidAPI. [This page](http://geodb-cities-api.wirefreethought.com/docs/guides/getting-started/test-drive) contains all the instructions/prompts you need to generate an API key.
  - **NOTE:** To sign up for RapidAPI, you will need a credit card. They do not charge your card and instead will cut you off from their API access once you exceed the limit of **432,000 requests** in a day.
2. Follow RapidAPI's prompts to subscribe to the GeoDB API. Collect your API key from the dashboard.
3. Input this token under the **header** parameter `X-Mashape-Key`. There is a second **header** parameter, `X-Mashape-Host` with the value `wft-geo-db.p.mashape.com`. You will now be able to execute sample calls with the API.
4. This is the link we use for API calls: `https://wft-geo-db.p.mashape.com/v1/geo/cities?namePrefix=<city_name>&offset=0&limit=10`
  - Consult the API docs, found [here](http://geodb-cities-api.wirefreethought.com/), for more information.
  - Consult the API demo, found [here](http://geodb-cities-api.wirefreethought.com/demo), for more information.


### Climacell
1. Navigate to Climacell's API website, and create an account. [This link](https://developer.climacell.co/signup?accountType=basic&planType=free&price=free) will take you directly to the create account page with the Free Plan selected. The free plan allows for 1000 calls/day.
2. From your account dashboard, select the API Token. Copy this token.
3. Input this token under the **header** parameter `apikey`. You will now be able to execute sample calls with the API.
4. This is the link we use for API calls: `https://api2.climacell.co/v2/weather/forecast/daily?lat=<some_latitude>&lon=<some_longitude>&fields=temp,feels_like,humidity,wind_speed,precipitation_accumulation`
  - Consult the API docs, found [here](https://developer.climacell.co/docs), for more information.

### World Weather Online
1. Navigate to Climacell's API website, and [create an account](https://www.worldweatheronline.com/developer/api/docs/). Follow the prompts to create your account (you can also login using Github, Google+, or Facebook).
2. Once logged in, the API key will be available in the dashboard. Copy it.
3. Input this token under the GET parameter `key`. You will now be able to execute sample calls with the API.
4. This is the link we use for API calls: `https://api.worldweatheronline.com/premium/v1/past-weather.ashx?format=json&q=<some_latitude>,<some_longitude>&date=<start_date>&enddate=<end_date>&key=<YOUR_API_KEY>`
  - **NOTE:** The free version of the API is a 2 month trial. If you wish to keep using the free version of the API, switch accounts/API keys every two months.
  - `date` and `enddate` cannot vary by more than a month.
  - The API allows for 500 requests/day.
  - Consult the API docs, found [here](https://www.worldweatheronline.com/developer/api/docs/), for more information.
