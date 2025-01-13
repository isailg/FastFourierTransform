# Transformada Rápida de Fourier
### Isaí López García  
---

## Descripción

Este repositorio contiene el código de la Transformada Rápida de Fourier propuesto por Cooley-Tukkeys(1965) implementado a procesamiento de audio.

### Contenido del Repositorio

1. El código con los algoritmos se encuentran en el archivo **TransformadaRapidadeFourier.py**, el cual contiene una función llamada `FFT` y otra llamado `InverseFFT` con los que se aplica la Transformada Rápida y la Inversa a un audio en el archivo **main.py**.

2. Una carpeta llamada **/audio** con 3 canciones de Youtube Studio, las cuales se procesaron con estos algoritmos.

3. Los audios resultantes estan en la carpeta raíz del repositorio con el prefijo "reconstructed_", también están las imágenes que muestran la **gráfica del audio original** (En el dominio del tiempo), **la resultante de la Transformada Rápida** (En el dominio de la frecuencia) y **la resultante de la Transformada Inversa** (En el dominio del tiempo). **Por audio transformado hay una imagen que contiene sus 3 gráficas.** 
