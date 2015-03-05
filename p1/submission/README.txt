CS5412 Project 1
mzw4

* Note that the MapQuest API broke, and I'm using a new url 'open.mapquestapi', which takes much longer to run, and produces different results. The program will now work and produce results, but the results are not as comprehensive as before. The original results are shown in the output queries.txt and the screenshots of the maps for each query.

Program instructions:

=============================
          Web app
=============================

1. Dependencies:

Pip should be included with Python 2.7.9 and later

Flask - To install in a unix environment, use 
  $ pip install flask

  You can use virtualenv if desired.
  $ sudo pip install virtualenv

  For Windows or more details, see:
  http://flask.pocoo.org/docs/0.10/installation/

Requests - To install, run 
  $ pip install requests

__________________________________

2. Starting the server:

To start the server, navigate into the directory containing server.py and run
$ python server.py

This will start a local web server. The output on the cmd line will tell you which network address the server is running on. To access the web app, type the local network address into a web browser.

For example, if the web server is running on http://127.0.0.1:5000/, type that address into a web browser to view the app.

__________________________________

3. Usage:

Inputs:
  Location (string): an address or set of lat/lng coordinates
  Distance (number): a distance threshold in miles

The request may take some time to complete (typically 10-15 seconds).
Once completed, the results will be displayed on the left panel in a list form. The google map on the right will center itself to the input location and display nearby restaurants as markers. To view details of a restaurant, you may either click on the restaurant in the list, or click on the marker on the map.

To download the formatted results output, 'queries.txt' as specified in the project description, click the "Download formatted results" button at the bottom of the results panel. This file will be truncated each time the server is started.

To make another query, hit the back button. This will bring you back to the main input page.

=============================
      Cmd line interface
=============================

If the web app does not work, you can run the CLI provided by the cmd_test.py module. This module uses the same interface as the web app, so the results will be the same. You just won't get the revolutionary user interface from the web app.

1. Dependencies:

Pip should be included with Python 2.7.9 and later

Requests - To install, run 
  $ pip install requests

__________________________________

2. Execution:

To run the CLI, navigate to the directory containing cmd_test.py and run
$ python cmd_test.py

__________________________________

3. Usage:

The program will ask for an an input address, then a distance threshold. These inputs are the same as those for the web app.
Results will be printed in the cmd terminal in the correct format. However they will also be appended to the file 'queries.txt'. Again, this file wille be truncated each time the CLI is started.


