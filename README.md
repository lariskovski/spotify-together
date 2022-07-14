# Spotify (Listen) Together

Listen to the song your friend is listening to.

Based on project [Spotify Buddylist](https://github.com/valeriangalliat/spotify-buddylist).

## Running it Locally

- Get the SP_DC cookie from Spotify's web player cookies. More info on the [original repo](https://github.com/valeriangalliat/spotify-buddylist#fetching-the-cookie)

- Export the cookie on the terminal like so: ``export SP_DC="xxxxxx"``

- Export Spotipy environment variables (Check [Spotify Developers Dashboard](https://developer.spotify.com/dashboard/login)):

~~~~
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url' #  SPOTIPY_REDIRECT_URI=http://127.0.0.1:5000/callback
~~~~

- Execute the script with the following commands:

~~~~
pipenv --python $(which python3.8) shell
pipenv install
python app.py
~~~~

- The browser will ask for your user's authorization

- After accepted, it'll redirect, copy all the redirect url and enter it on the terminal, as asked

## Sources

[Spotipy Docs](https://spotipy.readthedocs.io/en/2.19.0/#)

[LEARN SPOTIPY - A Lightweight Python Spotify Library](https://www.youtube.com/watch?v=tmt5SdvTqUI&list=PLqgOPibB_QnzzcaOFYmY2cQjs35y0is9N&index=1)

[spotify-api-auth-examples](https://github.com/kylepw/spotify-api-auth-examples)