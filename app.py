from flask import Flask, render_template, request
import matplotlib.pyplot as plt
from io import BytesIO
from flask_cors import CORS
import os,base64,random
from fuctions import bernuli,exponencial, multinomial, norm, simulacion_binomial,norm  # importa las funciones des la carpeta fuctions

app = Flask(__name__)
CORS(app)
## cometario deben de crear los inputs en el html y mandar los parametros a las funciones desde aca 
##para llmar algo del html aca se usa request.form['nombre del input']
##debende importar request de flask
##los metodos get y post son para mandar datos desde el html al servidor o recibir datos del servidor al html


app = Flask(__name__)
CORS(app)

## esta es la ruta principal que carga el index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bernoulli',methods=['GET', 'POST'])
def bernoulli():
    # Valores por defecto
    theta = 0.3
    n = 10000
    
    # valores del usuario
    if request.method == 'POST':
        theta = float(request.form.get('theta', 0.3))
        n = int(request.form.get('n', 10000))
    
    soles, aguilas = bernuli.simBernoulli(theta=theta, n=n)
    par = [soles, aguilas]

    # Crear el gráfico
    plt.figure()
    fig, ax = plt.subplots()
    ax.bar(x=range(len(par)), height=par)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Soles', 'Águilas'])
    plt.title(f'Distribución de Bernoulli (θ={theta}, n={n})')      
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
            
    img_str = base64.b64encode(img.getvalue()).decode('ascii')
    
    return render_template('resultado.html', 
                         titulo='Distribución de Bernoulli',
                         soles=soles, 
                         aguilas=aguilas,
                         imagen=img_str,
                         distribucion='bernoulli',
                         theta=theta,
                         n=n)

@app.route('/exponencial',methods=['GET', 'POST'])
def exponential():
    # Valores por defecto
    lmbda = 0.5
    n = 100
    
    # valores del usuario
    if request.method == 'POST':
        lmbda = float(request.form.get('lambda', 0.5))
        n = int(request.form.get('n', 100))
    
    ns = exponencial.simExponencial(lmbda=lmbda, n=n)

    # Generar la imagen 
    plt.figure()
    fig, ax = plt.subplots()
    ax.hist(ns, bins=20, edgecolor='black', density=True)  
    plt.title(f'Distribución Exponencial (λ={lmbda}, n={n})')
    plt.xlabel('Valores')
    plt.ylabel('Frecuencia relativa')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    img_str = base64.b64encode(img.getvalue()).decode('ascii')

    return render_template('resultado.html',
                         titulo='Distribución Exponencial',
                         imagen=img_str,
                         distribucion='exponencial',
                         lmbda=lmbda,
                         n=n)

@app.route('/multinomial',methods=['GET', 'POST'])
def multi():
    # Valores por defecto
    n = 10000
    caras = 5
    
    # valores del usuario
    if request.method == 'POST':
        n = int(request.form.get('n', 10000))
        caras = int(request.form.get('caras', 5))
    
    # Generar rangos aleatorios para las probabilidades
    rangos = [random.uniform(0,1) for _ in range(caras)]
    histograma = multinomial.simMultinomial(n=n, rangos=rangos)
    
    # Generar la imagen del histograma
    plt.figure()
    fig, ax = plt.subplots()
    ax.bar(x=range(len(histograma)), height=histograma)
    ax.set_xlabel('Cara del dado')
    ax.set_ylabel('Frecuencia')
    ax.set_xticks(range(len(histograma)))
    ax.set_xticklabels([f'Cara {i+1}' for i in range(len(histograma))])
    plt.title(f'Distribución Multinomial ({caras} caras, n={n})')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    img_str = base64.b64encode(img.getvalue()).decode('ascii')

    return render_template('resultado.html',
                         titulo='Distribución Multinomial',
                         datos=histograma,
                         imagen=img_str,
                         distribucion='multinomial',
                         n=n,
                         caras=caras)

@app.route('/binomial',methods=['GET', 'POST'])
def binomial():
    # Valores por defecto
    theta = 0.7
    lanzamientos = 10
    repeticiones = 1000
    
    # valores del usuario
    if request.method == 'POST':
        theta = float(request.form.get('theta', 0.7))
        lanzamientos = int(request.form.get('lanzamientos', 10))
        repeticiones = int(request.form.get('repeticiones', 1000))
    
    histograma, promedio = simulacion_binomial.simBinomial(theta=theta, lanzamientos=lanzamientos, repeticiones=repeticiones)
    
    # Crear el gráfico
    plt.figure()
    fig, ax = plt.subplots()
    ax.hist(histograma, bins=20, edgecolor="black", density=True)
    ax.set_xlabel("Número de soles (éxitos)")
    ax.set_ylabel("Frecuencia relativa")
    plt.title(f'Distribución Binomial (θ={theta}, n={lanzamientos}, rep={repeticiones})')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    img_str = base64.b64encode(img.getvalue()).decode('ascii')

    return render_template('resultado.html',
                         titulo='Distribución Binomial',
                         promedio=round(promedio, 2),
                         total_simulaciones=len(histograma),
                         imagen=img_str,
                         distribucion='binomial',
                         theta=theta,
                         lanzamientos=lanzamientos,
                         repeticiones=repeticiones)

@app.route('/normal',methods=['GET', 'POST'])
def normal():
    #valor por defecto 
    repeticiones = 100
    miu = 0
    sigma = 1
    if request.method == 'POST':
        repeticiones = int(request.form.get('repeticiones', 100))
        miu = float(request.form.get('miu'))
        sigma = float(request.form.get('sigma'))

    if sigma <= 0:
        sigma = 1

    valores = norm.normalEstandar(repeticiones,miu,sigma)
    plt.figure()
    fig, ax = plt.subplots()
    fig, ax = plt.subplots()
    ax.hist(valores, bins=50, edgecolor="black", density=True)
    ax.set_xlabel("Valores simulados (N(0,1))")
    ax.set_ylabel("Frecuencia relativa")
    plt.show()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close() 

    img_str = base64.b64encode(img.getvalue()).decode('ascii')

    return render_template('resultado.html',
                         titulo='Distribución Normal',
                         imagen=img_str,
                         distribucion='normal',
                         miu=miu,
                        sigma=sigma,
                         )


@app.route('/gebbs',methods=['GET', 'POST'])
def gebbs_method():
    return render_template('grafic3d.html',
                         titulo='Método de Gebbs',
                         distribucion='gebbs',
                         )

if __name__ == '__main__':
    app.run(debug=True,port=8080)