import sys, requests, json, math, re, time

# mapquest credentials
_mq_key = 'Fmjtd%7Cluu8216rll%2C8g%3Do5-942ngy' 
_mq_max_batch = 100

# diameter of the earth
_dia_miles = 3963.191
_dia_km = 6378.137

# restaurant db url
url = 'http://www.cs.cornell.edu/Courses/CS5412/2015sp/_cuonly/restaurants_all.csv'

# relevant regex
latlng_regex = re.compile('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$')
zip_regex = re.compile('(.*)\d{5}(?:[-\s]\d{4})?$')

db = ''
# connects the server to the db
def connect_db():
  global db
  print 'Downloading restaurant data files'
  # db = open('restaurants_all.csv', 'r')
  # db = db.read()

  response = requests.get(url, stream=True)
  total_length = int(response.headers.get('content-length'))
  print total_length

  if total_length is None: # no content length header
    print response.content
  else:
    dl = 0
    for data in response.iter_content(chunk_size=256):
      dl += len(data)
      db += data
      # print db
      percent = 100 * dl / total_length
      bars = int(50 * percent/100)
      sys.stdout.write("\r %s [%s%s] %s" % (percent, '=' * bars, ' ' * (50-bars), dl) )    
      sys.stdout.flush()

  # response = requests.get(url)
  # db = response.content

  return 'finished'

# find the nearest restaurants from the given address within the given distance in miles
def find_nearest(input_addr, distance_threshold):
  print 'Finding specified location...'
  start_t = time.time()

  # Geocode input address if necessary
  latlng = latlng_regex.match(input_addr)

  # form the request url
  # if the input is in lat/lng, use reverse geocoding
  # request_url = 'http://www.mapquestapi.com/geocoding/v1/' + \
  request_url = 'http://open.mapquestapi.com/geocoding/v1/' + \
    ('reverse' if latlng else 'address') + '?key=' + _mq_key + '&location=' + input_addr
  print request_url

  # make the request
  response = requests.get(request_url)
  print response.content
  response_json = json.loads(response.content)
  results = response_json['results']

  # get input zip code and latlng
  manual_zipcode = zip_regex.match(input_addr)
  input_zipcode = input_addr.split(',')[-1].split()[-1].split('-')[0] if manual_zipcode else None
  input_latlng = None

  if results and results[0]['locations']:
    input_latlng = results[0]['locations'][0]['latLng']
    input_zipcode = results[0]['locations'][0]['postalCode'].split('-')[0] # split to ignore sub codes
  else:
    print 'No matching locations found'
    return

  print input_addr, input_zipcode, input_latlng

  # Prepare to batch geocode restaurant addresses
  rcount = 0
  # orig_request_url = 'http://www.mapquestapi.com/geocoding/v1/batch?key=' + _mq_key + '&outFormat=json'
  orig_request_url = 'http://open.mapquestapi.com/geocoding/v1/batch?key=' + _mq_key + '&outFormat=json'
  request_url = orig_request_url

  # map of location -> restaurant data
  restaurant_loc_map = {}

  # map of location -> distance to input address
  distance_map = {}

  print 'Calculating restaurant distances...'
  for line in db.splitlines():
    restaurant = line.split(',')
    zipcode = restaurant[7]
    location = ', '.join(restaurant[4:8])
    restaurant_loc_map[location] = restaurant

    # only process restaurants with matching zip codes
    if zipcode == input_zipcode:
      rcount += 1
      request_url += '&location=' + location

    # check distances of processed addresses
    if rcount == _mq_max_batch:
      get_batch_restaurant_distances(request_url, distance_map, input_latlng)
      rcount = 0
      request_url = orig_request_url

  if rcount > 0:
    get_batch_restaurant_distances(request_url, distance_map, input_latlng)
  
  print 'Filtering results...'
  nearby_restaurants = {}
  for loc, (latlng, dist) in distance_map.items():
    if dist < distance_threshold:
      # print dist, restaurant_loc_map[loc][4:8], restaurant_loc_map[loc][3]
      name = restaurant_loc_map[loc][3]
      nearby_restaurants[name] = {'loc': loc, 'latlng': latlng, 'dist': dist}

  # print nearby_restaurants
  runtime = time.time() - start_t

  input_data = {'input_addr': input_addr, 'latlng': input_latlng, 'dist': distance_threshold, 'runtime': runtime}

  return input_data, nearby_restaurants

# perform batch request
def get_batch_restaurant_distances(request_url, distance_map, input_latlng):
  print '\tMaking batch geolocation request...'
  response = requests.get(request_url)
  response_json = json.loads(response.content)
  print response_json

  # record distances from each location to the input location
  for result in response_json['results']:
    loc = result['providedLocation']['location']
    print result['locations']
    if result['locations']:
      latlng = result['locations'][0]['latLng']
      distance_map[loc] = latlng, get_distance(latlng, input_latlng)

# compute the distance given latitude and longitude coordinate positions
def get_distance(latlng1, latlng2):
  lat1 = math.radians(latlng1['lat'])
  lng1 = math.radians(latlng1['lng'])
  lat2 = math.radians(latlng2['lat'])
  lng2 = math.radians(latlng2['lng'])

  dist = math.acos(
    math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lng1-lng2))
  return _dia_miles * dist

# format the results to the required output text format
def format_results(input_data, nearby_restaurants):
  output = ''
  output = input_data['input_addr'] + ' | ' + str(input_data['dist']) + ' miles | '\
    + str(input_data['runtime']) + ' seconds\n'
  for restaurant, data in nearby_restaurants.items():
    output += restaurant + ', ' + data['loc'] + ' | ' + str(data['dist']) + ' miles\n'
  return output


