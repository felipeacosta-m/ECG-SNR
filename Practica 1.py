import wfdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

# === Función corregida para calcular el SNR ===
def calcular_snr(señal_original, señal_contaminada):
    potencia_señal_con_ruido = np.mean(señal_contaminada ** 2)
    ruido = señal_contaminada - señal_original
    potencia_ruido = np.mean(ruido ** 2)

    if potencia_ruido == 0:
        return np.inf  # Evitar división por cero
    
    snr = 10 * np.log10(potencia_señal_con_ruido / potencia_ruido)  # Nueva ecuación
    return snr

# Nombre base del archivo 
archivo = "session1_participant1_gesture10_trial3"

# Leer los datos y la cabecera
registro = wfdb.rdrecord(archivo)
datos = registro.p_signal  
canales = registro.sig_name  
fs = registro.fs  

# Seleccionar el canal deseado
canal_seleccionado = 0  
señal = datos[:, canal_seleccionado]
nombre_canal = canales[canal_seleccionado]

# Estadísticos descriptivos
# 1. Cálculo manual
media_manual = sum(señal) / len(señal)
varianza_manual = sum((x - media_manual) ** 2 for x in señal) / len(señal)
desviación_manual = varianza_manual ** 0.5
coef_variación_manual = desviación_manual / media_manual

# 2. Cálculo con funciones predefinidas
media_numpy = np.mean(señal)
desviación_numpy = np.std(señal)
coef_variación_numpy = desviación_numpy / media_numpy

# Mostrar resultados en consola
print(f"--- Estadísticos")
print(f"Media con formula: {media_manual:.4f}, Media con funcion Python: {media_numpy:.4f}")
print(f"Desviación estándar con formula: {desviación_manual:.4f}, Desviación estándar con funcion Python: {desviación_numpy:.4f}")
print(f"Coeficiente de variación con formula: {coef_variación_manual:.4f}, Coeficiente de variación con funcion Python: {coef_variación_numpy:.4f}")

# Crear histograma y función de probabilidad
hist_data, bins, _ = plt.hist(señal, bins=50, density=True, color='green', alpha=0.6)
bin_centers = (bins[:-1] + bins[1:]) / 2

# Estimación de la función de densidad de probabilidad usando KDE
kde = gaussian_kde(señal)
x_vals = np.linspace(min(señal), max(señal), 100)
pdf_vals = kde(x_vals)

# Crear la interfaz con subplots
fig, axs = plt.subplots(2, 1, figsize=(12, 10))


# grafica 1: Señal EMG
t = np.linspace(0, len(señal) / fs, len(señal))
axs[0].plot(t, señal, color='blue')
axs[0].set_title(f"Señal EMG", fontsize=12)
axs[0].set_xlabel("Tiempo[seg]", fontsize=10)
axs[0].set_ylabel("Voltaje[mV]", fontsize=10)
axs[0].grid()

# grafica 2: Histograma y función de probabilidad
axs[1].hist(señal, bins=50, density=True, color='pink', alpha=0.6, label="Histograma")
axs[1].plot(x_vals, pdf_vals, color='purple', linewidth=2, label=" Funcion de Probabilidad")
axs[1].set_xlabel("Voltaje[mV]", fontsize=10)
axs[1].set_ylabel("Frecuencia[Hz]", fontsize=10)
axs[1].grid()
axs[1].legend(fontsize=10)


# === AGREGAR RUIDO GAUSSIANO === #
sigma_grande = 0.08  
sigma_pequeña = 0.02  

ruidog = np.random.normal(0, sigma_grande, señal.shape)  
ruidop = np.random.normal(0, sigma_pequeña, señal.shape)  
señal_con_ruidog = señal + ruidog  
señal_con_ruidop = señal + ruidop  

# === AGREGAR RUIDO DE IMPULSOS === #
num_impulsos_grande = int(len(señal) * 0.02)  
num_impulsos_pequeño = int(len(señal) * 0.003)  

indices_grande = np.random.randint(0, len(señal), num_impulsos_grande)  
indices_pequeño = np.random.randint(0, len(señal), num_impulsos_pequeño)  

amplitud_impulsos_grande = np.random.choice([-1, 1], num_impulsos_grande) * np.random.uniform(0.2, 1.0, num_impulsos_grande)  
amplitud_impulsos_pequeño = np.random.choice([-1, 1], num_impulsos_pequeño) * np.random.uniform(0.2, 1.0, num_impulsos_pequeño)  

señal_con_impulsosg = señal.copy()  
señal_con_impulsosp = señal.copy()  
señal_con_impulsosg[indices_grande] += amplitud_impulsos_grande  
señal_con_impulsosp[indices_pequeño] += amplitud_impulsos_pequeño  

# === AGREGAR RUIDO DE ARTEFACTO: MOVIMIENTO === #
t = np.linspace(0, len(señal) / fs, len(señal))  

amplitud_mov_grande = 0.6 * np.max(señal)  
amplitud_mov_pequeña = 0.2 * np.max(señal)  
frecuencia_mov = 0.7  

artefacto_movg = amplitud_mov_grande * np.sin(2 * np.pi * frecuencia_mov * t)  
artefacto_movp = amplitud_mov_pequeña * np.sin(2 * np.pi * frecuencia_mov * t)  

señal_con_artefactog = señal + artefacto_movg  
señal_con_artefactop = señal + artefacto_movp  

# === Cálculo del SNR para cada tipo de ruido con la nueva ecuación === #
snr_gaussiano_grande = calcular_snr(señal, señal_con_ruidog)
snr_gaussiano_pequeño = calcular_snr(señal, señal_con_ruidop)
snr_impulsos_grande = calcular_snr(señal, señal_con_impulsosg)
snr_impulsos_pequeño = calcular_snr(señal, señal_con_impulsosp)
snr_artefacto_grande = calcular_snr(señal, señal_con_artefactog)
snr_artefacto_pequeño = calcular_snr(señal, señal_con_artefactop)

# === Imprimir los valores de SNR corregidos === #
print("\n=== SNR de las señales contaminadas ===")
print(f"SNR Ruido Gaussiano (A. Grande): {snr_gaussiano_grande:.2f} dB")
print(f"SNR Ruido Gaussiano (A. Pequeña): {snr_gaussiano_pequeño:.2f} dB")
print(f"SNR Ruido de Impulsos (A. Grande): {snr_impulsos_grande:.2f} dB")
print(f"SNR Ruido de Impulsos (A. Pequeña): {snr_impulsos_pequeño:.2f} dB")
print(f"SNR Artefacto Movimiento (A. Grande): {snr_artefacto_grande:.2f} dB")
print(f"SNR Artefacto Movimiento (A. Pequeña): {snr_artefacto_pequeño:.2f} dB")

# === Graficar las señales === #
fig, axs = plt.subplots(4, 2, figsize=(10, 12))
fig.suptitle("Señales EMG con Diferentes Tipos de Ruido", fontsize=13)

# Señal original
axs[0, 0].plot(t, señal, color='blue')
axs[0, 0].set_title("Señal Original")

# Ruido Gaussiano
axs[1, 0].plot(t, señal_con_ruidog, color='green', alpha=0.7)
axs[1, 0].set_title(f"Ruido Gaussiano (A. Grande) - SNR: {snr_gaussiano_grande:.2f} dB")

axs[1, 1].plot(t, señal_con_ruidop, color='red', alpha=0.7)
axs[1, 1].set_title(f"Ruido Gaussiano (A. Pequeña) - SNR: {snr_gaussiano_pequeño:.2f} dB")

# Ruido de Impulsos
axs[2, 0].plot(t, señal_con_impulsosg, color='yellow', alpha=0.7)
axs[2, 0].set_title(f"Ruido de Impulsos (A. Grande) - SNR: {snr_impulsos_grande:.2f} dB")

axs[2, 1].plot(t, señal_con_impulsosp, color='brown', alpha=0.7)
axs[2, 1].set_title(f"Ruido de Impulsos (A. Pequeña) - SNR: {snr_impulsos_pequeño:.2f} dB")

# Artefacto de Movimiento
axs[3, 0].plot(t, señal_con_artefactog, color='purple', alpha=0.7)
axs[3, 0].set_title(f"Artefacto de Movimiento (A. Grande) - SNR: {snr_artefacto_grande:.2f} dB")

axs[3, 1].plot(t, señal_con_artefactop, color='orange', alpha=0.7)
axs[3, 1].set_title(f"Artefacto de Movimiento (A. Pequeña) - SNR: {snr_artefacto_pequeño:.2f} dB")

# Formato de las gráficas
for ax in axs.flat:
    ax.set_xlabel("")
    ax.set_ylabel("Voltaje[mV]")
    ax.grid()

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
