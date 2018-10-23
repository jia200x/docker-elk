import urllib
import urllib2
from flask import Flask
import json
import requests
from flask import request as r
from uuid import uuid4

app = Flask(__name__)

def __get_gh_user(token):
    url = 'http://api.github.com/user?access_token={}'.format(token)
    try:
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        ret = data.get("login", None)
    except:
        ret = None
    return ret

@app.route('/', methods=['POST'])
def auth():
    content = r.get_json(silent=False)

    token = content.get("token", None)
    results = content.get("results", None)
    if not token or not results:
        return "Bad request", 400

    content.pop("token")
    user = __get_gh_user(token)
    if not user:
        return "Bad request", 400

    content.update({"user": user, "uuid": str(uuid4())})
    request = requests.post("http://logstash:5000", json.dumps(content), headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    return "OK"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
