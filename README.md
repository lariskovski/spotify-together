# Spotify (Listen) Together

Based on project [Spotify Buddylist](https://github.com/valeriangalliat/spotify-buddylist).

## Running it Locally

- Get the SP_DC cookie from Spotify's web player cookies. More info on the [original repo](https://github.com/valeriangalliat/spotify-buddylist#fetching-the-cookie)

- Export the cookie on the terminal like so: ``export SP_DC="xxxxxx"``

- Execute the script with the following commands:

~~~~
pipenv --python $(which python3.8) shell
pipenv install
python app.py
~~~~

- The browser will ask for your user's authorization

- After accepted, it'll redirect, copy all the redirect url and enter it on the terminal, as asked