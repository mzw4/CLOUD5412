from finder.finder import find_nearest, format_results, connect_db

db = connect_db()

with open('queries.txt', 'w') as output:
  while True:
    address = raw_input('Find restaurants near:')
    distance = raw_input('Within (miles):')

    error = ''
    if not address:
      error = 'No input location!'
    elif not distance:
      error = 'No input distane!'
    else:
      try:
        float(distance)
      except ValueError:
        error = 'Distance must be a valid number!';

    if error:
      print error
    else:
      input_data, nearby_restaurants = find_nearest(address, distance)
      results = format_results(input_data, nearby_restaurants)

      output.write(results + '\n')
      print results