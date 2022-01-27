import requests

from flask import redirect, request, session, url_for, render_template, make_response
from datetime import datetime, timedelta
from flask import current_app as app
from .project import Route, MyMap, PlaylistForRoute
from .spotify import Spotify
from .utils import encodeAuthorization, prepareUrl
from .models import User, Token, db

# dostanie login i haslo do konta
# redirect do strony spotify do zalogowania
# wymagane parametry: client_id, response_type, redirect_uri, scope, state
@app.route('/register', methods=['GET', 'POST'])
def register(): 
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm']
    if(not (password == confirm)):
      return "Passwords dont match"

    existing_user = User.query.filter(
        User.username == username
    ).first()
    if existing_user:
      return make_response(f'{username} already created!')
    
    new_user = User(
      username=username,
      created_on=datetime.now(),
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()    
    session['username'] = username
    return redirect(prepareUrl())
  return '''
    <form method="post">
        Login<p><input type=text name=username>
        Password<p><input type=password name=password>
        Confirm Password<p><input type=password name=confirm>
        <p><input type=submit value=Register>
    </form>
    '''

# dostanie od spotify code i state
# ma wyslac request do spotify po access token
# parametry: grant_type, code, redirect_uri
# headery: Authorisation, Content-Type
# dostaniemy jsona z min accessTokenem
# zapisujemy ten access token do bazy danych  
@app.route('/createAccount', methods=['GET'])
def createAccount():
  args = request.args
  code = args.get('code')
  state = args.get('state')
  if(state == "abbaabbaabbaabba"):
    body = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': "http://127.0.0.1:5000/createAccount"}
    headers = {'Authorization': f'Basic {encodeAuthorization()}',
               'Content-Type': 'application/x-www-form-urlencoded'}
    url = "https://accounts.spotify.com/api/token"
    
    result = requests.post(url, headers=headers, data=body)
    jsonResult = result.json()
    # dodaj do DB accessToken dla danego użytkownika - jsonResult['access_token'], razem z waznoscia jego tokenu
    owner = User.query.filter_by(username=session['username']).first()
    token = Token(
      access_token=jsonResult['access_token'],
      expiration=datetime.now() + timedelta(seconds=3600),
      refresh_token=jsonResult['refresh_token'], # TODO: sprawdzic czy taki jest response
      owner = owner,
      owner_id = owner.id
    )
    db.session.add(token)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    start = request.form['start']
    end = request.form['end']
    map = MyMap()
    route = map.getRouteData(start, end)
    user = User.query.filter_by(username = session['username']).first()
    user_id = user.id
    token = Token.query.filter_by(owner_id = user_id).first()
    
    if(token.expiration < datetime.now()):
      refToken = token.refresh_token
      accessToken = refreshToken(user, refToken)
    else:
      accessToken = token.access_token
    spotifyClient = Spotify(accessToken)
    merged = PlaylistForRoute(route, spotifyClient, start, end)
    points = merged.createPlaylistForRoute()
    
    return render_template('index.html',
      start = start,
      end = end,
      points=points)
  
  elif 'username' in session:
    return '''
      <form method="post">
        Start<p><input type=text name=start>
        End<p><input type=text name=end>
        <p><input type=submit value=Login>
      </form>
    '''
  return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    session['username'] = request.form['username']
    return redirect(url_for('index'))
  return '''
      <form method="post">
        Login<p><input type=text name=username>
        Password<p><input type=text name=password>
        <p><input type=submit value=Login>
      </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


def refreshToken(user, refresh_token):
  body = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
  headers = {'Authorization': f'Basic {encodeAuthorization()}',
              'Content-Type': 'application/x-www-form-urlencoded'}
  url = "https://accounts.spotify.com/api/token"
  
  result = requests.post(url, headers=headers, data=body)
  jsonResult = result.json()
  old_token = user.token
  new_token = Token(
      access_token=jsonResult['access_token'],
      expiration=datetime.now() + timedelta(seconds=3600),
      refresh_token=refresh_token, # TODO: sprawdzic czy taki jest response
      owner=user,
      owner_id = user.id
  )
  db.session.add(new_token)
  db.session.delete(old_token)
  return new_token.access_token



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