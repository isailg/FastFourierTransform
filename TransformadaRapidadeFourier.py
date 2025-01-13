import numpy as np

def FFT(x):
    """
    Transformada Rápida de Fourier, Cooley-Tukkeys (1965) 
    
        Entrada: Numpy array de longitud potencia de 2
    
        Salida: Numpy array de frecuencias
    """
    N = len(x)
    
    if N == 1:
        return x
    else:
        X_even = FFT(x[::2])
        X_odd = FFT(x[1::2])
        factor = np.exp(-2j*np.pi*np.arange(N)/ N)
        
        X = np.concatenate(\
            [X_even+factor[:int(N/2)]*X_odd,
             X_even+factor[int(N/2):]*X_odd])
        return X


def inverseFFT(X):
    """
    Transformada Rápida de Fourier Inversa, Cooley-Tukkeys (1965) 
    
        Entrada: Numpy array obtenido de FFT
    
        Salida: Numpy array en dominio del tiempo 
    """
    N = len(X)
    if N <= 1:
        return X
    else:
        even = inverseFFT(X[::2])
        odd = inverseFFT(X[1::2])
        T = [np.exp(2j * np.pi * k / N) * odd[k] for k in range(N // 2)]
        result = [(even[k] + T[k]) for k in range(N // 2)] + \
                 [(even[k] - T[k]) for k in range(N // 2)]
    return [x / N for x in result]


def potenciade2(n):
    """ Encuentra el piso de la potencia de 2 más cercana a n"""
    return 2 ** int(np.floor(np.log2(n)))

def realse_bajos(fft_result, frecuencias, frecuencia_de_corte = 200, amp=1):
    """ Función para realsar los graves de una canción """
    for i in range(len(fft_result)):
        if np.abs(frecuencias[i]) < frecuencia_de_corte:
            fft_result[i] = fft_result[i]*amp
    return fft_result
    
def frecuencias(N, sample_rate):
    """ Calcula las frecuencias del array """
    k = np.arange(N)
    freqs = np.where(k < N // 2, k, k - N) * sample_rate / N
    return freqs
