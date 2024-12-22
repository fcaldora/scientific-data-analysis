from datetime import datetime

from fpdf import FPDF
import os


def create_pdf():
    os.makedirs('outputs', exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # portada
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Análisis de Datos Científicos y Geográficos", ln=True, align="C")
    pdf.ln(20)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "TP Final: Procesamiento de señales EEG", ln=True, align="C")

    # Autor y Fecha
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Autor: Facundo Caldora", ln=True, align="C")
    pdf.cell(0, 10, f"DNI: 34866599", ln=True, align="C")
    pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", ln=True, align="C")
    pdf.ln(30)

    pdf.image("//Users/fcaldora/itba_logo.jpg", x=50, y=120, w=110)  #

    #-------------------------------------

    # intro
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Introducción y Descripción de los Datos', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    intro_text = (
        "Este informe presenta un análisis exploratorio de datos (EDA) basado en señales EEG captadas por sensores "
        "colocados en la cabeza. Los datos se dividen en 8 archivos, cada uno representando distintas sesiones de captura. "
        "Las variables analizadas incluyen:\n\n"
        "- 'timestamp': momento de captura del dato.\n"
        "- 'eeg': señal eléctrica cerebral.\n"
        "- 'attention', 'meditation', 'blinking': características del comportamiento del usuario durante la captura.\n\n"
        "El análisis inicial incluye visualizaciones que destacan las principales características de las señales EEG. "
        "En la Figura 1 se presenta la distribución global de la señal EEG, mostrando su rango y concentración de valores. "
        "La Figura 2 ilustra la tendencia temporal de EEG, separando los datos por archivo para facilitar la comparación "
        "de las señales entre distintas sesiones.\n\n"
    )
    pdf.multi_cell(0, 10, intro_text)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Distribución de la Variable EEG', 0, 1, 'L')
    pdf.image('outputs/eeg_histogram.png', x=10, y=30, w=180)

    pdf.set_y(150)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Figura 1: Distribución Global de EEG', 0, 1, 'L')

    analysis_text = (
        "La Figura 1 muestra un histograma de la señal EEG para todos los archivos combinados. La distribución "
        "presenta una concentración central cercana a 0, con valores que oscilan entre -500 y 500."
    )
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, analysis_text)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Comparación de señales EEG por Archivo', 0, 1, 'L')
    pdf.image('outputs/eeg_trend_by_file.png', x=10, y=30, w=180)

    pdf.set_y(130)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Figura 2: Comparación de señales EEG por Archivo', 0, 1, 'L')

    analysis_text = (
        "La Figura 2 visualiza la señal EEG a lo largo del tiempo para cada archivo, destacando diferencias entre sesiones. "
        "Por ejemplo, los datos de 'risa.dat' muestran una mayor variabilidad y valores extremos, mientras que "
        "'bethoven.dat' exhibe señales más consistentes."
    )
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, analysis_text)

    # Experimento
    # Página de introducción al análisis y clasificador
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Objetivo propuesto: Análisis de Movimientos Faciales y Clasificación', 0, 1, 'L')

    # Introducción general
    intro_text = (
        "El plan será identificar diferencias en las señales EEG asociadas a movimientos faciales "
        "específicos, como los realizados durante los bloques Truco_dos (tirar besos) y Truco_siete (muecas). Para lograr esto, "
        "primero se hizo un cálculo de la energía de las señales filtradas en bandas de interés y el entrenamiento "
        "de un modelo supervisado que clasifica las actividades.\n\n"
        "Al obtener desempeños bajos (cerca del 58%) de los clasificadores, utilizando únicamente la energía de las señales, "
        "se optó por calcular otras features de la señal, basándose en el script `signalfeatures.py`.\n\n")
    analysis_content = (
        "Para abordar este problema, se siguieron los siguientes pasos:\n"
        "1. Filtrado de Señales:\n"
        "   Se aplicaron filtros pasa-banda para aislar las bandas de frecuencia de interés.\n"
        "2. Feature extraction:\n"
        "   Se calcularon múltiples características, incluyendo:\n"
        "   - Estadísticas Temporales: Peak-to-Peak, RMS, Crest Factor.\n"
        "   - Complejidad de la Señal: Parámetros de Hjorth (Activity, Complexity, Morbidity).\n"
        "   - Entropía de Shannon (calculada mediante histogramas).\n"
        "   - Fractalidad de la señal.\n"
        "3. Clasificación:\n"
        "   Un modelo Random Forest fue entrenado con las características extraídas para clasificar las actividades Truco_dos, "
        "Truco_siete y Baseline.\n"
        "4. Predicción en Truco_secuencia:\n"
        "   Finalmente, se utilizó el modelo entrenado para predecir las etiquetas de cada ventana temporal en el archivo "
        "Truco_secuencia."
    )
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, intro_text + analysis_content)

    # -----------------------------------------------------------------

    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '1 - Filtros y frecuencias elegidas', 0, 1, 'L')

    # intro
    intro_text = (
        "En este análisis, se implementaron filtros espectrales pasa-banda para aislar bandas de frecuencia específicas en los datos EEG, "
        "correspondientes a las actividades capturadas en cada archivo. A continuación, se describe cada actividad y las frecuencias seleccionadas:"
    )
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, intro_text)

    # frecuencias y archivos
    activity_descriptions = [
        ("data/baseline.dat", "Actividad en reposo", "0.5-8 Hz (Delta + Theta)",
         "Estados de relajación profunda y regeneración cerebral."),
        ("data/truco_siete.dat", "Juego truco - mueca", "13-40 Hz (Beta + Gamma)",
         "Actividad motora relacionada con movimientos de la boca."),
        ("data/truco_dos.dat", "Juego truco - tirar un beso", "13-30 Hz (Beta)",
         "Actividad motora breve asociada al gesto."),
        ("data/truco_secuencia.dat", "Señales intercaladas entre truco 2 y 7", "13-40 Hz (Beta + Gamma)",
         "Combinación de actividades motoras rápidas y breves.")
    ]

    for file_name, activity, freq, description in activity_descriptions:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 10, f"{file_name} - {activity}", 0, 1, 'L')
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 10, f"  Frecuencia: {freq}\n  Descripción: {description}\n")

    # -----------------------------------------------------------------

    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '2 - Feature extraction', 0, 1, 'L')

    # intro
    description = (
        "Para calcular la entropía de Shannon, se consideraron dos enfoques posibles: el uso de histogramas y el "
        "uso de contadores (Counter) como indica el archivo `signalfeature.py`. Aunque los datos EEG están "
        "discretizados debido al muestreo a 512 Hz,"
        " su naturaleza de alta resolución (valores en punto flotante) genera una gran cantidad de valores únicos."
        " Por ello, el enfoque basado en histogramas resultó ser más adecuado. Este método divide los datos "
        "en intervalos (bins), lo que permite estimar la distribución de probabilidad de manera más robusta "
        "y adecuada para datos continuos. Esto es particularmente útil en señales EEG, donde los valores"
        " únicos pueden ser numerosos, incluso después del muestreo. El histograma genera una representación "
        "agregada de los valores, mientras que Counter considera cada valor único como una categoría distinta."
        " Para señales EEG con alta resolución, Counter puede sobrestimar la complejidad debido a la falta de"
        " agrupación, mientras que los histogramas logran una estimación más precisa y útil para el análisis."
    )
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, description)

    # -----------------------------------------------------------------

    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '3 & 4 - Clasificación y predicción', 0, 1, 'L')

    # intro
    description = (
        "Tras la extracción de características, se utilizó un modelo de clasificación supervisado basado en Random Forest. "
        "Los datos extraídos de los bloques Baseline, Truco_dos, y Truco_siete se dividieron en un conjunto de entrenamiento (70%) "
        "y prueba (30%). El modelo fue entrenado para identificar patrones específicos asociados con cada clase."
        " Las métricas de evaluación (precisión, recall y F1-Score) revelaron que la clase Baseline fue la más fácil de identificar, "
        "mientras que Truco_dos y Truco_siete presentaron cierta confusión debido a la similitud en sus características."
        "El modelo entrenado fue posteriormente aplicado al archivo Truco_secuencia, que combina señales de Truco_dos "
        "y Truco_siete."
        "Esta predicción fue representada gráficamente para resaltar los cambios temporales en las etiquetas "
        "predichas a lo largo del tiempo."
    )
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, description)

    # -----------------------------------------------------------------

    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Resultados obtenidos', 0, 1, 'L')

    results_content = (
        "El modelo alcanzó una precisión promedio del 93%, " 
        "y además, obtuvo una puntuación F1 de 0.93. Vale la pena aclarar que se hicieron intentos de "
        "optimización de hiper-parámetros con GridSearch, e incluso sin filtrar las señales para obtener "
        "resultados comparativos. Finalmente, se utilizó el random forest original con las señales filtradas. "
        "A continuación se grafica la predicción de truco_secuencia a lo largo del tiempo."
    )
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, results_content)

    pdf.set_y(85)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Predicción secuencia truco:', 0, 1, 'L')

    pdf.image('outputs/truco_secuencia.png', x=10, y=100, w=180)

    # -----------------------------------------------------------------
    # Conclusiones
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Conclusiones', 0, 1, 'L')
    conclusion_content = (
        "Este análisis demuestra que es posible identificar patrones específicos en las señales EEG asociadas a actividades "
        "faciales mediante un enfoque de filtrado, extracción de características y clasificación supervisada.\n\n"
        "A través de Random Forest logramos una precisión promedio del 93% para predecir a que corresponde un bloque de "
        "una señal eeg registrada.\n"
        "A pesar de ello, recordando la persona siendo grabada en clase, y comparando con la predicción obtenida, es posible "
        "que tengamos un caso de overfitting, ya que no veo ninguna predicción de 'baseline', es decir, la persona en estado "
        "de resposo, y cuando lo grabamos la persona si bien hizo las dos señales casi constantemente, tuvo sus momentos de "
        "no hacer nada."
        "En conclusión, sería valioso poder hacer un análisis con mayor cantidad de datos y registros, para poder entrenar "
        "al modelo con mayor cantidad de casos y así obtener un modelo predictor con menor overfitting y mayor precisión."
    )

    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, conclusion_content)

    #
    # pdf.add_page()
    # pdf.set_font('Arial', 'B', 12)
    # pdf.cell(0, 10, 'Distribución de Variables (Boxplot)', 0, 1, 'L')
    # pdf.image('outputs/boxplots.png', x=10, y=30, w=180)
    #

    # Guardar PDF
    pdf.output('outputs/TPFinalFacundoCaldora.pdf')
    print("PDF generado en 'outputs/TPFinalFacundoCaldora.pdf'")

