import random
import numpy as np
import matplotlib.pyplot as plt

PUNTOS_JUGADOS = 0
PUNTOS_GANADOS = 0

def simular_punto(p_ganar_punto_A):
    return 'A' if random.random() < p_ganar_punto_A else 'B'

def simular_punto_clave(p_ganar_punto_clave_A):
    return 'A' if random.random() < p_ganar_punto_clave_A else 'B'

def simular_juego_normal(p_ganar_punto_A, p_ganar_clave_A):
    global PUNTOS_JUGADOS, PUNTOS_GANADOS
    puntos_A = 0
    puntos_B = 0
    while True:
        if (puntos_A >= 3 and puntos_A - puntos_B > 0) or (puntos_B >= 3 and puntos_B - puntos_A > 0) :
            if simular_punto_clave(p_ganar_clave_A) == 'A':
                puntos_A += 1
                PUNTOS_GANADOS += 1
            else:
                puntos_B += 1

        elif simular_punto(p_ganar_punto_A) == 'A':
            puntos_A += 1            
            PUNTOS_GANADOS += 1
        else:
            puntos_B += 1
        PUNTOS_JUGADOS += 1        
            
        if puntos_A >= 4 and puntos_A - puntos_B >= 2:
            return 'A'
        elif puntos_B >= 4 and puntos_B - puntos_A >= 2:
            return 'B'

def simular_tiebreak(p_ganar_punto_A, p_ganar_clave_A, puntos_objetivo=7):
    global PUNTOS_JUGADOS, PUNTOS_GANADOS
    puntos_A = 0
    puntos_B = 0
    while True:
        if (puntos_A >= puntos_objetivo and puntos_A - puntos_B > 0) or (puntos_B >= puntos_objetivo and puntos_B - puntos_A > 0) :
            if simular_punto_clave(p_ganar_clave_A) == 'A':
                puntos_A += 1
                PUNTOS_GANADOS += 1
            else:
                puntos_B += 1

        elif simular_punto(p_ganar_punto_A) == 'A':
            puntos_A += 1
            PUNTOS_GANADOS += 1
        else:
            puntos_B += 1
        PUNTOS_JUGADOS += 1
            
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
# SIMULACIÓN MONTE CARLO Y GRAFICADO
# -------------------------------------------------------------
if __name__ == "__main__":
    # Rango de probabilidades de ganar un punto: de 40% a 60%
    probs_punto = 0.5
    probs_punto_clave = np.linspace(0.25, 0.75, 26)
    
    simulaciones_por_prob = 1500

    porcentajes_victoria = []
    pct_putnos_victoria_array = []

    print("Ejecutando simulación...")
    for p in probs_punto_clave:
        victorias = sum(1 for _ in range(simulaciones_por_prob) if simular_partido(probs_punto, p) == 'A')
        pct = (victorias / simulaciones_por_prob) * 100
        porcentajes_victoria.append(pct)
        # pyrefly: ignore [division-by-zero]
        pct_putnos_victoria_array.append(PUNTOS_GANADOS/PUNTOS_JUGADOS * 100)        
        # pyrefly: ignore [division-by-zero]
        print(f"Prob. punto: {PUNTOS_GANADOS/PUNTOS_JUGADOS*100:.1f}% -> % Victorias partido: {pct:.1f}%")
        PUNTOS_JUGADOS = 0
        PUNTOS_GANADOS = 0

    # Convertir la probabilidad de punto clave a porcentaje (0% - 100%)
    prob_clave_pct = probs_punto_clave * 100

    plt.figure(figsize=(10, 6), dpi=120)

    # Línea guía continua de fondo
    plt.plot(pct_putnos_victoria_array, porcentajes_victoria, color='gray', linestyle='-', alpha=0.4, linewidth=1.5, zorder=1)

    # Puntos coloreados según la probabilidad de ganar un punto clave
    scatter = plt.scatter(
        pct_putnos_victoria_array, 
        porcentajes_victoria, 
        c=prob_clave_pct,      # <--- Mapeo al % de punto clave
        cmap='rainbow', 
        s=60, 
        edgecolors='black', 
        linewidth=0.5,
        zorder=2
    )

    # Barra lateral indicando la probabilidad de punto clave
    cbar = plt.colorbar(scatter)
    cbar.set_label('Probabilidad de ganar un punto clave (%)', fontsize=10)

    # Líneas de referencia (50% punto / 50% partido)
    plt.axvline(x=50, color='gray', linestyle='--', alpha=0.7)
    plt.axhline(y=50, color='gray', linestyle='--', alpha=0.7)

    plt.title('Efecto Amplificador del Sistema de Puntuación en Tenis (Mejor de 5 Sets)', fontsize=12, fontweight='bold', pad=15)
    plt.xlabel('Probabilidad de ganar un punto real (%)', fontsize=11)
    plt.ylabel('Porcentaje de partidos ganados (%)', fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.xlim(40, 60)
    plt.ylim(-5, 105)

    # Mostrar gráfico
    plt.tight_layout()
    plt.savefig('simulacion_tenis_punto_clave_color.png')
    plt.show()