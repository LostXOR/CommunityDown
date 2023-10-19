import requests, json
from base64 import b64encode

channelID = "UCTkXRDQl0luXxVQrRQvWS6w"
zyphID = "UCPXGFu34px86DdXwocV-bYA"

firstPagePayload = b"\x12\x09community\xf2\x06\x04\x0a\x02\x4a\x00"
firstPageJSON = {
    "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
    "browseId": channelID, "params": b64encode(firstPagePayload).decode()
}
response = requests.post(
    "https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
    headers = {"Content-Type": "application/json"},
    data = json.dumps(firstPageJSON))
responseJSON = response.json()

print(json.dumps(responseJSON))
