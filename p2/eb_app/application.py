import os, boto.sdb, requests
from flask import Flask, request, session, make_response

from flask import redirect, url_for

# ===========================================================================
#                                   Constants
# ===========================================================================

MAX_TRIES = 10

# ===========================================================================
#                                     Init
# ===========================================================================

application = Flask(__name__)

# app secret key for secret things
application.secret_key = os.urandom(24).encode('hex')

#Set application.debug=true to enable tracebacks on Beanstalk log output. 
#Make sure to remove this line before deploying to production.
application.debug=True

# Set up simpledb
conn = boto.sdb.connect_to_region(
    'us-west-2',
    aws_access_key_id='AKIAI25ZHWR5Y3RJZLMA',
    aws_secret_access_key='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')

# create user domain
try:
    conn.delete_domain('users')
    users = conn.create_domain('users')
except:
    users = conn.create_domain('users')

# ===========================================================================
#                                     Routes
# ===========================================================================

@application.route('/')
def main():
  return "Congratulations! You have arrived at a page that does absolutely nothing."

@application.route('/register', methods=['POST'])
def register():
  if request.method == 'POST':
    username = request.args.get('username')

    netid = request.args.get('netid')
    password = request.args.get('password')

    user = find(users, username)
    if user:
      return 'Username already taken.'

    users.put_attributes(username, { 'netid': netid, 'password': password })
    print 'User ' + username + ' registered!'
    return "success"
  return 'Invalid request type'

@application.route('/login', methods=['POST'])
def login():
  if request.method != 'POST':
    return 'Invalid request'
  if 'username' not in request.args or 'password' not in request.args:
    return 'Invalid user info'

  # check if the user info is correct
  username = request.args.get('username')
  password = request.args.get('password')

  user = find(users, username)
  if not user or user['password'] != password:
    return 'Incorrect username or password'

  # log the user in
  session['username'] = username
  print username + ' logged in!'
  return 'success'

@application.route('/query', methods=['GET'])
def query():
  if request.method != 'GET':
    return 'Invalid request'

  # ensure that the user is logged in
  if 'username' not in session:
    return 'Permission denied. You must log in or send me a very large sum of money.'

  # validate number
  n = request.args.get('number')
  num = validate_int(n)
  if not num:
    return 'Invalid input. Int plz!'

  # print 'Checking primality of number...'
  return str(is_prime(num))

@application.route('/logout', methods=['POST'])
def logout():
  if request.method != 'POST':
    return 'Invalid request'
  # print session['username']
  # remove the username from the session if it's there
  if not session.pop('username', None):
    return 'Could not log out. Invalid user.'
  print 'User logged out.'
  return 'success'

"""
Perform a get operation in simpledb
Try MAX_TRIES times since sometimes it doesn't update fast enough.
"""
def find(domain, item_name):
  item = None
  tries = 0
  while not item and tries < MAX_TRIES:
    item = domain.get_item(item_name)
    tries += 1
  return item

"""
Determine if n is an integer or not
"""
def validate_int(n):
  try:
    return int(n)
  except ValueError:
    return None

"""
Determines if a number is prime or not.

Source:
"Primality Test" Wikipedia, The Free Encyclopedia. Wikimedia Foundation, Inc. 25 Feb 2015. Web. 5 March 2015.
"""
def is_prime(n):
    if n <= 3:
        return n >= 2
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(n ** 0.5) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

# ===========================================================================
#                                     Main
# ===========================================================================

if __name__ == '__main__':
  # application.run(host='0.0.0.0')
  application.run()


