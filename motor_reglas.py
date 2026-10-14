# motor_reglas.py
"""
Módulo del Sistema Experto Clásico.
Contiene la base de conocimiento y el motor de inferencia
con encadenamiento hacia adelante y registro de traza.
"""

REGLAS_INICIALES = [
    {
        "nombre": "R1",
        "condiciones": {"codigo_no_legible"},
        "conclusion": "solicitar_lectura_manual"
    },
    {
        "nombre": "R2",
        "condiciones": {"solicitar_lectura_manual", "destino_no_identificado"},
        "conclusion": "enviar_revision"
    },
    {
        "nombre": "R3",
        "condiciones": {"embalaje_danado", "contenido_fragil"},
        "conclusion": "enviar_revision"
    },
    {
        "nombre": "R4",
        "condiciones": {"peso_fuera_rango"},
        "conclusion": "comprobar_peso"
    },
    {
        "nombre": "R5",
        "condiciones": {"comprobar_peso", "documentacion_incompleta"},
        "conclusion": "retener_temporalmente"
    },
    {
        "nombre": "R6",
        "condiciones": {"destino_identificado", "sin_incidencias"},
        "conclusion": "autorizar_clasificacion"
    },
    {
        "nombre": "R7",
        "condiciones": {"embalaje_danado"},
        "conclusion": "solicitar_reembalaje"
    }
]


def encadenar_hacia_adelante(hechos_iniciales, reglas=None):
    if reglas is None:
        reglas = REGLAS_INICIALES

    hechos = set(hechos_iniciales)
    traza = []
    hay_novedad = True
    
    while hay_novedad:
        hay_novedad = False
        
        for regla in reglas:
            condiciones = regla["condiciones"]
            conclusion = regla["conclusion"]
            
            if condiciones.issubset(hechos) and conclusion not in hechos:
                hechos.add(conclusion)
                traza.append({
                    "regla": regla["nombre"],
                    "condiciones": list(condiciones),
                    "conclusion": conclusion
                })
                hay_novedad = True
                
    return hechos, traza


def mostrar_traza(hechos_iniciales, hechos_finales, traza):
    print("\n" + "="*50)
    print(" TRAZA DE INFERENCIA DE LA DECISIÓN")
    print("="*50)
    print("Hechos iniciales detectados:")
    for h in hechos_iniciales:
        print(f"  - {h}")
    print("\nSecuencia de razonamiento:")
    
    if not traza:
        print("  (No se activó ninguna regla. No se generaron nuevas conclusiones)")
    else:
        for i, paso in enumerate(traza, 1):
            conds_texto = " + ".join(paso["condiciones"])
            print(f"  Paso {i}: [{paso['regla']}] {conds_texto} -> {paso['conclusion']}")
            
    print("\nConclusiones o estados finales alcanzados:")
    hechos_nuevos = hechos_finales - set(hechos_iniciales)
    if hechos_nuevos:
        for h in hechos_nuevos:
            print(f"  * {h}")
    else:
        print("  * Ninguna conclusión derivada.")
    print("="*50 + "\n")