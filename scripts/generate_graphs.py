import pandas as pd
import matplotlib.pyplot as plt
import os


def generate_all_graphs():
    os.makedirs('outputs', exist_ok=True)

    data_files = ['data/baseline.dat', 'data/bethoven.dat', 'data/deathmetal.dat', 'data/pestaneos.dat',
                  'data/risa.dat', 'data/truco_dos.dat', 'data/truco_secuencia.dat', 'data/truco_siete.dat']
    dataframes = []
    for file in data_files:
        df = pd.read_csv(file, delimiter=' ', names=['timestamp', 'counter', 'eeg',
                                                     'attention', 'meditation', 'blinking'])
        df['source_file'] = file
        dataframes.append(df)
    df = pd.concat(dataframes, ignore_index=True)

    # Histograma de EEG
    plt.figure(figsize=(10, 6))
    plt.hist(df['eeg'], bins=50, alpha=0.7, color='blue', edgecolor='black')
    plt.title('Distribución de la Variable EEG')
    plt.xlabel('EEG')
    plt.ylabel('Frecuencia')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('outputs/eeg_histogram.png')
    plt.close()

    # Gráfico de líneas (tendencia de EEG)
    # sample_df = df.sample(1000).sort_values(by='timestamp')
    # plt.figure(figsize=(12, 6))
    # plt.plot(sample_df['timestamp'], sample_df['eeg'], label='EEG', alpha=0.8)
    # plt.title('Tendencia de EEG en el Tiempo')
    # plt.xlabel('Timestamp')
    # plt.ylabel('EEG')
    # plt.grid(axis='both', linestyle='--', alpha=0.7)
    # plt.legend()
    # plt.savefig('outputs/eeg_trend.png')
    # plt.close()

    plt.figure(figsize=(12, 6))
    for file in data_files:
        file_data = df[df['source_file'] == file].sample(500).sort_values(by='timestamp')
        plt.plot(
            file_data['timestamp'],
            file_data['eeg'],
            label=file,
            alpha=0.8
        )
    plt.title('Comparacioón de señales EEG por Archivo')
    plt.xlabel('Timestamp')
    plt.ylabel('EEG')
    plt.legend(title="Archivo")
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.savefig('outputs/eeg_trend_by_file.png')
    plt.close()

    # Boxplot de EEG por archivo
    # plt.figure(figsize=(12, 6))
    # sns.boxplot(data=df, x='source_file', y='eeg')
    # plt.title('Distribución de EEG por Archivo')
    # plt.xlabel('Archivo')
    # plt.ylabel('EEG')
    # plt.xticks(rotation=45)
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.savefig('outputs/eeg_boxplot_by_file.png')
    # plt.close()

    print("Gráficos generados y guardados en 'outputs/'")
    return df
