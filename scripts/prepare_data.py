import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


# Extraer características (e.g., media, varianza, energía)
def extract_features(signal):
    return {
        'mean': np.mean(signal),
        'std': np.std(signal),
        'energy': np.sum(signal ** 2),
        'max': np.max(signal),
        'min': np.min(signal)
    }


def build_data(df, compare_file):
    # Filtrar datos para BASELINE y otro bloque
    baseline_data = df[df['source_file'] == 'data/baseline.dat']
    activity_data = df[df['source_file'] == compare_file]

    # Etiquetar datos
    baseline_data['label'] = 0
    activity_data['label'] = 1

    combined_data = pd.concat([baseline_data, activity_data])

    # Generar un DataFrame de características
    features = combined_data.groupby(['source_file', 'label']).apply(
        lambda x: pd.Series(extract_features(x['eeg']))
    ).reset_index()

    # Dividir en entrenamiento y prueba
    X = features.drop(['source_file', 'label'], axis=1)
    y = features['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    return X_train, X_test, y_train, y_test
