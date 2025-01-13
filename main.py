""" Programa principal
Ejecuta la Transformada Rápida de Fourier a un audio seleccionado. 
Obtiene el audio, lo grafica en el dominio del tiempo, aplica FFT y grafica el
vector resultante (en el dominio de la frecuencia), luego aplica la FFT Inversa y
grafica el resultante en el dominio del tiempo. 
Finalmente guarda el audio resultante.
Por: Isaí López García
"""

from TransformadaRapidadeFourier import *
from pydub import AudioSegment
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    audio_name = "DreamBig-JeremyKorpas"
    
    # Cargando el audio y convirtiendolo en vector
    audio = AudioSegment.from_file(f"audio/{audio_name}.mp3")
    audio = audio.set_channels(1)
    muestras = np.array(audio.get_array_of_samples())
    sample_rate = audio.frame_rate
    
    # Recortando longitud de muestras a la potencia de 2 mas cercana
    n = potenciade2(len(muestras))
    muestras = muestras[:n]
    
    # Aplicando Fast Fourier Transform
    resultado_FFT = FFT(muestras)
    
    # Obteniendo Frecuencias y Magnitud del resultante
    freq = frecuencias(len(muestras),sample_rate)
    magnitude = np.abs(resultado_FFT)
    
    # Realse de bajos (Solo para mostrar funcionamiento de Inverse FFT)
    #resultado_FFT = realse_bajos(resultado_FFT, freq, 150, 0.6)
        
    # Aplicando Fast Fourier Transform Inversa
    resultado_FFTinversa = inverseFFT(resultado_FFT)
    
    # Se obtiene parte real
    resultado_FFTinversa = np.real(resultado_FFTinversa)
    
    # Muestras resultantes
    vector_resultante = np.int16(resultado_FFTinversa[:len(muestras)] / np.max(np.abs(resultado_FFTinversa)) * 32767)
    
    # Graficar audio: Audio original, FFT result e Inverse FFT result
    fig, axs = plt.subplots(3, 1, figsize=(10, 7))
    
    # Audio original
    axs[0].plot(np.linspace(0, len(muestras) / sample_rate, num=len(muestras)), muestras)
    axs[0].set_title("Audio original (En el dominio del tiempo)")
    axs[0].set_xlabel("Tiempo (s)")
    axs[0].set_ylabel("Amplitud")
    
    # Fast Fourier Transform
    magnitude = np.abs(resultado_FFT)
    axs[1].plot(freq[:len(freq)//2], magnitude[:len(magnitude)//2])
    axs[1].set_title("Fast Fourier Transform (En el dominio de la Frecuencia)")
    axs[1].set_xlabel("Frecuencia (Hz)")
    axs[1].set_ylabel("Magnitud")
        
    # Inverse Fast Fourier Transform
    axs[2].plot(np.linspace(0, len(vector_resultante) / sample_rate, num=len(vector_resultante)), vector_resultante)
    axs[2].set_title("Audio resultante (Inverse Fast Fourier Transform)")
    axs[2].set_xlabel("Tiempo (s)")
    axs[2].set_ylabel("Amplitud")
    
    # Guardar y mostrar gráficas
    plt.tight_layout()
    plt.savefig(f"graficas_{audio_name}.png", dpi=300)
    plt.show()
    
    # Guardar audio
    processed_audio = AudioSegment(
    vector_resultante.tobytes(),
    frame_rate=sample_rate,
    sample_width=2,
    channels=1
    )
    processed_audio.export(f"reconstructed_{audio_name}.mp3", format="mp3")
    
