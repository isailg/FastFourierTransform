""" Programa principal
Ejecuta la Transformada Rápida de Fourier a un audio seleccionado. 
Obtiene el audio, lo grafica en el dominio del tiempo, aplica FFT y grafica el
vector resultante (en el dominio de la frecuencia), después aplica un filtro de pasabajas, 
recosntruye el audio aplicando la FFT Inversa y grafica el resultante en el dominio del tiempo. 
Finalmente guarda el audio resultante.
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
    """
    # Cargando el audio y convirtiendolo en vector
    audio = AudioSegment.from_file(f"audio/{audio_name}.mp3")
    audio = audio.set_channels(1)
    muestras = np.array(audio.get_array_of_samples())
    sample_rate = audio.frame_rate
    """
    
    # Recortando longitud de muestras a la potencia de 2 mas cercana
    n = potenciade2(len(muestras))
    muestras = muestras[:n]
    """
    # Parámetros de procesamiento
    CHUNK_SIZE = 512#1024  # Tamaño del fragmento a procesar
    total_chunks = len(muestras) // CHUNK_SIZE
    
    # Inicializar PyAudio para reproducción
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1,
                    rate=sample_rate,
                    output=True)
    
    # Configurar matplotlib para gráficas interactivas
    plt.ion()
    fig, axs = plt.subplots(3, 1, figsize=(10, 7))
    time_axis = np.linspace(0, CHUNK_SIZE / sample_rate, CHUNK_SIZE)
    freq_axis = frecuencias(CHUNK_SIZE, sample_rate)
    
    # Inicializar gráficos
    line_time, = axs[0].plot(time_axis, np.zeros(CHUNK_SIZE))
    axs[0].set_title("Audio original (Dominio del tiempo)")
    axs[0].set_xlabel("Tiempo (s)")
    axs[0].set_ylabel("Amplitud")
    
    line_freq, = axs[1].plot(freq_axis[:CHUNK_SIZE // 2], np.zeros(CHUNK_SIZE // 2))
    axs[1].set_title("FFT (Dominio de la frecuencia)")
    axs[1].set_xlabel("Frecuencia (Hz)")
    axs[1].set_ylabel("Magnitud")
    
    line_time_proc, = axs[2].plot(time_axis, np.zeros(CHUNK_SIZE))
    axs[2].set_title("Audio procesado (Dominio del tiempo)")
    axs[2].set_xlabel("Tiempo (s)")
    axs[2].set_ylabel("Amplitud")
    
    #plt.tight_layout()
    
    fragmentos_procesados = []
    
    # Procesar y reproducir en bloques
    for i in range(total_chunks):
        start = i * CHUNK_SIZE
        end = start + CHUNK_SIZE
        chunk = muestras[start:end]

        # FFT
        resultado_FFT = FFT(chunk)
        magnitude = np.abs(resultado_FFT)
        
        # Frecuencias positivas
        freq_axis = frecuencias(CHUNK_SIZE, sample_rate)
        positive_freq_indices = freq_axis >= 0
        freq_axis = freq_axis[positive_freq_indices]
        magnitude = magnitude[positive_freq_indices]
    
        # Filtro pasa bajas
        resultado_FFT = filtro_pasabajas(resultado_FFT, freq_axis, 200, 0.1)

        # FFT inversa
        resultado_FFTinversa = inverseFFT(resultado_FFT)
        resultado_FFTinversa = np.real(resultado_FFTinversa)
        chunk_procesado = np.int16(resultado_FFTinversa / np.max(np.abs(resultado_FFTinversa)) * 32767)

        # Reproducir fragmento procesado
        stream.write(chunk_procesado.tobytes())
        
        fragmentos_procesados.append(chunk_procesado)

        # Actualizar gráficas
        line_time.set_ydata(chunk)
        line_freq.set_ydata(magnitude)
        line_time_proc.set_ydata(chunk_procesado)
        plt.pause(0.01)  # Pausa para actualizar las gráficas
    
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
    
    print("Procesamiento en tiempo real completado.")
    plt.tight_layout()
    plt.savefig("graficas_procesamiento.png", dpi=300)
    plt.show()
    """
    # Aplicando Fast Fourier Transform
    resultado_FFT = FFT(muestras)
    
    # Obteniendo Frecuencias y Magnitud del resultante
    freq = frecuencias(len(muestras),sample_rate)
    magnitude = np.abs(resultado_FFT)
    
    # Filtro de pasabajas
    resultado_FFT = filtro_pasabajas(resultado_FFT, freq, 200, 0)
        
    # Aplicando Fast Fourier Transform Inversa
    resultado_FFTinversa = inverseFFT(resultado_FFT)
    
    # Se obtiene parte real
    resultado_FFTinversa = np.real(resultado_FFTinversa)
    
    # Muestras resultantes
    vector_resultante = np.int16(resultado_FFTinversa[:len(muestras)] / np.max(np.abs(resultado_FFTinversa)) * 32767)
    
    output = f"Reconstructed_{audio_name}.wav"
    sf.write(output, vector_resultante, sample_rate)
        
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
    """
    # Guardar audio
    processed_audio = AudioSegment(
    vector_resultante.tobytes(),
    frame_rate=sample_rate,
    sample_width=2,
    channels=1
    )
    processed_audio.export(f"reconstructed_{audio_name}.mp3", format="mp3")
    """
