import subprocess

cred_file = open("client.secret", "r")
client_id, client_secret = cred_file.read().split(",")

url = "http://www.strava.com/oauth/authorize?\
client_id={client_id}&\
response_type=code&\
redirect_uri=http://localhost/exchange_token&approval_prompt=force&\
scope=read,read_all,activity:read_all,profile:read_all".format(client_id = client_id)

firefox_command = ["firefox", url]
subprocess.run(firefox_command)

