import base64
from requests.models import PreparedRequest


def encodeAuthorization():
    # your secret key and client id
    auth = "" + ""
    auth_bytes = auth.encode("ascii")
    base64_bytes = base64.b64encode(auth_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


def prepareUrl():
    req = PreparedRequest()
    url = "https://accounts.spotify.com/authorize?"
    params = {"response_type": 'code',
              "client_id": "", # your client id
              "scope": "user-read-private user-read-email playlist-modify-public user-top-read",
              "redirect_uri": "http://127.0.0.1:5000/createAccount",
              "state": "securestatecode"}
    req.prepare_url(url, params)
    return req.url
