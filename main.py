import requests, json
from base64 import b64encode

channelID = "UCTkXRDQl0luXxVQrRQvWS6w"
zyphID = "UCPXGFu34px86DdXwocV-bYA"
hexPayload = "1209" + "community".encode("utf-8").hex() + "f206040a024a00"


dataInitial = {"context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
    "browseId": channelID,
    "params": b64encode(bytes.fromhex(hexPayload)).decode()
}
response = requests.post(
    "https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
    headers = {"Content-Type": "application/json"},
    data = json.dumps(dataInitial))
responseJSON = response.json()

print(json.dumps(responseJSON))
"""
dataCont = {
    "context": {"client": {"clientName": "WEB", "clientVersion": "2.20231016"}},
    "browseId": channelID,
    "continuation": b64encode(bytes.fromhex(cont1Payload)).decode()
}
response = requests.post(
    "https://www.youtube.com/youtubei/v1/browse?prettyprint=false",
    headers = {"Content-Type": "application/json"},
    data = json.dumps(dataCont))
"""

"""
cont1Payload = (
    "e2a985b2028d011218" +
    channelID.encode("utf-8").hex() +
    "1a58" +
    b64encode(bytes.fromhex(
        "1209" +
        "community".encode("utf-8").hex() +
        "aa03280a245132684352465272546e646b4d477853556a425754564a496244566a4d565a4452554642280a" +
        "f206040a024a00"
    )).decode().replace("=", "%3D").encode("utf-8").hex() +
    "9a0216" +
    "backstage-item-section".encode("utf-8").hex()
)
cont2Payload = (
    "e2a985b2028d011218" +
    channelID.encode("utf-8").hex() +
    "1a58" +
    b64encode(bytes.fromhex(
        "1209" +
        "community".encode("utf-8").hex() +
        "aa03280a245132684352465646556c4a694d317075556d7457536c4a47634735594d6a6c45525546422813" +
        "f206040a024a00"
    )).decode().replace("=", "%3D").encode("utf-8").hex() +
    "9a0216" +
    "backstage-item-section".encode("utf-8").hex()
)
"""
