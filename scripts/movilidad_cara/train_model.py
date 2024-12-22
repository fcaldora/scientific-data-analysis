import numpy as np
from scipy.stats import entropy
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV


def calculate_entropy_with_histogram(signal, bins=10, base=2):
    hist, _ = np.histogram(signal, bins=bins, density=True)
    return entropy(hist + 1e-8, base=base)


def compute_hjorth_parameters(signal):
    first_derivative = np.diff(signal)
    second_derivative = np.diff(first_derivative)
    activity = np.var(signal)
    complexity = np.sqrt(np.var(first_derivative) / activity) if activity != 0 else 0
    morbidity = (np.sqrt(np.var(second_derivative) / np.var(first_derivative)) / complexity
                 if complexity != 0 and np.var(first_derivative) != 0 else 0)
    return activity, complexity, morbidity


def compute_features_with_entropy(signal, window_size):
    features = []
    for i in range(0, len(signal), window_size):
        window = signal[i:i + window_size]
        if len(window) < window_size:
            continue
        p2p = np.max(window) - np.min(window)
        rms = np.sqrt(np.mean(window ** 2))
        crest_factor = np.max(np.abs(window)) / rms if rms != 0 else 0
        shannon_entropy = calculate_entropy_with_histogram(window, bins=10)
        activity, complexity, morbidity = compute_hjorth_parameters(window)
        fractal = np.log(len(window)) / np.log(np.std(window) + 1e-8)
        features.append([p2p, rms, crest_factor, shannon_entropy, activity, complexity, morbidity, fractal])
    return np.array(features)


def train_model(df, window_size):
    print('-signal length-')
    print(len(df[df['source_file'] == 'data/baseline.dat']['eeg_filtered_0.5-8Hz'].values))
    baseline_features = compute_features_with_entropy(df[df['source_file'] == 'data/baseline.dat']['eeg_filtered_0.5-8Hz'].values, window_size)
    truco_dos_features = compute_features_with_entropy(df[df['source_file'] == 'data/truco_dos.dat']['eeg_filtered_13-30Hz'].values, window_size)
    truco_siete_features = compute_features_with_entropy(df[df['source_file'] == 'data/truco_siete.dat']['eeg_filtered_13-40Hz'].values, window_size)
    #baseline_features = compute_features_with_entropy(df[df['source_file'] == 'data/baseline.dat']['eeg'].values, window_size)
    #truco_dos_features = compute_features_with_entropy(df[df['source_file'] == 'data/truco_dos.dat']['eeg'].values, window_size)
    #truco_siete_features = compute_features_with_entropy(df[df['source_file'] == 'data/truco_siete.dat']['eeg'].values, window_size)

    print('-baseline-')
    print(len(baseline_features))
    print(baseline_features)
    print('-truco dos-')
    print(len(truco_dos_features))
    print(truco_dos_features)
    print('-truco siete-')
    print(len(truco_siete_features))
    print(truco_siete_features)

    baseline_labels = np.zeros(len(baseline_features))
    truco_dos_labels = np.ones(len(truco_dos_features))
    truco_siete_labels = np.full(len(truco_siete_features), 2)

    X = np.vstack([baseline_features, truco_dos_features, truco_siete_features])
    y = np.concatenate([baseline_labels, truco_dos_labels, truco_siete_labels])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # param_grid = {
    #     'n_estimators': [50, 100, 200, 500],
    #     'max_depth': [5, 10, 15, 20],
    #     'min_samples_split': [2, 3, 5, 7, 10],
    #     'min_samples_leaf': [1, 2, 4, 5],
    #     'max_features': ['sqrt', 'log2', None]
    # }

    clf = RandomForestClassifier(random_state=42)

    # Configurar GridSearchCV
    # grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, verbose=2, n_jobs=-1)

    # Ejecutar búsqueda
    clf.fit(X_train, y_train)

    # Mejor combinación de hiperparámetros
    # print("Mejores parámetros:", grid_search.best_params_)
    # clf = grid_search.best_estimator_

    #clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(y_test)
    print(y_pred)
    classification_report_results = classification_report(y_test, y_pred)
    confusion_matrix_results = confusion_matrix(y_test, y_pred)

    print("Reporte de Clasificación:")
    print(classification_report_results)

    print("Matriz de Confusión:")
    print(confusion_matrix_results)

    return clf
