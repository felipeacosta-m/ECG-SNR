import numpy as np
import matplotlib.pyplot as plt
from scipy.signal.windows import gaussian

# ================================
#   PARTE B: Generar señal ECG
# ================================

# Parámetros de la señal
frecuencia_muestreo = 360  # Hz
duracion_segundos = 5  # segundos
numero_muestras = frecuencia_muestreo * duracion_segundos
tiempo = np.arange(numero_muestras) / frecuencia_muestreo

# 1️⃣ Interferencia de baja frecuencia (línea base)
interferencia_baja_frecuencia = 0.05 * np.sin(2 * np.pi * 0.5 * tiempo)

# 2️⃣ Generar plantilla de QRS
frecuencia_cardiaca = 72  # latidos por minuto
intervalo_rr = int(frecuencia_muestreo * (60 / frecuencia_cardiaca))
qrs_sigma = 0.03 * frecuencia_muestreo
qrs_longitud = int(qrs_sigma * 8)
plantilla_qrs = gaussian(qrs_longitud, std=qrs_sigma)
plantilla_qrs /= np.max(plantilla_qrs)

# 3️⃣ Construir señal ECG
ecg = np.zeros(numero_muestras)
for inicio in range(0, numero_muestras, intervalo_rr):
    fin = inicio + qrs_longitud
    if fin <= numero_muestras:
        ecg[inicio:fin] += plantilla_qrs

# 4️⃣ Añadir ondas P y T
for inicio in range(0, numero_muestras, intervalo_rr):
    indice_p = inicio - int(0.16 * frecuencia_muestreo)
    indice_t = inicio + int(0.24 * frecuencia_muestreo)
    if 0 <= indice_p < numero_muestras - int(0.05 * frecuencia_muestreo):
        ecg[indice_p:indice_p + int(0.05 * frecuencia_muestreo)] += 0.2 * np.hanning(int(0.05 * frecuencia_muestreo))
    if 0 <= indice_t < numero_muestras - int(0.1 * frecuencia_muestreo):
        ecg[indice_t:indice_t + int(0.1 * frecuencia_muestreo)] += 0.3 * np.hanning(int(0.1 * frecuencia_muestreo))

# 5️⃣ Añadir interferencia aleatoria (simula variaciones aleatorias)
interferencia_aleatoria = 0.02 * np.random.randn(numero_muestras)
ecg += interferencia_baja_frecuencia + interferencia_aleatoria

# ================================
#   Cálculos manuales
# ================================
N = len(ecg)

media_manual = sum(ecg) / N
desviacion_estandar_manual = (sum((x - media_manual) ** 2 for x in ecg) / (N - 1)) ** 0.5
coef_variacion_manual = desviacion_estandar_manual / media_manual if media_manual != 0 else np.nan
m4 = sum((x - media_manual) ** 4 for x in ecg) / N
curtosis_manual = m4 / (desviacion_estandar_manual ** 4)

# Histograma manual
numero_bins = 20
valor_min = min(ecg)
valor_max = max(ecg)
ancho_bin = (valor_max - valor_min) / numero_bins
bins_manual = [valor_min + i * ancho_bin for i in range(numero_bins + 1)]
hist_manual = [0] * numero_bins
for valor in ecg:
    indice = int((valor - valor_min) / ancho_bin)
    if indice == numero_bins:  # Caso borde
        indice -= 1
    hist_manual[indice] += 1

# Convertir a densidad
hist_manual = [h / (N * ancho_bin) for h in hist_manual]
centros_manual = [(bins_manual[i] + bins_manual[i+1]) / 2 for i in range(numero_bins)]

# ================================
#   Mostrar resultados
# ================================
print("=== Señal Sintética (Cálculos Manuales) ===")
print(f"Media: {media_manual:.6f}")
print(f"Desviación estándar: {desviacion_estandar_manual:.6f}")
print(f"Coeficiente de variación: {coef_variacion_manual:.6f}")
print(f"Curtosis: {curtosis_manual:.6f}")

# ================================
#   Graficar resultados
# ================================
# Señal ECG
plt.figure(figsize=(10, 4))
plt.plot(tiempo, ecg, color='blue', label='ECG sintético (5s)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (mV)')
plt.title('ECG Sintético - Primeros 5 segundos')
plt.grid(True)
plt.legend()

# Histograma manual
plt.figure(figsize=(6, 4))
plt.bar(
    centros_manual,
    hist_manual,
    width=ancho_bin,
    alpha=0.7,
    color='g',
    edgecolor='black'
)
plt.xlabel('Amplitud (mV)')
plt.ylabel('Densidad')
plt.title('Histograma (Manual) - ECG sintético')
plt.grid(True)

plt.show()

# ================================
#   Guardar señal como TXT
# ================================
np.savetxt('ecg_sintetico.txt', ecg)
print("Archivo 'ecg_sintetico.txt' generado.")
