from scripts.filter_signals import filter_signals
from scripts.generate_filtered_graphs import generate_filtered_graphs
from scripts.generate_graphs import generate_all_graphs
from scripts.generate_pdf import create_pdf
from scripts.movilidad_cara.predict import predict
from scripts.movilidad_cara.train_model import train_model


def main():
    print("Generando gráficos inciales...")
    df = generate_all_graphs()

    print("Filtrando señales...")
    filtered_signals, df = filter_signals(df)

    print("Generando gráficos señales filtradas...")
    generate_filtered_graphs(df, filtered_signals)

    frequency = 512

    print("Entrenando modelo...")
    clf = train_model(df, frequency)

    print("Predecir...")
    predict(df[df['source_file'] == 'data/truco_secuencia.dat']['eeg_filtered_13-40Hz'], clf, frequency, frequency)


    print("Creando el informe PDF...")
    create_pdf()


if __name__ == "__main__":
    main()
