import random
import os
import time

# parámetros y posiciones
n = 7
gx, gy = 1, 6
rx, ry = 6, 6
qx, qy = 1, 0
gato = (gx, gy)
raton = (rx, ry)
queso = (qx, qy)

lista_movimientos = [(-1, 0), (1, 0), (0, 1), (0, -1)]

def mostrar_tablero(pos_gato, pos_raton, pos_queso):
    for fila in range(n):
        for columna in range(n):
            if (fila, columna) == pos_gato:
                x = "G"
            elif (fila, columna) == pos_raton:
                x = "R"
            elif (fila, columna) == pos_queso:
                x = "Q"
            else:
                x = "."
            print(x, end=" ")
        print()
    print()

def move(posicion):
    while True:
        y, x = posicion
        dy, dx = random.choice(lista_movimientos)
        ny, nx = y + dy, x + dx
        if 0 <= ny < n and 0 <= nx < n:
            return (ny, nx)

def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def evaluar(pos_gato, pos_raton, pos_queso):
    if pos_gato == pos_raton:
        return float("-inf")  # ratón pierde
    if pos_raton == pos_queso:
        return float("inf")   # ratón gana
    peso_queso = 50
    peso_peligro = 30
    valor_queso = peso_queso * (n - distancia(pos_raton, pos_queso))
    valor_seguridad = peso_peligro * distancia(pos_raton, pos_gato)
    return valor_queso + valor_seguridad

MOVIMIENTOS = [(1,0), (-1,0), (0,1), (0,-1)]

def movimientos_validos(pos):
    y, x = pos
    for dy, dx in MOVIMIENTOS:
        ny, nx = y + dy, x + dx
        if 0 <= ny < n and 0 <= nx < n:
            yield (ny, nx)

# minimax simple para el ratón
def minimax(pos_gato, pos_raton, pos_queso, profundidad, es_turno_raton):
    if profundidad == 0 or pos_gato == pos_raton or pos_raton == pos_queso:
        return evaluar(pos_gato, pos_raton, pos_queso)

    if es_turno_raton:
        max_valor = float("-inf")
        for nueva_pos in movimientos_validos(pos_raton):
            val = minimax(pos_gato, nueva_pos, pos_queso, profundidad-1, False)
            max_valor = max(max_valor, val)
        return max_valor
    else:
        # gato simplemente minimiza score del ratón (no crítico porque perseguirá directamente)
        min_valor = float("inf")
        for nueva_pos in movimientos_validos(pos_gato):
            val = minimax(nueva_pos, pos_raton, pos_queso, profundidad-1, True)
            min_valor = min(min_valor, val)
        return min_valor

def mejor_movimiento_raton(pos_gato, pos_raton, pos_queso, profundidad, prev_pos_raton=None):
    mejores = []
    mejor_valor = float("-inf")
    for nueva_pos in movimientos_validos(pos_raton):
        if prev_pos_raton is not None and nueva_pos == prev_pos_raton:
            continue
        valor = minimax(pos_gato, nueva_pos, pos_queso, profundidad-1, False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejores = [nueva_pos]
        elif valor == mejor_valor:
            mejores.append(nueva_pos)
    if not mejores:
        return move(pos_raton)
    mejores.sort(key=lambda p: distancia(p, pos_queso))
    choice_pool = mejores[:2] if len(mejores) >= 2 else mejores
    return random.choice(choice_pool)

# gato persigue al ratón directamente
def mejor_movimiento_gato(pos_gato, pos_raton):
    min_dist = float("inf")
    candidatos = []
    for nueva_pos in movimientos_validos(pos_gato):
        d = distancia(nueva_pos, pos_raton)
        if d < min_dist:
            min_dist = d
            candidatos = [nueva_pos]
        elif d == min_dist:
            candidatos.append(nueva_pos)
    return random.choice(candidatos) if candidatos else move(pos_gato)

# -------------------------
# BUCLE PRINCIPAL
# -------------------------
random.seed(0)
contador = 0
prev_raton = None
prev_gato = None
profundidad = 4
max_turnos = 25

print("Tablero inicial:")
mostrar_tablero(gato, raton, queso)
time.sleep(1)

while gato != raton and raton != queso and contador < max_turnos:
    # ratón inteligente
    nuevo_mov_r = mejor_movimiento_raton(gato, raton, queso, profundidad, prev_raton)
    prev_raton = raton
    raton = nuevo_mov_r

    # gato persigue al ratón
    nuevo_mov_g = mejor_movimiento_gato(gato, raton)
    prev_gato = gato
    gato = nuevo_mov_g

    os.system('cls' if os.name == 'nt' else 'clear')
    mostrar_tablero(gato, raton, queso)
    contador += 1
    print(f"Turno: {contador}")
    time.sleep(0.5)

# resultado final
os.system('cls' if os.name == 'nt' else 'clear')
mostrar_tablero(gato, raton, queso)
if gato == raton:
    print(f"El gato atrapó al ratón en {contador} movimientos.")
elif raton == queso:
    print(f"El ratón atrapó el queso en {contador} movimientos.")
else:
    print(f"El Ratñon escapo en: {contador} movimientos.")
