import requests, time, sys

# ===========================================================================
#                                     Functions
# ===========================================================================

def register(username, netid, password):
  print 'Registering user ' + username + '...'
  payload = { 'username': username, 'netid': netid, 'password': password }
  r = requests.post(server_url + 'register', params=payload)
  if r.text == 'success':
    print 'User ' + username + ' registered.'
  else:
    print r.text

def login(username, password, session):
  print 'Loggin in ' + username + '...'
  payload = { 'username': username, 'password': password }
  r = session.post(server_url + 'login', params=payload)
  if r.text == 'success':
    print 'User ' + username + ' logged in.'
  else:
    print r.text

def query(n, session):
  payload = { 'number': n }
  r = session.get(server_url + 'query', params=payload)
  return r.text

def logout(session):
  print 'Logging out...'
  r = session.post(server_url + 'logout')
  if r.text == 'success':
    print 'Logged out!'
  else:
    print r.text

"""
Determine if n is an integer or not
"""
def validate_int(n):
  try:
    return int(n)
  except ValueError:
    return None

"""
Perform user query operations:
  - register user
  - log in
  - make queries
  - log out
  - reports stats
"""
def perform_queries(server_url, username, netid, password, start, end):
  print '----- Performing query operations -----'
  s = requests.Session()

  # validate input
  start_int = validate_int(start)
  end_int = validate_int(end)
  if (not start_int and start_int != 0) or (not end_int and end_int != 0):
    print 'Invalid input numbers'
    return

  # register user and log in
  register(username, netid, password)
  login(username, password, s)

  # keep track of query latencies and prime results
  latencies = []
  primes = []

  # check primes, skipping even numbers
  print 'Querying...'
  for i in range(start_int, end_int+1):
    if i % 2 == 0 and i != 2: continue
    success = False;
    while not success:
      start = time.time()
      prime = query(i, s)
      latency = time.time() - start
      if prime == 'True' or prime == 'False':
        success = True

    latencies.append(latency)
    primes.append((i, prime))

    # progress indicator
    percent = (float(i) - start_int)/(end_int - start_int)*100
    sys.stdout.write("\r Done: %s%% Current: %s" % ("{0:.2f}".format(percent), i))    
    sys.stdout.flush()

  logout(s)

  # report prime stats
  print '----- Prime number stats -----'
  print 'Total numbers checked: ' + str(len(primes))
  prime_count = zip(*primes)[1].count('True')
  percent = float(prime_count)/len(primes)*100
  print 'Num prime numbers: %s (%s%%)' % (prime_count, '{0:.2f}'.format(percent))

  # report latency stats
  if latencies:
    num_requests = len(latencies)
    latencies.sort()
    print '----- Latency stats -----'
    print 'Min: ' + str(latencies[0])
    print 'Max: ' + str(latencies[-1])
    print 'Mean: ' + str(sum(latencies)/num_requests)
    print 'Median: ' +\
      ( str(latencies[num_requests/2]) if (num_requests % 2 == 1 or num_requests < 2) else\
      str((latencies[num_requests/2 - 1] + latencies[num_requests/2])/2) )
  print '\n'

# ===========================================================================
#                                     Main
# ===========================================================================

while True:
  print '----- User inputs (Press enter for default) -----'
  server_url = raw_input('Server URL: ')
  username = raw_input('Username: ')
  netid = raw_input('netid: ')
  password = raw_input('Password: ')
  start = raw_input('Start query: ')
  end = raw_input('End query: ')

  # defaults
  if not server_url: server_url = 'http://primeapp-env.elasticbeanstalk.com/'
  # if not server_url: server_url = 'http://127.0.0.1:5000/'
  if not username: username = 'mikey'
  if not netid: netid = 'mzw4'
  if not password: password = 'omg'
  if not start: start = 1
  if not end: end = 100

  perform_queries(server_url, username, netid, password, start, end)

