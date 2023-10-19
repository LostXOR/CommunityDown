import requests, json, re
from base64 import b64encode

channelID = "UCTkXRDQl0luXxVQrRQvWS6w"
zyphID = "UCPXGFu34px86DdXwocV-bYA"

# JSON data sent in POST to request community pages
# params is a magic string that's used to get the community tab, no idea what it's for
requestData = {
    "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
    "browseId": channelID, "params": "Egljb21tdW5pdHnyBgQKAkoA"
}

# Fetch community pages
newPage = True
while newPage:
    # Request community page from the API
    response = requests.post("https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
    headers = {"Content-Type": "application/json"}, data = json.dumps(requestData))

    # Get continuation data from response (regex is simpler than trying to parse the JSON)
    # Continuation data is a magic string we need to send the API to get the next page
    contMatch = re.findall('{"token": {0,1}".*?"}', response.text)
    if len(contMatch) == 1:
        requestData["continuation"] = json.loads(contMatch[0])["token"]
    else:
        newPage = False
