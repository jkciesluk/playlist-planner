import base64
from requests.models import PreparedRequest
def encodeAuthorization():
    auth = "e892b60798b94c6b9d526a7e2f408be5:" + "572c283a63af4aef9e0bd0b283b8081c"
    auth_bytes = auth.encode("ascii")
    base64_bytes = base64.b64encode(auth_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def prepareUrl():
  req = PreparedRequest()
  url = "https://accounts.spotify.com/authorize?"
  params = {"response_type": 'code',
    "client_id": "e892b60798b94c6b9d526a7e2f408be5",
    "scope": "user-read-private user-read-email",
    "redirect_uri": "http://127.0.0.1:5000/createAccount",
    "state": "abbaabbaabbaabba"}
  req.prepare_url(url, params)
  return req.url
