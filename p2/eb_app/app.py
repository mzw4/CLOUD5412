from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
  #Set application.debug=true to enable tracebacks on Beanstalk log output. 
  #Make sure to remove this line before deploying to production.
  app.debug = True
  app.run()