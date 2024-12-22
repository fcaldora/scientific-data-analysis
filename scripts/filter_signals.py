from filters.spectral_filter import bandpass_filter


def filter_signals(df):
    fs = 512
    activity_filters = {
        'data/baseline.dat': (0.5, 8),  # Delta + Theta
        'data/beethoven.dat': (8, 13),  # Alpha
        'data/deathmetal.dat': (13, 30),  # Beta
        'data/truco_siete.dat': (13, 40),  # Beta + Gamma
        'data/pestaneos.dat': (0.5, 4),  # Delta
        'data/risa.dat': (13, 40),  # Beta + Gamma
        'data/truco_dos.dat': (13, 30),  # Beta
        'data/truco_secuencia.dat': (13, 40),  # Beta + Gamma
    }

    filtered_signals = {}
    for file, (lowcut, highcut) in activity_filters.items():
        signal = df[df['source_file'] == file]['eeg']
        filtered_signal = bandpass_filter(signal, lowcut, highcut, fs)
        filtered_signals[file] = filtered_signal
        df.loc[df['source_file'] == file, f'eeg_filtered_{lowcut}-{highcut}Hz'] = filtered_signal

    return filtered_signals, df
