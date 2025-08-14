# LABORATORIO-1-PDS

## SNR (Relación Señal Ruido)

Es una medida de cuantificación para evaluar una señal deseada comparando el ruido presentado (interferencia no deseada que degrada la calidad de la información) , es decir medir cuanto de lo que se desea ver esta presente en relación con lo que no. Entre mas alto sea el valor de SNR indican una señal más clara y con menos ruido. 

En este caso para la señal requerida, en la señal EMG el SNR es un parámetro que determina la calidad de esta y su utilidad para un analisis adecuado biomecánico y clínico. Un SNR alto indica una señal clara con poca interferenciay un SNR bajo sugiere que el ruido afecta los datos señalados.

Para calcular el SNR debe compararse la intensidad de la señal con el ruido de fondo, la formula para hallar este valor que se presenta en (dB) es la siguiente:
![image](https://github.com/user-attachments/assets/46d4cdff-f816-4780-b637-de251b41f5a1)
 
 *Formula para calcular SNR (Relación Señal Ruido)*
 
Esta técnica de medición tiene una aplicación muy importante ya sea en el uso de señales de internet, de sonido y de igual manera identificar el ruido para tomar decisiones respecto a esa señal. Se clasifican en tres tipos de ruido:

#### Ruido Gaussiano:
sigue una distribución normal con una media y una desviación estandar, los valores cercanos se relacionan con la media y los extremos no son frecuentes.

#### Ruido de impulso: 
Son valores aletorios en su mayoria grandes y en algunas muestras de la señal, se simulan picos de ruido de gran amplitud. 

#### Ruido tipo artefacto:
Se debe a movimientos o interferencias electricas pueden ser de baja frecuencia en este caso una señal seno.

## Ruidos en la señal aplicada
Se agregan estos tres tipos de ruidos a la señal EMG con diferentes amplitudes cada uno, es decir por cada ruido una onda grande y una mas pequeña. 

En el primer caso se agrega el ruido gaussiano y con cada amplitud se obtienen valores de SNR:
![image](https://github.com/user-attachments/assets/3ef0a4f7-c747-4257-ae5a-d149658f392e)

*Ruido Gaussiano con Amplitud Grande y Pequeña*

SNR(Amplitud Grande de 8mV): 0.94dB que indica que la potencia del ruido y la señal EMG son similares por lo que no se logra distinguir la señal esto justifica el valor bajo de SNR

SNR(Amplitud Pequeña de 2mV): 6.94dB este valor indica que la potencia del ruido es menos por lo cual la señal se logra identificar pero con una pequeña distorsión
