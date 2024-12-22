import numpy as np
import matplotlib.pyplot as plt


def compute_energy(signal, window_size=512):
    energy = [np.sum(signal[i:i + window_size] ** 2) for i in range(0, len(signal), window_size)]
    return np.array(energy)


def compute_energies(df):
    truco_dos_signal = df[df['source_file'] == 'data/truco_dos.dat']['eeg_filtered_13-30Hz']
    truco_siete_signal = df[df['source_file'] == 'data/truco_siete.dat']['eeg_filtered_13-40Hz']

    truco_dos_energy = compute_energy(truco_dos_signal)
    truco_siete_energy = compute_energy(truco_siete_signal)

    return truco_siete_energy, truco_dos_energy
