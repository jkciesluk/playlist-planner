import flask
import json
import requests
from flask import redirect, request, session, url_for
from application.project import Route
from application.utils import encodeAuthorization, prepareUrl



app = flask.Flask(__name__)
app.config["DEBUG"] = True

# dostanie login i haslo do konta
# redirect do strony spotify do zalogowania
# wymagane parametry: client_id, response_type, redirect_uri, scope, state
@app.route('/register', methods=['GET', 'POST'])
def register(): 
  if request.method == 'POST':
    session['username'] = request.form['username']
    redirect(prepareUrl())
  return '''
    <form method="post">
        Login<p><input type=text name=username>
        <p><input type=submit value=Login>
    </form>
    '''


# dostanie od spotify code i state
# ma wyslac request do spotify po access token
# parametry: grant_type, code, redirect_uri
# headery: Authorisation, Content-Type
# dostaniemy jsona z min accessTokenem
# zapisujemy ten access token do bazy danych  
@app.route('/createAccount', methods=['GET, POST, PUT'])
def createAccount(): 
  args = request.args
  code = args.get('code')
  state = args.get('state')
  if(state == "abbaabbaabbaabba"):
    body = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': "http://127.0.0.1:5000/createAccount"}
    headers = {'Authorization': f'Basic {encodeAuthorization()}',
               'Content-Type': 'application/x-www-form-urlencoded'}
    url = "https://accounts.spotify.com/authorize?"
    
    result = requests.post(url, headers=headers, data=body)
    jsonResult = json.loads(result.text)
    # dodaj do DB accessToken dla danego użytkownika - jsonResult['access_token'], razem z waznoscia jego tokenu
      


@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return '<'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


def refreshToken():
  # jesli token jest niewazny
  # wysylamy do Spotify request z tokenem
  # dostajemy nowy token
  # zapisujemy go do DB razem z waznoscia
  pass

app.run()
"""
Plan jest taki:
 - w pythonie pisze API
 - apka w js, input fields z opcjami trasy itd
 - wysylam request do pythona z startem i końcem
 - python zwaraca mi:
  a) trase która wyswietlam na mapie + spis punktow, piosenki ze spotify, playliste
  b) tylko spis punktów i playliste, a trase tutaj obliczam po raz drugi
  (raczej wybiore B, przynajmniej chwilowo)
 - W PRZYPADKU WYBORU A:
  - dostaje liste z koordami punktów i aktualnie lecaca piosenka
  - dodaje na mape pushpiny w kazdym z tych punktów, z infoboxem pod którym bedzie dana piosenka
 - gdzies jeszcze umieszcze cala playliste
 - byc moze z logowaniem sie do spotify? (to by bylo bardzo git, chyba tak zrobie)
 
"""