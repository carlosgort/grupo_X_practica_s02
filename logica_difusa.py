# logica_difusa.py
"""
Módulo de Lógica Difusa para la Gestión Gradual de Ocupación de Zona.
"""

import numpy as np
import matplotlib.pyplot as plt


def triangular(x, a, b, c):
    x = np.asarray(x, dtype=float)
    resultado = np.zeros_like(x)
    
    mask_subida = (x >= a) & (x <= b) & (b > a)
    resultado[mask_subida] = (x[mask_subida] - a) / (b - a)
    
    mask_bajada = (x > b) & (x <= c) & (c > b)
    resultado[mask_bajada] = (c - x[mask_bajada]) / (c - b)
    
    resultado[x == b] = 1.0
    return resultado if resultado.shape != () else float(resultado)


def trapezoidal(x, a, b, c, d):
    x = np.asarray(x, dtype=float)
    resultado = np.zeros_like(x)
    
    if a == b:
        mask_izq = (x <= a)
        resultado[mask_izq] = 1.0
    else:
        mask_subida = (x >= a) & (x < b)
        resultado[mask_subida] = (x[mask_subida] - a) / (b - a)
        
    mask_centro = (x >= b) & (x <= c)
    resultado[mask_centro] = 1.0
    
    if c == d:
        mask_der = (x >= c)
        resultado[mask_der] = 1.0
    else:
        mask_bajada = (x > c) & (x <= d)
        resultado[mask_bajada] = (d - x[mask_bajada]) / (d - c)
        
    return resultado if resultado.shape != () else float(resultado)


def fuzzificar_ocupacion(o):
    return {
        "baja": trapezoidal(o, 0, 0, 40, 55),
        "media": triangular(o, 45, 65, 85),
        "alta": trapezoidal(o, 70, 85, 100, 100)
    }


def evaluar_salida_desvio(d_grid):
    return {
        "bajo": trapezoidal(d_grid, 0, 0, 20, 40),
        "medio": triangular(d_grid, 25, 50, 75),
        "alto": trapezoidal(d_grid, 60, 80, 100, 100)
    }


def inferir_desvio(o):
    o = np.clip(o, 0.0, 100.0)
    grados = fuzzificar_ocupacion(o)
    
    d_grid = np.linspace(0, 100, 1001)
    mf_salida = evaluar_salida_desvio(d_grid)
    
    act_baja = grados["baja"]
    act_media = grados["media"]
    act_alta = grados["alta"]
    
    activaciones = {
        "D1": act_baja,
        "D2": act_media,
        "D3": act_alta
    }
    
    rec_bajo = np.minimum(act_baja, mf_salida["bajo"])
    rec_medio = np.minimum(act_media, mf_salida["medio"])
    rec_alto = np.minimum(act_alta, mf_salida["alto"])
    
    salida_agregada = np.maximum(np.maximum(rec_bajo, rec_medio), rec_alto)
    
    suma_pesos = np.sum(salida_agregada)
    if suma_pesos == 0:
        d_final = 0.0
    else:
        d_final = np.sum(d_grid * salida_agregada) / suma_pesos
        
    return grados, activaciones, d_grid, salida_agregada, float(d_final)


def generar_grafico_difuso(o_actual=None):
    x_grid = np.linspace(0, 100, 1001)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    ax1.plot(x_grid, trapezoidal(x_grid, 0, 0, 40, 55), label="Baja", color="blue")
    ax1.plot(x_grid, triangular(x_grid, 45, 65, 85), label="Media", color="orange")
    ax1.plot(x_grid, trapezoidal(x_grid, 70, 85, 100, 100), label="Alta", color="red")
    ax1.set_title("Variable de Entrada: Ocupación (%)")
    ax1.set_xlabel("Ocupación")
    ax1.set_ylabel("Grado de Pertenencia")
    ax1.grid(True, linestyle="--", alpha=0.6)
    
    if o_actual is not None:
        ax1.axvline(x=o_actual, color="black", linestyle=":", label=f"Actual ({o_actual}%)")
    ax1.legend()
    
    ax2.plot(x_grid, trapezoidal(x_grid, 0, 0, 20, 40), label="Bajo", color="blue")
    ax2.plot(x_grid, triangular(x_grid, 25, 50, 75), label="Medio", color="orange")
    ax2.plot(x_grid, trapezoidal(x_grid, 60, 80, 100, 100), label="Alto", color="red")
    ax2.set_title("Variable de Salida: Nivel de Desvío (%)")
    ax2.set_xlabel("Desvío")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend()
    
    plt.tight_layout()
    return fig