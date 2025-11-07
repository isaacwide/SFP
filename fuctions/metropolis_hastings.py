import random
import math
import numpy as np
from math import factorial, gamma as gamma_func

# CASO DISCRETO

def metropolis_hastings_discreto(pi, Q, n_iteraciones, x0=None):
    #pi - distribucion estacionaria
    #Q - matriz de transicion
    #x0 - edo. inicial, alearotio si no se especifica
    
    n_estados = len(pi)
    cadena = np.zeros(n_iteraciones, dtype=int)
    # Estado inicial
    if x0 is None:
        cadena[0] = np.random.randint(0, n_estados)
    else:
        cadena[0] = x0
    
    aceptados = 0
    
    for t in range(1, n_iteraciones):
        # Estado actual
        i = cadena[t-1]
        
        # Generar candidato K usando la matriz Q
        k = np.random.choice(n_estados, p=Q[i])
        
        #se implementa la funcion acepracion α = min(1, (π_k × Q_ki) / (π_i × Q_ik))
        if Q[i, k] > 0:
            alpha = min(1, (pi[k] * Q[k, i]) / (pi[i] * Q[i, k]))
        else:
            alpha = 0
        
        #aceptar o rechazar
        u = np.random.uniform(0, 1)
        if u <= alpha:
            cadena[t] = k
            aceptados += 1
        else:
            cadena[t] = i
    
    tasa_aceptacion = aceptados / (n_iteraciones - 1)
    
    return cadena, tasa_aceptacion
    #cadena - estados generados
    #tasa_aceptados - proporcion propuestas aceptadas 


def crear_matriz_propuesta_simetrica(n_estados):
    Q = np.zeros((n_estados, n_estados))
    
    for i in range(n_estados):
        if i == 0:
            Q[i, i] = 0.5
            Q[i, i+1] = 0.5
        elif i == n_estados - 1:
            Q[i, i-1] = 0.5
            Q[i, i] = 0.5
        else:
            Q[i, i-1] = 0.5
            Q[i, i+1] = 0.5
    #print(Q)
    
    return Q #cadena de markov con matriz de transicion


def visualizar_resultados(cadena, pi, burn_in=1000):
    """Función original para visualización - mantener para compatibilidad"""
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Traza de la cadena
    axes[0, 0].plot(cadena, linewidth=0.5)
    axes[0, 0].set_xlabel('Iteración')
    axes[0, 0].set_ylabel('Estado')
    axes[0, 0].set_title('Traza de la Cadena de Markov')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Histograma después del burn-in
    estados_unicos = np.arange(len(pi))
    frecuencias = np.bincount(cadena[burn_in:], minlength=len(pi))
    frecuencias = frecuencias / frecuencias.sum()
    
    x = np.arange(len(pi))
    width = 0.35
    axes[0, 1].bar(x - width/2, frecuencias, width, label='Empírica', alpha=0.7)
    axes[0, 1].bar(x + width/2, pi, width, label='Objetivo', alpha=0.7)
    axes[0, 1].set_xlabel('Estado')
    axes[0, 1].set_ylabel('Probabilidad')
    axes[0, 1].set_title(f'Distribución (después de {burn_in} iteraciones)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Convergencia de la media
    medias_acumuladas = np.cumsum(cadena) / np.arange(1, len(cadena) + 1)
    media_teorica = np.sum(estados_unicos * pi)
    
    axes[1, 0].plot(medias_acumuladas)
    axes[1, 0].axhline(y=media_teorica, color='r', linestyle='--', 
                       label=f'Media teórica = {media_teorica:.3f}')
    axes[1, 0].set_xlabel('Iteración')
    axes[1, 0].set_ylabel('Media acumulada')
    axes[1, 0].set_title('Convergencia de la Media')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    #autocorrelacion
    max_lag = min(100, len(cadena) // 10)
    autocorr = np.correlate(cadena - cadena.mean(), cadena - cadena.mean(), 
                           mode='full')[len(cadena)-1:]
    autocorr = autocorr / autocorr[0]
    
    axes[1, 1].plot(autocorr[:max_lag])
    axes[1, 1].set_xlabel('Lag')
    axes[1, 1].set_ylabel('Autocorrelación')
    axes[1, 1].set_title('Función de Autocorrelación')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


# CASO CONTINUO - Distribuciones hasta Gamma donde Isaac me dijo Bv

def normal_pdf(x, mu, sigma):
    """Función de densidad Normal"""
    return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)


def exponencial_pdf(x, lambda_param):
    """Función de densidad Exponencial"""
    if x < 0:
        return 0
    return lambda_param * math.exp(-lambda_param * x)


def uniforme_pdf(x, a, b):
    """Función de densidad Uniforme"""
    if a <= x <= b:
        return 1 / (b - a)
    return 0


def gamma_pdf(x, alpha, beta):
    """
    Función de densidad Gamma
    f(x) = (beta^alpha / Gamma(alpha)) * x^(alpha-1) * e^(-beta*x)
    """
    if x <= 0:
        return 0
    return (beta ** alpha / gamma_func(alpha)) * (x ** (alpha - 1)) * math.exp(-beta * x)


def mh_continuo(n_samples, initial_value, distribucion, params, proposal_std):
    """
    Metropolis-Hastings para distribuciones continuas
    
    Args:
        n_samples: Número de muestras a generar
        initial_value: Valor inicial de la cadena
        distribucion: Tipo de distribución ('normal', 'exponencial', 'uniforme', 'gamma')
        params: Diccionario con parámetros de la distribución
        proposal_std: Desviación estándar de la distribución de propuesta
    
    Returns:
        samples: Lista de muestras generadas
        acceptance_rate: Tasa de aceptación
    """
    samples = []
    current = initial_value
    accepted = 0
    
    # Seleccionar función de densidad según distribución
    if distribucion == 'normal':
        target_pdf = lambda x: normal_pdf(x, params['mu'], params['sigma'])
    elif distribucion == 'exponencial':
        target_pdf = lambda x: exponencial_pdf(x, params['lambda'])
    elif distribucion == 'uniforme':
        target_pdf = lambda x: uniforme_pdf(x, params['a'], params['b'])
    elif distribucion == 'gamma':
        target_pdf = lambda x: gamma_pdf(x, params['alpha'], params['beta'])
    else:
        raise ValueError(f"Distribución '{distribucion}' no soportada")
    
    for i in range(n_samples):
        # Proponer nuevo valor (distribución normal centrada en el valor actual)
        proposal = random.gauss(current, proposal_std)
        
        # Calcular razón de aceptación
        target_current = target_pdf(current)
        target_proposal = target_pdf(proposal)
        
        # Evitar división por cero
        if target_current > 0:
            acceptance_ratio = min(1, target_proposal / target_current)
        else:
            acceptance_ratio = 1
        
        # Decidir si aceptar la propuesta
        if random.uniform(0, 1) < acceptance_ratio:
            current = proposal
            accepted += 1
        
        samples.append(current)
    
    acceptance_rate = (accepted / n_samples) * 100
    return samples, acceptance_rate


# Funciones auxiliares

def calcular_estadisticas(samples, burn_in=1000):
    """Calcula estadísticas básicas de las muestras"""
    samples_filtradas = samples[burn_in:]
    return {
        'media': np.mean(samples_filtradas),
        'mediana': np.median(samples_filtradas),
        'desviacion': np.std(samples_filtradas),
        'minimo': np.min(samples_filtradas),
        'maximo': np.max(samples_filtradas)
    }


def calcular_autocorrelacion(samples, max_lag=100):
    """Calcula la función de autocorrelación"""
    samples_array = np.array(samples)
    autocorr = np.correlate(
        samples_array - samples_array.mean(), 
        samples_array - samples_array.mean(), 
        mode='full'
    )[len(samples_array)-1:]
    autocorr = autocorr / autocorr[0]
    return autocorr[:min(max_lag, len(autocorr))]