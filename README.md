# SadReaccs - Joan Chirinos, Raunak Chowdhuy, Susan Lin

Welcome! The title of our project is **WeatherBois** and in short, it allows users to search cities by name and view the current/past/future climate and weather. The app will also provide historical data on the country in question. This is intended to help travelers can make the most informed decisions about the climate of where they want to go.

Our project utilizes three APIs: GeoDB, World Weather Online, and Climacell. The descriptions are below and the instructions to use each may be found in **API Key Instructions** after **Instructions for launch**

API | Description
--- | ---
Accuweather Locations API | access to geographical data of a given location (i.e. city name)
Climacell | access to realtime weather and forecasts
World Weather Online | access to historical weather data
Dogs API | pictures of dogs

## Dependencies:
- We are using **Python3**
- a virtual environment (aka venv)
- flask
   - launch the venv using ". path/<venv name>/bin/activate"
   - pip install flask

## Instructions for cloning repo:
- go to [PM Lin's repo](https://github.com/slin15/SadReaccs)
- copy the ssh key under **clone or download**
- open up a bash session and navigate to where you'd like to house the repo
- type `git clone` and your ssh key

## Instructions for launch:
- start up your venv by typing `. path/<venv name>/bin/activate`
- cd to the project repository/v2
- type in python app.py
- go to the localhost:5000 address on your chosen browser

## Instructions for adding API keys:
- Add the text files (`accuweather.txt`, `worldweatheronline.txt`, and `climacell.txt`) to the root of the repo.

## API Key Instructions

### Accuweather -- 50 requests/day
- Click on [this link](https://developer.accuweather.com/). Click "Register", and submit the registration form. You will receive an email.
- Follow the instructions in the email to avail yourself of an API key.
- Copy/paste this key to `accuweather.txt`.

### Climacell —- 1000 requests/day
- Navigate to Climacell's API website, and create an account. [This link](https://developer.climacell.co/signup?accountType=basic&planType=free&price=free) will take you directly to the create account page with the Free Plan selected.
- From your account dashboard, select the API Token. Copy this token.
- Paste the key into `climacell.txt`.

### World Weather Online -- 500 requests/day
- Navigate to WWO's API website, and [create an account](https://www.worldweatheronline.com/developer/api/docs/). Follow the prompts to create your account (you can also login using Github, Google+, or Facebook).
- Once logged in, the API key will be available in the dashboard. Copy it.
- Paste the key into `worldweatheronline.txt`.

### Dogs API
- Nothing is required!

## Please make sure to paste the correct keys into the correct files, else the API requests will not work!
