import wfdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kurtosis

# --- Configuración ---
record_name = '01'
ruta_archivos = '.'

# --- Leer señal ---
record = wfdb.rdrecord(f"{ruta_archivos}/{record_name}")
signal = record.p_signal[:, 0]  # Canal 1
fs = record.fs

# --- Extraer primeros 5 segundos ---
muestras_5s = int(fs * 5)
segmento = signal[:muestras_5s]
tiempo = np.arange(len(segmento)) / fs

# ================================
#   CÁLCULOS MANUALES
# ================================
N = len(segmento)

media_manual = sum(segmento) / N
desviacion_std_manual = (sum((x - media_manual) ** 2 for x in segmento) / (N - 1)) ** 0.5
coef_variacion_manual = desviacion_std_manual / media_manual if media_manual != 0 else np.nan
m4 = sum((x - media_manual) ** 4 for x in segmento) / N
curtosis_manual = m4 / (desviacion_std_manual ** 4)
hist_manual, bins_manual = np.histogram(segmento, bins=20, density=True)

# ================================
#   CÁLCULOS CON FUNCIONES
# ================================
media_func = np.mean(segmento)
desviacion_std_func = np.std(segmento, ddof=0)  # Poblacional
coef_variacion_func = desviacion_std_func / media_func if media_func != 0 else np.nan
curtosis_func = kurtosis(segmento, fisher=False)
hist_func, bins_func = np.histogram(segmento, bins=20, density=True)

# ================================
#   MOSTRAR RESULTADOS
# ================================
print("=== Cálculo Manual (5s) ===")
print(f"Media: {media_manual:.6f}")
print(f"Desviación estándar: {desviacion_std_manual:.6f}")
print(f"Coeficiente de variación: {coef_variacion_manual:.6f}")
print(f"Curtosis: {curtosis_manual:.6f}")

print("\n=== Cálculo con funciones predefinidas (5s) ===")
print(f"Media: {media_func:.6f}")
print(f"Desviación estándar: {desviacion_std_func:.6f}")
print(f"Coeficiente de variación: {coef_variacion_func:.6f}")
print(f"Curtosis: {curtosis_func:.6f}")

# ================================
#   GRAFICAR
# ================================

# 1️⃣ Señal
plt.figure(figsize=(10, 4))
plt.plot(tiempo, segmento, label='Señal ECG (5s)', color='black')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (mV)')
plt.title('ECG - Primeros 5 segundos')
plt.grid(True)
plt.legend()

# 2️⃣ Histograma manual
plt.figure(figsize=(6, 4))
plt.bar(
    (bins_manual[:-1] + bins_manual[1:]) / 2,
    hist_manual,
    width=(bins_manual[1] - bins_manual[0]),
    alpha=0.7,
    color='g',
    edgecolor='black'
)
plt.xlabel('Amplitud (mV)')
plt.ylabel('Densidad')
plt.title('Histograma (Manual)')
plt.grid(True)

# 3️⃣ Histograma con funciones
plt.figure(figsize=(6, 4))
plt.bar(
    (bins_func[:-1] + bins_func[1:]) / 2,
    hist_func,
    width=(bins_func[1] - bins_func[0]),
    alpha=0.7,
    color='r',
    edgecolor='black'
)
plt.xlabel('Amplitud (mV)')
plt.ylabel('Densidad')
plt.title('Histograma (Funciones predefinidas)')
plt.grid(True)

# Mostrar todas las ventanas
plt.show()











