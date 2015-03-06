
================================================
                    Overview
================================================

The server and client are both written in Python using the
Flask microframework, and requests library.

The database is implemented using Amazon's SimpleDB.
Amazon's Boto API is used to interface with SimpleDB.


================================================
                      Setup
================================================

Dependencies (all can be installed using pip):
Flask==0.9
requests==2.4.3
boto==2.36.0

ie.
$ pip install boto

================================================
              Running the program
================================================

To run the server, simply open a terminal window and run the command:

$ python application.py

This will start a local web server.


Similarly, to run the client, run the command:

$ python client.py

You will be prompted with the parameters to make queries to the web server.