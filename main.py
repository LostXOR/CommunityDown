import requests, json, re
from base64 import b64encode

channelID = "UCTkXRDQl0luXxVQrRQvWS6w"
zyphID = "UCPXGFu34px86DdXwocV-bYA"

# Payload needed for request, contains arbitrary bytes of unknown origin
firstPagePayload = b"\x12\x09community\xf2\x06\x04\x0a\x02\x4a\x00"
# JSON data needed for request
firstPageJSON = {
    "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
    "browseId": channelID, "params": b64encode(firstPagePayload).decode()
}

# Request first page of community posts
response = requests.post(
    "https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
    headers = {"Content-Type": "application/json"},
    data = json.dumps(firstPageJSON))

while True:
    # Get continuation payload from response
    contMatch = re.findall('{"token": {0,1}".*?"}', response.text)
    if len(contMatch) != 1:
        break
    contPayload = json.loads(contMatch[0])["token"]
    print(contPayload)

    # JSON data needed for request
    contJSON = {
        "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
        "browseId": channelID, "continuation": contPayload
    }
    # Request next page of community posts
    response = requests.post(
        "https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
        headers = {"Content-Type": "application/json"},
        data = json.dumps(contJSON))
