from flask import Flask, render_template, url_for
import os

from bernuli import simBernoulli
from exponencial import simExponencial
from multinomial import simMultinomial
from simulacion_binomial import simBinomial

app = Flask(__name__)


if not os.path.exists('static/images'):
    os.makedirs('static/images')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bernoulli')
def bernoulli():
    soles, aguilas = simBernoulli()
    return render_template('resultado.html', 
                         titulo='Distribución de Bernoulli',
                         soles=soles, 
                         aguilas=aguilas,
                         imagen='bernoulli.png')

@app.route('/exponencial')
def exponencial():
    soles, aguilas = simExponencial()
    return render_template('resultado.html',
                         titulo='Distribución Exponencial ', 
                         soles=soles,
                         aguilas=aguilas,
                         imagen='exponencial.png')

@app.route('/multinomial')
def multinomial():
    histograma = simMultinomial()
    return render_template('resultado.html',
                         titulo='Distribución Multinomial',
                         datos=histograma,
                         imagen='multinomial.png')

@app.route('/binomial')
def binomial():
    histograma, promedio = simBinomial()
    return render_template('resultado.html',
                         titulo='Distribución Binomial',
                         promedio=round(promedio, 2),
                         total_simulaciones=len(histograma),
                         imagen='binomial.png')

if __name__ == '__main__':
    app.run(debug=True)