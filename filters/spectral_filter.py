from scipy.signal import butter, filtfilt, lfilter


def bandpass_filter(signal, lowcut, highcut, fs, order=4):
    """
    Aplica un filtro pasa-banda a una señal.

    Parámetros:
    - signal: array de la señal original.
    - lowcut: frecuencia mínima del pasa-banda.
    - highcut: frecuencia máxima del pasa-banda.
    - fs: frecuencia de muestreo (Hz).
    - order: orden del filtro Butterworth.

    Retorna:
    - Señal filtrada.
    """
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, signal)
