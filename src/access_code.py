import requests

auth_code_file = open("auth_code.secret", "r")
auth_code = auth_code_file.read().strip()
print(auth_code)

cred_file = open("client.secret", "r")
client_id, client_secret = cred_file.read().strip().split(",")

payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
        "grant_type": "authorization_code"
}

oauth_url = "https://www.strava.com/oauth/token"

oauth_response = requests.post(oauth_url, data=payload)
print(oauth_response.status_code)
print(oauth_response.text)
if (oauth_response.status_code == 200):
    oauth_json = oauth_response.json()
    expires_at = oauth_json["expires_at"]
    refresh_token = oauth_json["refresh_token"]
    access_token = oauth_json["access_token"]
    wf = open("access.secret", "w")
    wf.write(access_token)
    wf.write(",")
    wf.write(refresh_token)
    wf.write(",")
    wf.write(str(expires_at))
