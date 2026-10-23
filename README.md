# Sistema Experto Explicable y Lógica Difusa - Centro Logístico

Proyecto desarrollado para la práctica S02 del módulo de Inteligencia Artificial.

## 1. Integrantes
* **Daniel Jiménez 1**
* **Gonzalo Frutos 2**
* **Alejandro Pérez 3**
* **Carlos García**

## 2. Estructura del Proyecto
```text
grupo_X_practica_s02/
├── motor_reglas.py         # Motor de reglas y traza
├── logica_difusa.py        # Funciones de pertenencia y ciclo Mamdani
├── main.py                 # Interfaz de consola (Obligatoria)
├── app.py                  # Interfaz Streamlit (Ampliación A10)
├── README.md               # Guía de ejecución
└── informe_grupo_X_s02.pdf # Memoria del trabajo

## 3. Instalación de dependencias
Tener Python version 3.12 o superior instalado
Ejecutar comando 'pip install -r requirements.txt'
## 4. Ejecucución
Interfaz: python main.py
Aplicación web Streamlit: python -m streamlit run app.py

Añade un requirements.txt con este contenido:
numpy
matplotlib
streamlit
