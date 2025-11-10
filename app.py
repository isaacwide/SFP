from flask import Flask, render_template, request, send_file
from io import BytesIO, StringIO
from flask_cors import CORS
import os   
import tempfile
import base64
import random
import math
import numpy as np
from math import factorial
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fuctions import bernuli, exponencial, multinomial, norm, simulacion_binomial, metropolis_hastings

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 
CORS(app)

app.config['secret_key']='9f3a8b7c2d1e4f5a6b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bernoulli', methods=['GET', 'POST'])
def bernoulli():
    theta = 0.5
    n = 10000
    
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
            
    # Crear datos para descarga        
    img_str = base64.b64encode(img.getvalue()).decode('ascii')
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
    lmbda = 0.5
    n = 100
    
    if request.method == 'POST':
        lmbda = float(request.form.get('lambda', 0.5))
        n = int(request.form.get('n', 100))
    
    valores = exponencial.simExponencial(lmbda=lmbda, n=n)

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
                         desviacion=sigma)

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

@app.route('/metropolis_hastings')
def metropolis_hastings_menu():
    return render_template('metropolis_hastings.html')

@app.route('/metropolis_hastings/continuo', methods=['GET', 'POST'])
def mh_continuo():
    # Valores por defecto
    n_samples = 1000
    initial_value = 0
    distribucion = 'normal'
    proposal_std = 1
    
    # Parámetros específicos por distribución
    params = {
        'normal': {'mu': 0, 'sigma': 1},
        'exponencial': {'lambda': 1},
        'uniforme': {'a': 0, 'b': 1},
        'gamma': {'alpha': 2, 'beta': 1},
        "SumaNormal":{'mu1':-2,'sigma1':1,'mu2':2,'sigma2':1,'peso':0.5}
    }
    
    if request.method == 'POST':
        n_samples = int(request.form.get('n_samples' or 1000))
        initial_value = float(request.form.get('initial_value'or 0))
        distribucion = request.form.get('distribucion', 'normal')
        proposal_std = float(request.form.get('proposal_std'or 1))
        
        # Obtener parámetros según distribución
        if distribucion == 'normal':
            params['normal']['mu'] = float(request.form.get('mu'or 0))
            params['normal']['sigma'] = float(request.form.get('sigma'or 1))
            dist_params = params['normal']
        elif distribucion == 'exponencial':
            params['exponencial']['lambda'] = float(request.form.get('lambda'or 1))
            dist_params = params['exponencial']
        elif distribucion == 'uniforme':
            params['uniforme']['a'] = float(request.form.get('a'or 0))
            params['uniforme']['b'] = float(request.form.get('b'or 1))
            dist_params = params['uniforme']
        elif distribucion == 'gamma':
            params['gamma']['alpha'] = float(request.form.get('alpha'or 2))
            params['gamma']['beta'] = float(request.form.get('beta'or 1))
            dist_params = params['gamma']
        elif distribucion == 'SumaNormal':
            
            params['SumaNormal']['mu1'] = float(request.form.get('mu1' or -2))
            params['SumaNormal']['sigma1'] = float(request.form.get('sigma1' or 1))
            params['SumaNormal']['mu2'] = float(request.form.get('mu2' or 2))
            params['SumaNormal']['sigma2']= float(request.form.get('sigma2' or 1))
            params['SumaNormal']['peso'] = float(request.form.get('peso' or 0.5))
            dist_params = params['SumaNormal']
            

            # Generar muestras
        
        samples, acceptance_rate = metropolis_hastings.mh_continuo(
            n_samples, initial_value, distribucion, dist_params, proposal_std
        )
        # Calcular estadísticas
        stats = metropolis_hastings.calcular_estadisticas(samples, burn_in=min(1000, n_samples//10))
        
        # Crear gráfico
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Histograma
        axes[0, 0].hist(samples, bins=50, edgecolor='black', density=True, alpha=0.7)
        axes[0, 0].set_xlabel('Valores')
        axes[0, 0].set_ylabel('Densidad')
        axes[0, 0].set_title(f'Distribución de muestras - {distribucion.capitalize()}')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Traza de la cadena
        axes[0, 1].plot(samples[:min(1000, len(samples))], linewidth=0.8)
        axes[0, 1].set_xlabel('Iteración')
        axes[0, 1].set_ylabel('Valor')
        axes[0, 1].set_title(f'Traza de la cadena (primeras {min(1000, len(samples))} iteraciones)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Convergencia de la media
        medias_acumuladas = np.cumsum(samples) / np.arange(1, len(samples) + 1)
        axes[1, 0].plot(medias_acumuladas)
        axes[1, 0].axhline(y=stats['media'], color='r', linestyle='--', 
                          label=f'Media final = {stats["media"]:.3f}')
        axes[1, 0].set_xlabel('Iteración')
        axes[1, 0].set_ylabel('Media acumulada')
        axes[1, 0].set_title('Convergencia de la Media')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Autocorrelación
        autocorr = metropolis_hastings.calcular_autocorrelacion(samples, max_lag=min(100, len(samples)//10))
        axes[1, 1].plot(autocorr)
        axes[1, 1].set_xlabel('Lag')
        axes[1, 1].set_ylabel('Autocorrelación')
        axes[1, 1].set_title('Función de Autocorrelación')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        img = BytesIO()
        plt.savefig(img, format='png', dpi=100)
        img.seek(0)
        plt.close()
        
        img_str = base64.b64encode(img.getvalue()).decode('ascii')
        
        # Datos para descarga
        datos_descarga = f"Estadísticas:\nMedia: {stats['media']:.6f}\nMediana: {stats['mediana']:.6f}\nDesviación: {stats['desviacion']:.6f}\n\nMuestras:\n"
        datos_descarga += "\n".join([f"Muestra {i+1}: {x:.6f}" for i, x in enumerate(samples)])
        
        return render_template('mh_continuo.html',
                             imagen=img_str,
                             acceptance_rate=acceptance_rate,
                             n_samples=n_samples,
                             initial_value=initial_value,
                             distribucion=distribucion,
                             params=dist_params,
                             proposal_std=proposal_std,
                             stats=stats,
                             datos_descarga=datos_descarga)
    
    return render_template('mh_continuo.html',
                         distribucion='normal',
                         params=params['normal'])

@app.route('/metropolis_hastings/discreto', methods=['GET', 'POST'])
def mh_discreto():
    n_iteraciones = 10000
    n_estados = 10
    x0 = None
    tipo_distribucion = 'poisson'
    
    if request.method == 'POST':
        n_iteraciones = int(request.form.get('n_iteraciones', 10000))
        n_estados = int(request.form.get('n_estados', 10))
        x0_input = request.form.get('x0', '')
        x0 = int(x0_input) if x0_input else None
        tipo_distribucion = request.form.get('tipo_distribucion', 'poisson')
        
        if tipo_distribucion == 'poisson':
            lambda_param = float(request.form.get('lambda_poisson', 3))
            estados = np.arange(0, n_estados)
            pi = np.exp(-lambda_param) * (lambda_param ** estados) / np.array([factorial(k) for k in estados])
            pi = pi / pi.sum()
            param_info = f"λ={lambda_param}"
        elif tipo_distribucion == 'uniforme':
            pi = np.ones(n_estados) / n_estados
            param_info = "Uniforme"
        elif tipo_distribucion == 'geometrica':
            p = float(request.form.get('p_geometrica', 0.3))
            estados = np.arange(0, n_estados)
            pi = p * ((1-p) ** estados)
            pi = pi / pi.sum()
            param_info = f"p={p}"
        else:
            pi = np.ones(n_estados) / n_estados
            param_info = "Uniforme"
        
         # Crear matriz de propuesta
        Q = metropolis_hastings.crear_matriz_propuesta_simetrica(n_estados)

         # Ejecutar Metropolis-Hastings
        cadena, tasa_aceptacion = metropolis_hastings.metropolis_hastings_discreto(pi, Q, n_iteraciones, x0)
        
        # Usar la función de visualización original
        burn_in = 1000
        fig = metropolis_hastings.visualizar_resultados(cadena, pi, burn_in)
        
         # Guardar imagen
        img = BytesIO()
        plt.savefig(img, format='png', dpi=100)
        img.seek(0)
        plt.close()
        
        img_str = base64.b64encode(img.getvalue()).decode('ascii')
        
        # Calcular distribución empírica
        frecuencias = np.bincount(cadena[burn_in:], minlength=n_estados)
        dist_empirica = frecuencias / frecuencias.sum()
        
        # Datos para descarga
        datos_probs = f"Distribución: {tipo_distribucion.capitalize()} ({param_info})\n"
        datos_probs += f"Número de iteraciones: {n_iteraciones}\n"
        datos_probs += f"Tasa de aceptación: {tasa_aceptacion:.3f}\n\n"
        datos_probs += "Comparación de distribuciones (después del burn-in):\n"
        datos_probs += "Estado | Objetivo | Empírica | Diferencia\n"
        datos_probs += "-" * 50 + "\n"
        for i in range(n_estados):
            diff = abs(pi[i] - dist_empirica[i])
            datos_probs += f"  {i:2d}   |  {pi[i]:.4f}  |  {dist_empirica[i]:.4f}  |  {diff:.4f}\n"
        
        mse = np.mean((pi - dist_empirica)**2)
        datos_probs += f"\nError cuadrático medio: {mse:.6f}\n"
        
        datos_samples = f"\n\nMuestras (primeras 10000):\n"
        datos_samples += "\n".join([f"Muestra {i+1}: Estado {s}" for i, s in enumerate(cadena[:10000])])
        datos_descarga = datos_probs + datos_samples
        
        return render_template('mh_discreto.html',
                             imagen=img_str,
                             acceptance_rate=tasa_aceptacion * 100,
                             n_iteraciones=n_iteraciones,
                             n_estados=n_estados,
                             x0=x0 if x0 is not None else 'Aleatorio',
                             tipo_distribucion=tipo_distribucion,
                             datos_descarga=datos_descarga)
    
    return render_template('mh_discreto.html')

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
                        continue
        
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
                if len(prob_lineas) > 1:
                    csv_datos += "Cara,Probabilidad\n"
                    # Procesar todas las lineas despues del encabezado
                    for linea in prob_lineas[1:]:
                        if linea.strip():# Si la linea no esta vacia
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
                    
        elif distribucion == 'mh_continuo':
            lineas = datos.split('\n')
            csv_datos = ""
            
            # Buscar estadísticas
            for i, linea in enumerate(lineas):
                if linea.startswith('Estadísticas:'):
                    csv_datos += "Estadística,Valor\n"
                    for j in range(i+1, min(i+5, len(lineas))):
                        if ': ' in lineas[j]:
                            partes = lineas[j].split(': ')
                            csv_datos += f"{partes[0]},{partes[1]}\n"
                    csv_datos += "\nMuestra,Valor\n"
                    break
            
            # Procesar muestras
            for linea in lineas:
                if linea.startswith('Muestra '):
                    try:
                        partes = linea.split(': ')
                        num = partes[0].replace('Muestra ', '')
                        valor = partes[1]
                        csv_datos += f"{num},{valor}\n"
                    except IndexError:
                        continue

        elif distribucion == 'mh_discreto':
            csv_datos = datos.replace('  ', ',').replace(' | ', ',')
        
        else:
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