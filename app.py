import os, requests, json, logging, time

logging.basicConfig()  
logger=logging.getLogger()
logger.setLevel(logging.ERROR)

SP_DC = os.environ['SP_DC']


def get_access_token(sp_dc_token: str) -> str:
    response = requests.get('https://open.spotify.com/get_access_token?reason=transport&productType=web_player',
                    headers={
                            'Content-Type':'application/json',
                            'Cookie': f'sp_dc={sp_dc_token}'
                            })
    content = json.loads(response.content)
    logger.debug(content)
    return content['accessToken']


def get_all_friends_activity_list(web_access_token: str) -> list:
    # Alternative url https://guc-spclient.spotify.com/presence-view/v1/buddylist
    response = requests.get("https://spclient.wg.spotify.com/presence-view/v1/buddylist",
                    headers={
                            'Content-Type':'application/json',
                            'Authorization': f'Bearer {web_access_token}'
                            })
    content = json.loads(response.content)
    return content['friends']


def get_friend_activity(friends_activity: list, friend_name: str) -> dict or None:
    current_epoch_time_in_ms = int(time.time()) * 1000 # Conversion needed as Spotify uses ms and Python, seconds

    for friend in friends_activity:
        if friend['user']['name'] == friend_name:
            friend_activity = {
                "track": friend['track']['name'],
                "uri": friend['track']['uri'],
                "album": friend['track']['album']['name'],
                "artist": friend['track']['artist']['name'],
                "seconds_since_last_update": int((current_epoch_time_in_ms - friend['timestamp']) / 1000)
                }
            logger.info(friend)
            return friend_activity

    logger.error(f"No user {friend_name} found on friends acitivity.")


def play_track(user_id: str, track_id: str) -> None:
    import spotipy
    import spotipy.util as util
    from json.decoder import JSONDecodeError

    scope = 'user-read-private user-read-playback-state user-modify-playback-state'

    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(user_id, scope) # add scope
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{user_id}")
        token = util.prompt_for_user_token(user_id, scope) # add scope

    # Create our spotify object with permissions
    spotifyObject = spotipy.Spotify(auth=token)

    # Get current device
    try:
        devices = spotifyObject.devices()
        deviceID = devices['devices'][0]['id']
    except IndexError:
        print("No connected devices.")

    # Play Song
    spotifyObject.start_playback(deviceID, None, [track_id])
    # print(spotifyObject.current_user()['id'])


def main():
    # Provide your used_id and friends name
    USER_ID = '' # https://support.symdistro.com/hc/en-us/articles/360039036711-Spotify-How-to-obtain-a-URI-URL
    FRIEND_NAME = ''

    web_access_token = get_access_token(SP_DC)
    friends_activity = get_all_friends_activity_list(web_access_token)

    friend_activity = get_friend_activity(friends_activity, FRIEND_NAME)
    print(friend_activity)
    track_uri = friend_activity['uri']

    play_track(USER_ID, track_uri)


if __name__ == "__main__":
    main()
