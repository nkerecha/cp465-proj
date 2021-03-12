# Necessarry imports 
from flask import Flask,render_template
from flask import session, redirect, url_for, request
from data_etl import *
app = Flask(__name__)


@app.route('/')
def indexer():
    Pokemons =["jazz music", "hiphop music", "car price", "black widow",  
           "wakanda marvel", "drake music", "visa card", "mastercard cards", "credit cards", "samsung tv", "data definition"] 
  
    return render_template('index.html', len = len(Pokemons), Pokemons = Pokemons)


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/result',methods=["POST","GET"])
def result():
    if request.method=="POST":
        value = request.form.get('search-entry')
        print(value)
        _, _, _, res_no_op,num_records = runner(value)
        if res_no_op != None:
            return render_template('result.html',res = res_no_op, records=num_records, search_name=value)
        else:
            return render_template('result.html',res = ["No matching records"], records=0, search_name=value)


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(debug=True)
