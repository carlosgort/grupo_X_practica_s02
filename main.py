# main.py
"""
Módulo de Interfaz de Consola (Obligatoria).
"""

import sys
from motor_reglas import encadenar_hacia_adelante, mostrar_traza
from logica_difusa import inferir_desvio, generar_grafico_difuso
import matplotlib.pyplot as plt


def menu_sistema_experto():
    print("\n" + "="*60)
    print(" 1. ZONA DEL SISTEMA EXPERTO CLÁSICO (GESTOR DE INCIDENCIAS)")
    print("="*60)
    print("Marque con 's' (Sí) o 'n' (No) los hechos observados en el paquete:")
    
    hechos_disponibles = [
        ("codigo_no_legible", "¿El código de barras es ilegible?"),
        ("destino_no_identificado", "¿El destino NO está identificado?"),
        ("destino_identificado", "¿El destino SÍ está identificado?"),
        ("embalaje_danado", "¿El embalaje presenta daños visibles?"),
        ("contenido_fragil", "¿El contenido está marcado como frágil?"),
        ("peso_fuera_rango", "¿El peso está fuera de los márgenes permitidos?"),
        ("documentacion_incompleta", "¿Falta documentación del envío?"),
        ("sin_incidencias", "¿El paquete NO presenta ninguna incidencia visual?")
    ]
    
    hechos_iniciales = set()
    for clave, pregunta in hechos_disponibles:
        resp = input(f"  {pregunta} (s/n): ").strip().lower()
        if resp == 's':
            hechos_iniciales.add(clave)
            
    print("\n[PROCESANDO INFERENCIA EN ENCADENAMIENTO HACIA ADELANTE...]")
    hechos_finales, traza = encadenar_hacia_adelante(hechos_iniciales)
    mostrar_traza(hechos_iniciales, hechos_finales, traza)


def menu_sistema_difuso():
    print("\n" + "="*60)
    print(" 2. ZONA DEL SISTEMA DIFUSO (OCUPACIÓN DE ZONAS)")
    print("="*60)
    
    while True:
        try:
            val_str = input("Introduzca el porcentaje de ocupación de la zona (0 a 100%): ")
            ocupacion = float(val_str)
            if 0 <= ocupacion <= 100:
                break
            else:
                print("  [Error] El valor debe estar comprendido entre 0 y 100.")
        except ValueError:
            print("  [Error] Debe introducir un valor numérico válido.")
            
    grados, activaciones, _, _, desvio_final = inferir_desvio(ocupacion)
    
    print("\n" + "-"*50)
    print(f" RESULTADOS DE EVALUACIÓN DIFUSA EN ZONA ({ocupacion}% OCUPACIÓN)")
    print("-"*50)
    print("1. Grados de Pertenencia (Fuzzificación):")
    for termino, grado in grados.items():
        print(f"   - Ocupación {termino.capitalize()}: {grado:.3f}")
        
    print("\n2. Activación de Reglas Difusas:")
    for regla, act in activaciones.items():
        print(f"   - Regla {regla}: Grado de activación = {act:.3f}")
        
    print(f"\n3. Nivel de Desvío Recomendado (Desfuzzificación Centroide):")
    print(f"   >>> {desvio_final:.2f}% de paquetes deben desviarse <<<")
    print("-"*50)
    
    resp_graf = input("\n¿Desea visualizar la gráfica de las funciones de pertenencia? (s/n): ").strip().lower()
    if resp_graf == 's':
        fig = generar_grafico_difuso(ocupacion)
        plt.show()


def main():
    while True:
        print("\n" + "="*60)
        print(" SISTEMA EXPERTO Y DIFUSO - CENTRO LOGÍSTICO")
        print("="*60)
        print(" 1. Evaluar incidencia de un paquete (Sistema Experto)")
        print(" 2. Evaluar nivel de desvío por ocupación (Lógica Difusa)")
        print(" 3. Salir")
        
        opcion = input("\nSeleccione una opción (1-3): ").strip()
        
        if opcion == '1':
            menu_sistema_experto()
        elif opcion == '2':
            menu_sistema_difuso()
        elif opcion == '3':
            print("\nSaliendo del sistema...\n")
            sys.exit(0)
        else:
            print("Opción no válida. Por favor, seleccione 1, 2 o 3.")


if __name__ == "__main__":
    main()