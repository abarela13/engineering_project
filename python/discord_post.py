import requests
import json

def get_webhooks(path):
    with open(path) as f:
        return json.load(f)

def discord_webhook_post(channel, series, link, vendor, name, image):
    hooks = get_webhooks('.secret/discord_webhooks.json')

    # https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {
        "content": f"@{series}"
    }

    # https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [
        {
            "url": link,
            "description": vendor,
            "title": name,
            "image": {
                "url": image
            }
        }
    ]

    result = requests.post(hooks[channel], json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))