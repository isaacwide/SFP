from flask import Flask, render_template, request, send_file
from io import BytesIO, StringIO
import base64
import random
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fuctions import bernuli, exponencial, multinomial, norm, simulacion_binomial

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bernoulli', methods=['GET', 'POST'])
def bernoulli():
    # Valores por defecto
    theta = 0.3
    n = 10000
    
    # valores del usuario
    if request.method == 'POST':
        theta = float(request.form.get('theta', 0.3))
        n = int(request.form.get('n', 10000))
    
    soles, aguilas, secuencia = bernuli.simBernoulli(theta=theta, n=n)
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
    
    # Crear datos para descarga
    datos_descarga = "\n".join([f"Experimento {i+1}: {'Sol' if x == 1 else 'Águila'}" for i, x in enumerate(secuencia)])
    
    return render_template('resultado.html', 
                         titulo='Distribución de Bernoulli',
                         soles=soles, 
                         aguilas=aguilas,
                         imagen=img_str,
                         distribucion='bernoulli',
                         theta=theta,
                         n=n,
                         datos_descarga=datos_descarga)

@app.route('/exponencial', methods=['GET', 'POST'])
def exponential():
    # Valores por defecto
    lmbda = 0.5
    n = 100
    
    # valores del usuario
    if request.method == 'POST':
        lmbda = float(request.form.get('lambda', 0.5))
        n = int(request.form.get('n', 100))
    
    valores = exponencial.simExponencial(lmbda=lmbda, n=n)

    # Generar la imagen 
    plt.figure()
    fig, ax = plt.subplots()
    ax.hist(valores, bins=20, edgecolor='black', density=True)  
    plt.title(f'Distribución Exponencial (λ={lmbda}, n={n})')
    plt.xlabel('Valores')
    plt.ylabel('Frecuencia relativa')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    img_str = base64.b64encode(img.getvalue()).decode('ascii')

    # Crear datos para descarga
    datos_descarga = "\n".join([f"Muestra {i+1}: {x}" for i, x in enumerate(valores)])

    return render_template('resultado.html',
                         titulo='Distribución Exponencial',
                         imagen=img_str,
                         distribucion='exponencial',
                         lmbda=lmbda,
                         n=n,
                         datos_descarga=datos_descarga)

@app.route('/multinomial', methods=['GET', 'POST'])
def multi():
    # Valores por defecto
    n = 10000
    caras = 5
    uniforme = False
    # valores del usuario
    if request.method == 'POST':
        n = int(request.form.get('n', 10000))
        caras = int(request.form.get('caras', 5))
        uniforme = request.form.get('uniforme') == '1'

    histograma, secuencia , probabilidades= multinomial.simMultinomial(n=n, rangos=caras, uniforme=uniforme)
    
    # Generar la imagen del histograma
    plt.figure()
    fig, ax = plt.subplots()
    ax.bar(x=range(len(histograma)), height=histograma)
    ax.set_xlabel('Cara del dado')
    ax.set_ylabel('Frecuencia')
    ax.set_xticks(range(len(histograma)))
    ax.set_xticklabels([f' {i+1}' for i in range(len(histograma))])
    plt.title(f'Distribución Multinomial ({caras} caras, n={n})')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    img_str = base64.b64encode(img.getvalue()).decode('ascii')

    # Crear datos para descarga
    # Guardar también las probabilidades
    datos_probabilidades = "Probabilidades:\n" + ", ".join([f"Cara {i+1}: {p:.4f}" for i, p in enumerate(probabilidades)])
    datos_lanzamientos = "\n".join([f"Lanzamiento {i+1}: Cara {resultado+1}" for i, resultado in enumerate(secuencia)])
    datos_descarga = datos_probabilidades + "\n\n" + datos_lanzamientos

    return render_template('resultado.html',
                         titulo='Distribución Multinomial',
                         datos=histograma,
                         imagen=img_str,
                         distribucion='multinomial',
                         n=n,
                         caras=caras,
                         uniforme=uniforme,
                         datos_descarga=datos_descarga)

@app.route('/binomial', methods=['GET', 'POST'])
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
    
    histograma, promedio, secuencia = simulacion_binomial.simBinomial(theta=theta, lanzamientos=lanzamientos, repeticiones=repeticiones)
    
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

    # Crear datos para descarga
    datos_descarga = "\n".join([f"Experimento {i+1}: {exitos} éxitos" for i, exitos in enumerate(secuencia)])

    return render_template('resultado.html',
                         titulo='Distribución Binomial',
                         promedio=round(promedio, 2),
                         total_simulaciones=len(histograma),
                         imagen=img_str,
                         distribucion='binomial',
                         theta=theta,
                         lanzamientos=lanzamientos,
                         repeticiones=repeticiones,
                         datos_descarga=datos_descarga)

@app.route('/normal', methods=['GET', 'POST'])
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

    valores = norm.normalEstandar(repeticiones, miu, sigma)
    plt.figure()
    fig, ax = plt.subplots()
    ax.hist(valores, bins=50, edgecolor="black", density=True)
    ax.set_xlabel("Valores simulados")
    ax.set_ylabel("Frecuencia relativa")
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close() 

    img_str = base64.b64encode(img.getvalue()).decode('ascii')

    # Crear datos para descarga
    datos_descarga = "\n".join([f"Muestra {i+1}: {x}" for i, x in enumerate(valores)])

    return render_template('resultado.html',
                         titulo='Distribución Normal',
                         imagen=img_str,
                         distribucion='normal',
                         miu=miu,
                         sigma=sigma,
                         datos_descarga=datos_descarga)

@app.route('/gebbs', methods=['GET', 'POST'])
def gebbs_method():
    return render_template('grafic3d.html',
                         titulo='Método de Gebbs',
                         distribucion='gebbs')


@app.route('/normal_2', methods=['GET', 'POST'])
def normal_2():
    return render_template('grafic3d.html',
                         titulo='Normal en 2 variables',
                         distribucion='2normal')


@app.route('/descargar_datos/<distribucion>', methods=['POST'])
def descargar_datos(distribucion):
    datos = request.form.get('datos', '')
    filename = f"simulacion_{distribucion}.txt"
    
    # Crear archivo en memoria
    file_obj = StringIO()
    file_obj.write(datos)
    file_obj.seek(0)
    
    return send_file(
        BytesIO(file_obj.getvalue().encode('utf-8')),
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)