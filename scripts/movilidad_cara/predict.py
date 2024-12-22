import matplotlib.pyplot as plt
import numpy as np

from scripts.movilidad_cara.train_model import compute_features_with_entropy


def predict(data, clf, window_size, Fs):

    truco_secuencia_features = compute_features_with_entropy(data.values, window_size)
    truco_secuencia_predictions = clf.predict(truco_secuencia_features)

    time_stamps = np.arange(len(truco_secuencia_predictions)) * (window_size / Fs)  # Tiempo en segundos

    plt.figure(figsize=(12, 6))
    plt.step(time_stamps, truco_secuencia_predictions, where='post', label='Predicciones', color='blue', alpha=0.7)
    plt.title('Predicciones en Truco_secuencia')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Etiqueta Predicha')
    plt.yticks([0, 1, 2], ['Baseline', 'Truco_dos', 'Truco_siete'])
    plt.grid(alpha=0.5)
    plt.legend()
    #plt.show()
    plt.savefig('outputs/truco_secuencia.png')
