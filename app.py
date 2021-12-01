import os, requests, json, logging

logging.basicConfig()  
logger=logging.getLogger()
logger.setLevel(logging.INFO)

SP_DC = os.environ['SP_DC']


def get_access_token(sp_dc_token) -> str:
    response = requests.get('https://open.spotify.com/get_access_token?reason=transport&productType=web_player',
                    headers={
                            'Content-Type':'application/json',
                            'Cookie': f'sp_dc={sp_dc_token}'
                            })
    content = json.loads(response.content)
    logger.debug(content)
    return content['accessToken']


def get_all_friends_activity_list(web_access_token) -> list:
    # Alternative url https://guc-spclient.spotify.com/presence-view/v1/buddylist
    response = requests.get("https://spclient.wg.spotify.com/presence-view/v1/buddylist",
                    headers={
                            'Content-Type':'application/json',
                            'Authorization': f'Bearer {web_access_token}'
                            })
    content = json.loads(response.content)
    return content['friends']


def get_friend_activity(friends_activity, friend_name):
    for friend in friends_activity:
        if friend['user']['name'] == friend_name:
            friend_activity = {
                "track": friend['track']['name'],
                "album": friend['track']['album']['name'],
                "artist": friend['track']['artist']['name']
                }
            logger.info(friend_activity)
            return friend_activity

    logger.error(f"No user {friend_name} found on friends acitivity.")


def main():
    web_access_token = get_access_token(SP_DC)
    friends_activity = get_all_friends_activity_list(web_access_token)
    print(get_friend_activity(friends_activity, "Vicente"))


if __name__ == "__main__":
    main()
