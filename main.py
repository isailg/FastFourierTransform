""" Programa principal
Ejecuta la Transformada Rápida de Fourier a un audio seleccionado. 
Obtiene el audio, lo grafica en el dominio del tiempo, aplica FFT y grafica el
vector resultante (en el dominio de la frecuencia), después aplica un filtro de
 pasabajas, recosntruye el audio aplicando la FFT Inversa y grafica el resultante 
 en el dominio del tiempo. También reproduce el audio resultante en tiempo real.
 Finalmente guarda el audio resultante y exporta las gráficas.
Por: Isaí López García
"""

from TransformadaRapidadeFourier import *
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import pyaudio
import wave
import os



if __name__ == "__main__":
    
    audio_name = "DreamBig-JeremyKorpas"
    mp3_path = f"audio/{audio_name}.mp3"
    wav_path = f"{audio_name}.wav"
    
    # Convertir MP3 a WAV
    convertir_mp3_a_wav(mp3_path, wav_path)
    
    # Leer el archivo WAV con wave
    with wave.open(wav_path, "rb") as wf:
        sample_rate = wf.getframerate()
        n_frames = wf.getnframes()
        n_channels = wf.getnchannels()
        audio_data = wf.readframes(n_frames)
        muestras = np.frombuffer(audio_data, dtype=np.int16)
    
    # Recortando longitud de muestras a la potencia de 2 mas cercana
    n = potenciade2(len(muestras))
    muestras = muestras[:n]
    
    # Parámetros de procesamiento
    submuestra_size = 512 #1024
    n_submuestras = len(muestras) // submuestra_size
    
    # Inicializar PyAudio para reproducción
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1,
                    rate=sample_rate,
                    output=True)
    
    # Configurar matplotlib para gráficas interactivas
    plt.ion()
    fig, axs = plt.subplots(3, 1, figsize=(10, 7))
    time_axis = np.linspace(0, submuestra_size / sample_rate, submuestra_size)
    freq_axis = frecuencias(submuestra_size, sample_rate)
    
    # Inicializar gráficos
    line_time, = axs[0].plot(time_axis, np.zeros(submuestra_size))
    axs[0].set_title("Audio original (Dominio del tiempo)")
    axs[0].set_xlabel("Tiempo (s)")
    axs[0].set_ylabel("Amplitud")
    
    line_freq, = axs[1].plot(freq_axis[:submuestra_size // 2], np.zeros(submuestra_size // 2))
    axs[1].set_title("FFT (Dominio de la frecuencia)")
    axs[1].set_xlabel("Frecuencia (Hz)")
    axs[1].set_ylabel("Magnitud")
    
    line_time_proc, = axs[2].plot(time_axis, np.zeros(submuestra_size))
    axs[2].set_title("Audio procesado (Dominio del tiempo)")
    axs[2].set_xlabel("Tiempo (s)")
    axs[2].set_ylabel("Amplitud")
    
    
    fragmentos_procesados = []
    
    # Procesar y reproducir en bloques de submuestras
    for i in range(n_submuestras):
        start = i * submuestra_size
        end = start + submuestra_size
        submuestra = muestras[start:end]

        # FFT
        resultado_FFT = FFT(submuestra)
        magnitude = np.abs(resultado_FFT)
        
        # Frecuencias
        freq_axis = frecuencias(submuestra_size, sample_rate)
        positive_freq_indices = freq_axis >= 0
        freq_axis = freq_axis[positive_freq_indices]
        magnitude = magnitude[positive_freq_indices]
    
        # Filtro pasa bajas
        resultado_FFT = filtro_pasabajas(resultado_FFT, freq_axis, 150, 0)

        # FFT inversa
        resultado_FFTinversa = inverseFFT(resultado_FFT)
        resultado_FFTinversa = np.real(resultado_FFTinversa)
        submuestra_procesado = np.int16(resultado_FFTinversa / np.max(np.abs(resultado_FFTinversa)) * 32767)

        # Reproducir fragmento filtrado
        stream.write(submuestra_procesado.tobytes())
        fragmentos_procesados.append(submuestra_procesado)

        # Actualizar gráficas
        line_time.set_ydata(submuestra)
        line_freq.set_ydata(magnitude)
        line_time_proc.set_ydata(submuestra_procesado)
        plt.pause(0.01)  # Pausa para actualizar las gráficas
    
    # Agregarlo al vector final resultante
    audio_procesado = np.concatenate(fragmentos_procesados)
    
    with wave.open("audio_procesado.wav", "w") as archivo_wav:
        archivo_wav.setnchannels(1)  # Canal mono
        archivo_wav.setsampwidth(2)  # Tamaño de muestra en bytes (16 bits = 2 bytes)
        archivo_wav.setframerate(sample_rate)  # Tasa de muestreo
        archivo_wav.writeframes(audio_procesado.tobytes())
    
    # Cerrar el flujo de audio
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    plt.tight_layout()
    plt.savefig("graficas_{audio_name}.png", dpi=300)
    plt.show()
    
