# Necessarry imports 
from flask import Flask,render_template
from flask import session, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/team')
def team():
    return render_template('team.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run(debug=True)
