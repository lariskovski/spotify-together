import os, requests, json, logging, time

logging.basicConfig()  
logger=logging.getLogger()
logger.setLevel(logging.INFO)


class FriendsActivity():
    
    def __init__(self) -> None:
        self.sp_dc_token = os.environ['SP_DC']


    def __get_access_token(self) -> str:
        response = requests.get('https://open.spotify.com/get_access_token?reason=transport&productType=web_player',
                        headers={
                                'Content-Type':'application/json',
                                'Cookie': f'sp_dc={self.sp_dc_token}'
                                })
        content = json.loads(response.content)
        logger.debug(content)
        return content['accessToken']


    def __get_all_friends_activity_list(self) -> list:
        web_access_token = self.__get_access_token()

        # Alternative url https://guc-spclient.spotify.com/presence-view/v1/buddylist
        response = requests.get("https://spclient.wg.spotify.com/presence-view/v1/buddylist",
                        headers={
                                'Content-Type':'application/json',
                                'Authorization': f'Bearer {web_access_token}'
                                })
        content = json.loads(response.content)
        return content['friends']


    def get_friend_activity(self, friend_name: str) -> dict or None:
        friends_activity = self.__get_all_friends_activity_list()

        current_epoch_time_in_ms = int(time.time()) * 1000 # Conversion needed as Spotify uses ms and Python, seconds

        for friend in friends_activity:
            if friend['user']['name'] == friend_name:
                friend_activity = {
                    "track_name": friend['track']['name'],
                    "album": friend['track']['album']['name'],
                    "artist": friend['track']['artist']['name'],
                    "track_uri": friend['track']['uri'],
                    "album_uri": friend['track']['album']['uri'],
                    "seconds_since_last_update": int((current_epoch_time_in_ms - friend['timestamp']) / 1000)
                    }
                logger.info(friend)
                return friend_activity

        logger.error(f"No user {friend_name} found on friends acitivity.")

