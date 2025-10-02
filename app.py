from flask import Flask, render_template, request, send_file
from io import BytesIO, StringIO
from flask_cors import CORS
import os   
import tempfile
import base64
import random
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fuctions import bernuli, exponencial, multinomial, norm, simulacion_binomial

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 
CORS(app) # Permitir CORS para todas las rutas

app.config['secret_key']='9f3a8b7c2d1e4f5a6b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bernoulli', methods=['GET', 'POST'])
def bernoulli():
    # Valores por defecto
    theta = 0.5
    n = 10000
    
    # valores del usuario
    if request.method == 'POST':
        theta = float(request.form.get('theta', 0.5))
        n = int(request.form.get('n', 10000))
    
    exitos, fracaso, secuencia = bernuli.simBernoulli(theta=theta, n=n)
    par = [exitos, fracaso]


    # Crear el grafico
    plt.figure()
    fig, ax = plt.subplots()
    ax.bar(x=range(len(par)), height=par)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Fracaso', 'Exitos'])
    plt.title(f'Distribucion de Bernoulli (θ={theta}, n={n})')      
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
            
    img_str = base64.b64encode(img.getvalue()).decode('ascii')
    
    # Crear datos para descarga
    datos_descarga = "\n".join([f"Experimento {i+1}: {'fracaso' if x == 1 else 'exito'}" for i, x in enumerate(secuencia)])
    
    return render_template('resultado.html', 
                         titulo='Distribucion de Bernoulli',
                         fracaso=fracaso, 
                         exitos=exitos,
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
    plt.title(f'Distribucion Exponencial (λ={lmbda}, n={n})')
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
                         titulo='Distribucion Exponencial',
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

    histograma, secuencia, probabilidades = multinomial.simMultinomial(n=n, rangos=caras, uniforme=uniforme)
    
    # Generar la imagen del histograma
    plt.figure()
    fig, ax = plt.subplots()
    ax.bar(x=range(len(histograma)), height=histograma)
    ax.set_xlabel('Cara del dado')
    ax.set_ylabel('Frecuencia')
    ax.set_xticks(range(len(histograma)))
    ax.set_xticklabels([f' {i+1}' for i in range(len(histograma))])
    plt.title(f'Distribucion Multinomial ({caras} caras, n={n})')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    img_str = base64.b64encode(img.getvalue()).decode('ascii')

    datos_probabilidades = "Probabilidades:\n"
    for i, p in enumerate(probabilidades):
        datos_probabilidades += f"Cara {i+1}: {p:.4f}"
        if i < len(probabilidades) - 1:
            datos_probabilidades += ", "
    

    max_lanzamientos = 10000
    if len(secuencia) > max_lanzamientos:
        secuencia_reducida = secuencia[:max_lanzamientos]
        datos_lanzamientos = "\n".join([f"Lanzamiento {i+1}: Cara {resultado+1}" for i, resultado in enumerate(secuencia_reducida)])
        datos_lanzamientos += f"\n\n... y {len(secuencia) - max_lanzamientos} lanzamientos mas (total: {len(secuencia)})"
    else:
        datos_lanzamientos = "\n".join([f"Lanzamiento {i+1}: Cara {resultado+1}" for i, resultado in enumerate(secuencia)])
    
    datos_descarga = datos_probabilidades + "\n\n" + datos_lanzamientos

    return render_template('resultado.html',
                         titulo='Distribucion Multinomial',
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
    
    # Crear el grafico
    plt.figure()
    fig, ax = plt.subplots()
    ax.hist(histograma, bins=20, edgecolor="black", density=True)
    ax.set_xlabel("Numero de exitos")
    ax.set_ylabel("Frecuencia relativa")
    plt.title(f'Distribucion Binomial (θ={theta}, n={lanzamientos}, rep={repeticiones})')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    img_str = base64.b64encode(img.getvalue()).decode('ascii')

    if len(secuencia) > 10000:
        secuencia_reducida = secuencia[:10000]
        datos_descarga = "\n".join([f"Experimento {i+1}: {exitos} exitos" for i, exitos in enumerate(secuencia_reducida)])
        datos_descarga += f"\n\n... y {len(secuencia) - 10000} experimentos mas (total: {len(secuencia)})"
    else:
        datos_descarga = "\n".join([f"Experimento {i+1}: {exitos} exitos" for i, exitos in enumerate(secuencia)])

    return render_template('resultado.html',
                         titulo='Distribucion Binomial',
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
                         titulo='Distribucion Normal',
                         imagen=img_str,
                         distribucion='normal',
                         miu=miu,
                         sigma=sigma,
                         datos_descarga=datos_descarga,
                         repeticiones=repeticiones,
                         varianza=miu,
                         desviacion=sigma,
                         )

@app.route('/gebbs', methods=['GET', 'POST'])
def gebbs_method():
    return render_template('grafic3d.html',
                         titulo='Metodo de Gibbs',
                         distribucion='gebbs')


@app.route('/normal_2', methods=['GET', 'POST'])
def normal_2():
    return render_template('grafic3d.html',
                         titulo='Normal en 2 variables',
                         distribucion='2normal')



@app.route('/descargar_datos/<distribucion>', methods=['POST'])
def descargar_datos(distribucion):
    temp_filename = None
    try:
        datos = request.form.get('datos', '')
        
        # Si no hay datos, retornar error
        if not datos:
            return "No hay datos para descargar", 400
            
        csv_datos = ""
        filename = f"simulacion_{distribucion}.csv"
        
        if distribucion == 'bernoulli':
            lineas = datos.split('\n')
            csv_datos = "Experimento,Resultado\n"
            for linea in lineas:
                if ': ' in linea:
                    try:
                        partes = linea.split(': ')
                        csv_datos += f"{partes[0].replace('Experimento ', '')},{partes[1]}\n"
                    except IndexError:
                        continue  # Saltar lineas mal formateadas
        
        elif distribucion == 'exponencial':
            lineas = datos.split('\n')
            csv_datos = "Muestra,Valor\n"
            for linea in lineas:
                if ': ' in linea:
                    try:
                        partes = linea.split(': ')
                        csv_datos += f"{partes[0].replace('Muestra ', '')},{partes[1]}\n"
                    except IndexError:
                        continue
        
        elif distribucion == 'multinomial':
            # Hacer el procesamiento mas robusto
            partes = datos.split('\n\n')
            
            # Verificar que tenemos al menos una parte
            if len(partes) == 0:
                return "Formato de datos invalido", 400
                
            csv_datos = ""
            
            # Procesar probabilidades si existen
            if len(partes) > 0 and 'Probabilidades:' in partes[0]:
                prob_lineas = partes[0].split('\n')
                if len(prob_lineas) > 1:  # Si hay mas de una linea (encabezado + datos)
                    csv_datos += "Cara,Probabilidad\n"
                    # Procesar todas las lineas despues del encabezado
                    for linea in prob_lineas[1:]:
                        if linea.strip():  # Si la linea no esta vacia
                            # Dividir por comas para obtener cada par cara-probabilidad
                            elementos = linea.split(', ')
                            for elemento in elementos:
                                if ': ' in elemento:
                                    try:
                                        cara_prob = elemento.split(': ')
                                        cara = cara_prob[0].replace('Cara ', '')
                                        prob = cara_prob[1]
                                        csv_datos += f"{cara},{prob}\n"
                                    except IndexError:
                                        continue
            
            # Procesar lanzamientos si existen
            if len(partes) > 1:
                lanzamientos = partes[1].split('\n')
                csv_datos += "\nLanzamiento,Resultado\n"
                for linea in lanzamientos:
                    if ': ' in linea:
                        try:
                            partes_linea = linea.split(': ')
                            lanzamiento_num = partes_linea[0].replace('Lanzamiento ', '')
                            resultado = partes_linea[1].replace('Cara ', '')
                            csv_datos += f"{lanzamiento_num},{resultado}\n"
                        except IndexError:
                            continue
        
        elif distribucion == 'binomial':
            lineas = datos.split('\n')
            csv_datos = "Experimento,exitos\n"
            for linea in lineas:
                if ': ' in linea:
                    try:
                        partes = linea.split(': ')
                        num_experimento = partes[0].replace('Experimento ', '')
                        num_exitos = partes[1].replace(' exitos', '')
                        csv_datos += f"{num_experimento},{num_exitos}\n"
                    except IndexError:
                        continue
        
        elif distribucion == 'normal':
            lineas = datos.split('\n')
            csv_datos = "Muestra,Valor\n"
            for linea in lineas:
                if ': ' in linea:
                    try:
                        partes = linea.split(': ')
                        csv_datos += f"{partes[0].replace('Muestra ', '')},{partes[1]}\n"
                    except IndexError:
                        continue
        
        else:
            # Para distribuciones no especificadas, usar formato simple
            csv_datos = "Datos\n" + datos.replace('\n', '\n')
        
        # Si no se generaron datos CSV, crear un formato basico
        if not csv_datos.strip():
            csv_datos = "Datos\n" + datos.replace('\n', '\n')
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as tmp_file:
            tmp_file.write(csv_datos)
            temp_filename = tmp_file.name
        
        def cleanup():
            try:
                if temp_filename and os.path.exists(temp_filename):
                    os.unlink(temp_filename)
            except:
                pass
        
        response = send_file(
            temp_filename,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
        
        response.call_on_close(cleanup)
        return response
        
    except Exception as e:
        # Limpieza en caso de error
        if temp_filename and os.path.exists(temp_filename):
            try:
                os.unlink(temp_filename)
            except:
                pass
        return f"Error al generar el archivo: {str(e)}", 500
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)