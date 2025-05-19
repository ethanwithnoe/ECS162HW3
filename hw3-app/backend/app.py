from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os

from flask import Flask, jsonify, send_from_directory, request
import requests
from flask_cors import CORS

from pymongo import MongoClient

static_path = os.getenv('STATIC_PATH','static')
template_path = os.getenv('TEMPLATE_PATH','templates')

app = Flask(__name__, static_folder=static_path, template_folder=template_path)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
comments_collection = db["comments"]


app.secret_key = os.urandom(24)


oauth = OAuth(app)

nonce = generate_token()


oauth.register(
    name=os.getenv('OIDC_CLIENT_NAME'),
    client_id=os.getenv('OIDC_CLIENT_ID'),
    client_secret=os.getenv('OIDC_CLIENT_SECRET'),
    #server_metadata_url='http://dex:5556/.well-known/openid-configuration',
    authorization_endpoint="http://localhost:5556/auth",
    token_endpoint="http://dex:5556/token",
    jwks_uri="http://dex:5556/keys",
    userinfo_endpoint="http://dex:5556/userinfo",
    device_authorization_endpoint="http://dex:5556/device/code",
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/')
def home():
    user = session.get('user')
    if user:
        redirect_uri = 'http://localhost:5173?user=' + str(user['email'])
        return redirect(redirect_uri)
        # return f"<h2>Logged in as {user['email']}</h2><a href='/logout'>Logout</a>"
    return '<a href="/login">Login with Dex</a>'

@app.route('/login')
def login():
    session['nonce'] = nonce
    redirect_uri = 'http://localhost:8000/authorize'
    return oauth.flask_app.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authorize')
def authorize():
    token = oauth.flask_app.authorize_access_token()
    nonce = session.get('nonce')

    user_info = oauth.flask_app.parse_id_token(token, nonce=nonce)  # or use .get('userinfo').json()
    session['user'] = user_info
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# @app.route('/api/key')
# def get_key():
#     return jsonify({'apiKey': os.getenv('NYT_API_KEY')})

@app.route('/api/comments', methods=['POST'])
def create_comment():
    data = request.json
    result = comments_collection.insert_one(data)
    return jsonify({"article_id": data.get("article_id"),
                    "comment_text": data.get("comment_text"),
                    "user": data.get("user"),
                    "inserted_id": str(result.inserted_id)}), 201

@app.route('/api/comments', methods=['GET'])
def get_comments():
    comments = list(comments_collection.find())
    for com in comments:
        com['_id'] = str(com['_id'])
    return jsonify(comments)

@app.route('/api/comments', methods=['DELETE'])
def delete_comment(comment):
    result = comments_collection.delete_one({"comment_text": comment})
    return jsonify({"deleted_count": result.deleted_count})

NYT_API_KEY = os.getenv('NYT_API_KEY')  

@app.route('/api/articles', methods=['GET'])
def getarticles():
    print("hello getarticles here")
    query = '"Davis CA""U.C. Davis"'
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={NYT_API_KEY}"

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "error"}), 500

    data = response.json()
    return jsonify(data), 200

@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path=''):
    if path != '' and os.path.exists(os.path.join(static_path,path)):
        return send_from_directory(static_path, path)
    return send_from_directory(template_path, 'index.html')

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)),debug=debug_mode)