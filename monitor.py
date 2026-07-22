import os
import json
import requests

TWITCH_CLIENT_ID = os.environ["TWITCH_CLIENT_ID"]
TWITCH_CLIENT_SECRET = os.environ["TWITCH_CLIENT_SECRET"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
STREAMER_NAME = os.environ["STREAMER_NAME"].lower().strip()

STATE_FILE = "state.json"

def get_twitch_token():
    url = "https://id.twitch.tv/oauth2/token"
    payload = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    res = requests.post(url, data=payload)
    res.raise_for_status()
    return res.json()["access_token"]

def get_stream_info(token):
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.twitch.tv/helix/streams?user_login={STREAMER_NAME}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    data = res.json().get("data", [])
    if data:
        return {
            "is_live": True,
            "game_name": data[0]["game_name"],
            "title": data[0]["title"],
            "display_name": data[0]["user_name"]
        }
    return {"is_live": False, "game_name": "", "title": "", "display_name": STREAMER_NAME}

def read_state():
    default_state = {"last_game": None, "is_live": False}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    default_state.update(data)
        except Exception:
            pass
    return default_state

def write_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def main():
    token = get_twitch_token()
    current = get_stream_info(token)
    state = read_state()

    if current["is_live"]:
      if state.get("last_game") != current["game_name"]:
            payload = {
                "content": "<@704476478842077185>",
                "embeds": [{
                    "title": f"🎮 {current['display_name']} changed category!",
                    "description": f"**New Category:** {current['game_name']}\n**Stream Title:** {current['title']}",
                    "url": f"https://twitch.tv/{STREAMER_NAME}",
                    "color": 9127187
                }]
            }
            requests.post(DISCORD_WEBHOOK_URL, json=payload)
            state["last_game"] = current["game_name"]
            state["is_live"] = True
    else:
        state["last_game"] = None
        state["is_live"] = False

    write_state(state)

if __name__ == "__main__":
    main()
