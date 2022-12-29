"""Application entry point"""
import flask
from dashapp import create_app

server = flask.Flask(__name__)

app = create_app(server)


if __name__ == "__main__":
    app.run(debug=False)

