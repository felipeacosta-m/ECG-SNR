import numpy as np
import matplotlib.pyplot as plt
from scipy.signal.windows import gaussian

# ======================================
#   PARTE B: Generar señal ECG sintética
# ======================================

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
ecg_original = ecg + interferencia_baja_frecuencia + interferencia_aleatoria

# ======================================
#   Función para calcular SNR
# ======================================
def calcular_snr(senal, senal_con_ruido):
    potencia_senal = np.mean(senal**2)
    potencia_ruido = np.mean((senal_con_ruido - senal)**2)
    return 10 * np.log10(potencia_senal / potencia_ruido)

# ======================================
#   a) Ruido Gaussiano
# ======================================
ruido_gaussiano = 0.05 * np.random.randn(numero_muestras)
ecg_gaussiano = ecg_original + ruido_gaussiano
snr_gauss = calcular_snr(ecg_original, ecg_gaussiano)

# ======================================
#   b) Ruido Impulsivo
# ======================================
ecg_impulsivo = ecg_original.copy()
num_impulsos = int(0.01 * numero_muestras)  # 1% de puntos
posiciones = np.random.randint(0, numero_muestras, num_impulsos)
ecg_impulsivo[posiciones] += np.random.choice([-1, 1], num_impulsos) * 1.5
snr_impulsivo = calcular_snr(ecg_original, ecg_impulsivo)

# ======================================
#   c) Ruido tipo artefacto
#       (simula movimiento muscular o eléctrico periódico)
# ======================================
ruido_artefacto = 0.1 * np.sin(2 * np.pi * 50 * tiempo)  # 50 Hz
ecg_artefacto = ecg_original + ruido_artefacto
snr_artefacto = calcular_snr(ecg_original, ecg_artefacto)

# ======================================
#   Mostrar resultados SNR
# ======================================
print("=== Relación Señal/Ruido (SNR) ===")
print(f"SNR con ruido gaussiano: {snr_gauss:.2f} dB")
print(f"SNR con ruido impulsivo: {snr_impulsivo:.2f} dB")
print(f"SNR con ruido tipo artefacto: {snr_artefacto:.2f} dB")

# ======================================
#   Graficar señales
# ======================================
plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
plt.plot(tiempo, ecg_original, label="ECG Original")
plt.title("ECG Original")
plt.grid(True)

plt.subplot(4, 1, 2)
plt.plot(tiempo, ecg_gaussiano, label="ECG + Ruido Gaussiano", color='orange')
plt.title(f"ECG con Ruido Gaussiano (SNR = {snr_gauss:.2f} dB)")
plt.grid(True)

plt.subplot(4, 1, 3)
plt.plot(tiempo, ecg_impulsivo, label="ECG + Ruido Impulsivo", color='red')
plt.title(f"ECG con Ruido Impulsivo (SNR = {snr_impulsivo:.2f} dB)")
plt.grid(True)

plt.subplot(4, 1, 4)
plt.plot(tiempo, ecg_artefacto, label="ECG + Ruido Artefacto", color='green')
plt.title(f"ECG con Ruido Artefacto (SNR = {snr_artefacto:.2f} dB)")
plt.grid(True)

plt.tight_layout()
plt.show()
