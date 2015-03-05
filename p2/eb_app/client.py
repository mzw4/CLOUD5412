import requests

server url = 'www.google.com'
username 'maverickmonkey'
netid = 'mzw4'
password = 'prancinglemur'
starting number = 1
ending number = 100


r = requests.get('https://server/register', auth=('user', 'pass'))
r = requests.get('https://server/login', auth=('user', 'pass'))
r = requests.get('https://server/query', auth=('user', 'pass'))
r = requests.get('https://server/logout', auth=('user', 'pass'))
r.status_code
r.headers['content-type']
r.encoding
r.text
r.json()

