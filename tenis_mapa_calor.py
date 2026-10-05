import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def simular_punto(p_ganar_punto_A):
    return 'A' if random.random() < p_ganar_punto_A else 'B'

def simular_punto_clave(p_ganar_punto_clave_A):
    return 'A' if random.random() < p_ganar_punto_clave_A else 'B'

def simular_juego_normal(p_ganar_punto_A, p_ganar_clave_A):
    puntos_A = 0
    puntos_B = 0
    while True:
        if (puntos_A >= 3 and puntos_A - puntos_B > 0) or (puntos_B >= 3 and puntos_B - puntos_A > 0) :
            if simular_punto_clave(p_ganar_clave_A) == 'A':
                puntos_A += 1
            else:
                puntos_B += 1

        elif simular_punto(p_ganar_punto_A) == 'A':
            puntos_A += 1
        else:
            puntos_B += 1
            
        if puntos_A >= 4 and puntos_A - puntos_B >= 2:
            return 'A'
        elif puntos_B >= 4 and puntos_B - puntos_A >= 2:
            return 'B'

def simular_tiebreak(p_ganar_punto_A, p_ganar_clave_A, puntos_objetivo=7):
    puntos_A = 0
    puntos_B = 0
    while True:
        if (puntos_A >= puntos_objetivo and puntos_A - puntos_B > 0) or (puntos_B >= puntos_objetivo and puntos_B - puntos_A > 0) :
            if simular_punto_clave(p_ganar_clave_A) == 'A':
                puntos_A += 1
            else:
                puntos_B += 1

        elif simular_punto(p_ganar_punto_A) == 'A':
            puntos_A += 1
        else:
            puntos_B += 1
            
        if puntos_A >= puntos_objetivo and puntos_A - puntos_B >= 2:
            return 'A'
        elif puntos_B >= puntos_objetivo and puntos_B - puntos_A >= 2:
            return 'B'

def simular_set(p_ganar_punto_A, p_ganar_clave_A, es_quinto_set=False):
    juegos_A = 0
    juegos_B = 0
    while True:
        if juegos_A == 6 and juegos_B == 6:
            puntos_tb = 10 if es_quinto_set else 7
            return simular_tiebreak(p_ganar_punto_A, p_ganar_clave_A, puntos_objetivo=puntos_tb)
        
        ganador_juego = simular_juego_normal(p_ganar_punto_A, p_ganar_clave_A)
        if ganador_juego == 'A':
            juegos_A += 1
        else:
            juegos_B += 1
            
        if juegos_A >= 6 and juegos_A - juegos_B >= 2:
            return 'A'
        elif juegos_B >= 6 and juegos_B - juegos_A >= 2:
            return 'B'

def simular_partido(prob_A, prob_clave_A):
    sets_A = 0
    sets_B = 0
    num_set = 1
    while sets_A < 3 and sets_B < 3:
        es_quinto = (num_set == 5)
        ganador_set = simular_set(prob_A, prob_clave_A, es_quinto_set=es_quinto)
        if ganador_set == 'A':
            sets_A += 1
        else:
            sets_B += 1
        num_set += 1
    return 'A' if sets_A == 3 else 'B'


# -------------------------------------------------------------
# EJECUCIÓN Y GENERACIÓN DE MATRIZ DE SIMULACIÓN
# -------------------------------------------------------------
if __name__ == "__main__":
    # Rango de probabilidades de 40% a 60%
    probs_normal = np.linspace(0.40, 0.60, 11)
    probs_clave = np.linspace(0.40, 0.60, 11)
    simulaciones_por_celda = 500

    matriz_victorias = np.zeros((len(probs_clave), len(probs_normal)))

    print("Ejecutando matriz de simulación...")
    for i, p_c in enumerate(probs_clave):
        for j, p_n in enumerate(probs_normal):
            victorias = sum(1 for _ in range(simulaciones_por_celda) if simular_partido(p_n, p_c) == 'A')
            matriz_victorias[i, j] = (victorias / simulaciones_por_celda) * 100

    # 1. GENERACIÓN DEL MAPA DE CALOR
    plt.figure(figsize=(10, 8), dpi=120)
    sns.heatmap(
        matriz_victorias, 
        annot=True, 
        fmt=".0f", 
        cmap="YlGnBu", 
        xticklabels=[f"{p*100:.0f}%" for p in probs_normal],
        yticklabels=[f"{p*100:.0f}%" for p in probs_clave],
        cbar_kws={'label': '% de Partidos Ganados'}
    )

    plt.title('Mapa de Calor: % Victorias según Punto Normal vs Punto Clave', fontsize=12, fontweight='bold', pad=15)
    plt.xlabel('Probabilidad en Punto Normal (%)', fontsize=11, labelpad=10)
    plt.ylabel('Probabilidad en Punto Clave (%)', fontsize=11, labelpad=10)
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.savefig('matriz_victorias_tenis_puntos_claves.png')
    plt.show()