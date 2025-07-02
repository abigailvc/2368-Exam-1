# Initial setup for Troop API - CIS 2368 Exam 1
# Based on Flask structure from Homework 2 (Zoo API)

from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    return "Troop API is running"

if __name__ == '__main__':
    app.run()
