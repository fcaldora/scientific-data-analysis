from matplotlib import pyplot as plt


def generate_filtered_graphs(df, filtered_signals):

    plt.figure(figsize=(12, 8))
    for file, filtered_signal in filtered_signals.items():
        plt.plot(
            df[df['source_file'] == file]['timestamp'][:1000],
            filtered_signal[:1000],
            label=file
        )

    plt.title('Señales EEG Filtradas por Actividad')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.legend(title='Archivo / Actividad')
    plt.grid(alpha=0.5)
    plt.savefig('outputs/eeg_filtered.png')
    # plt.show()

