from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO
from flask_cors import CORS
import os,base64,random
from fuctions import bernuli,exponencial, multinomial, simulacion_binomial # importa las funciones des la carpeta fuctions

app = Flask(__name__)
CORS(app)
## cometario deben de crear los inputs en el html y mandar los parametros a las funciones desde aca 
##para llmar algo del html aca se usa request.form['nombre del input']
##debende importar request de flask
##los metodos get y post son para mandar datos desde el html al servidor o recibir datos del servidor al html

## esta es la ruta principal que carga el index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bernoulli',methods=['GET', 'POST'])
def bernoulli():
    #introducir theta como parametro
    soles, aguilas = bernuli.simBernoulli(theta=0.3,n=10000)
    par = [soles, aguilas]

    # guardar la imagen en memoria
    # Crear el gráfico
    plt.figure()
    fig, ax = plt.subplots()
    ax.bar(x=range(len(par)), height=par)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Soles', 'Águilas'])
    plt.title('Distribución de Bernoulli')      
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
            
    img_str = base64.b64encode(img.getvalue()).decode('ascii')
    
    return render_template('resultado.html', 
                         titulo='Distribución de Bernoulli',
                         soles=soles, 
                         aguilas=aguilas,
                         imagen=img_str)



@app.route('/exponencial',methods=['GET', 'POST'])
def exponential():
    #introducir lmbda y n como parametros
    ns= exponencial.simExponencial(lmbda=0.5,n=100)

    #generamos la imagen 
    plt.figure()
    fig, ax = plt.subplots()
    ax.hist(ns, bins=20, edgecolor='black', density=True)  
    plt.title('Distribución Exponencial')
    plt.xlabel('Valores')
    plt.ylabel('Frecuencia relativa')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    img_str = base64.b64encode(img.getvalue()).decode('ascii')

    return render_template('resultado.html',
                         titulo='Distribución Exponencial ', 
                         ns='aguilas',
                         imagen= img_str)


@app.route('/multinomial',methods=['GET', 'POST'])
def multi():
    #esta parte el usuario ingresa la cantidad de simulaciones y los rangos
    histograma = multinomial.simMultinomial(n=10000,rangos = [random.uniform(0,1) for _ in range(5)])
    #generamos la imagen del histograma
    plt.figure()
    fig, ax = plt.subplots()
    ax.bar(x=range(len(histograma)), height=histograma)
    ax.set_xlabel('Cara del dado')
    ax.set_ylabel('Frecuencia')
    ax.set_xticks(range(6))
    ax.set_xticklabels([f'Cara {i+1}' for i in range(6)])
    plt.title('Distribución Multinomial (Dado)')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    img_str = base64.b64encode(img.getvalue()).decode('ascii')


    return render_template('resultado.html',
                         titulo='Distribución Multinomial',
                         datos=histograma,
                         imagen=img_str)



@app.route('/binomial',methods=['GET', 'POST'])
def binomial():
    #introducir theta, lanzamientos y repeticiones como parametros
    histograma, promedio = simulacion_binomial.simBinomial(theta=0.7,lanzamientos=10,repeticiones=1000)
    #generamos la imagen del histograma
     # Crear el gráfico
    plt.figure()
    fig, ax = plt.subplots()
    ax.hist(histograma, bins=20, edgecolor="black", density=True)
    ax.set_xlabel("Número de soles (éxitos)")
    ax.set_ylabel("Frecuencia relativa")
    plt.title('Distribución Binomial')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()


    img_str = base64.b64encode(img.getvalue()).decode('ascii')

    return render_template('resultado.html',
                         titulo='Distribución Binomial',
                         promedio=round(promedio, 2),
                         total_simulaciones=len(histograma),
                         imagen=img_str)

if __name__ == '__main__':
    app.run(debug=True,port=8080)