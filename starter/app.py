"""Flask application entry point for the Sudoku game."""

from flask import Flask

from sudoku_blueprint import bp

app = Flask(__name__)
app.register_blueprint(bp)


if __name__ == '__main__':
    app.run(debug=True)