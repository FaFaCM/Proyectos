import os
os.system("")

RESET = "\033[0m"
FONDO_CLARO = "\033[48;5;230m"
FONDO_OSCURO = "\033[48;5;94m"
COLOR_CLARAS = "\033[1;97m"
COLOR_OSCURAS = "\033[38;5;16m"

tablero = [['.' for _ in range(8)] for _ in range(8)]

def inicializar_tablero():
    for fila in range(8):
        for col in range(8):
            tablero[fila][col] = '.'
            if (fila + col) % 2 == 1:
                if fila < 3:
                    tablero[fila][col] = 'c'
                elif fila > 4:
                    tablero[fila][col] = 'o'

def imprimir_tablero():
    print("\n    1  2  3  4  5  6  7  8")
    for fila in range(8):
        print(chr(ord('a') + fila), " ", end="")
        for col in range(8):
            fondo = FONDO_OSCURO if (fila + col) % 2 == 1 else FONDO_CLARO
            pieza = tablero[fila][col]
            simbolo = " "
            color = ""
            if pieza != '.':
                if color_de(pieza) == 'c':
                    simbolo = "D" if es_dama(pieza) else "○"
                else:
                    simbolo = "D" if es_dama(pieza) else "●"
                color = COLOR_CLARAS if color_de(pieza) == 'c' else COLOR_OSCURAS
            print(fondo + color + " " + simbolo + " " + RESET, end="")
        print()

def dentro_del_tablero(fila, col):
    return 0 <= fila < 8 and 0 <= col < 8

def color_de(pieza):
    if pieza == 'c' or pieza == 'C':
        return 'c'
    return 'o'

def es_dama(pieza):
    return pieza == 'C' or pieza == 'O'

def nombre_casilla(fila, col):
    return chr(ord('a') + fila) + str(col + 1)

def etiqueta_de_jugador(jugador):
    if jugador == 'c':
        return FONDO_OSCURO + COLOR_CLARAS + " ● CLARAS " + RESET
    return FONDO_OSCURO + COLOR_OSCURAS + " ● OSCURAS " + RESET

def fichas_de(jugador):
    lista = []
    for fila in range(8):
        for col in range(8):
            if tablero[fila][col] != '.' and color_de(tablero[fila][col]) == jugador:
                lista.append((fila, col))
    return lista

def opciones_de_direccion(pieza):
    if es_dama(pieza):
        return [("Izquierda arriba", -1, -1), ("Derecha arriba", -1, 1),
                ("Izquierda abajo", 1, -1), ("Derecha abajo", 1, 1)]
    adelante = 1 if color_de(pieza) == 'c' else -1
    return [("Izquierda", adelante, -1), ("Derecha", adelante, 1)]

def destino_de(fila, col, delta_fila, delta_col):
    f1 = fila + delta_fila
    c1 = col + delta_col
    if not dentro_del_tablero(f1, c1):
        return None
    if tablero[f1][c1] == '.':
        return f1, c1

    f2 = fila + 2 * delta_fila
    c2 = col + 2 * delta_col
    es_enemigo = color_de(tablero[f1][c1]) != color_de(tablero[fila][col])
    if es_enemigo and dentro_del_tablero(f2, c2) and tablero[f2][c2] == '.':
        return f2, c2
    return None

def movimientos_desde(fila, col):
    lista = []
    for texto, delta_fila, delta_col in opciones_de_direccion(tablero[fila][col]):
        destino = destino_de(fila, col, delta_fila, delta_col)
        if destino is not None:
            lista.append(destino)
    return lista

def puede_capturar_desde(fila, col):
    for fd, cd in movimientos_desde(fila, col):
        if abs(fd - fila) == 2:
            return True
    return False

def fichas_que_pueden_comer(jugador):
    lista = []
    for fila, col in fichas_de(jugador):
        if puede_capturar_desde(fila, col):
            lista.append(nombre_casilla(fila, col))
    return lista

def jugador_puede_mover(jugador):
    for fila, col in fichas_de(jugador):
        if len(movimientos_desde(fila, col)) > 0:
            return True
    return False

def coronar(fila, col):
    if tablero[fila][col] == 'c' and fila == 7:
        tablero[fila][col] = 'C'
    if tablero[fila][col] == 'o' and fila == 0:
        tablero[fila][col] = 'O'

def mover_ficha(fo, co, fd, cd):
    tablero[fd][cd] = tablero[fo][co]
    tablero[fo][co] = '.'
    if abs(fd - fo) == 2:
        tablero[(fo + fd) // 2][(co + cd) // 2] = '.'
    coronar(fd, cd)

def leer_casilla(texto):
    texto = texto.replace(" ", "").lower()
    if len(texto) != 2 or texto[0] not in "abcdefgh" or texto[1] not in "12345678":
        return None
    return ord(texto[0]) - ord('a'), int(texto[1]) - 1

def pedir_direccion(pieza, se_puede_cancelar):
    opciones = opciones_de_direccion(pieza)

    print("¿Hacia dónde quieres moverla?")
    for i in range(len(opciones)):
        print(f"  {i + 1}) {opciones[i][0]}")
    if se_puede_cancelar:
        print("  0) Cancelar")

    while True:
        respuesta = input("Elige una opción: ").strip()
        if respuesta == "0" and se_puede_cancelar:
            return None
        if respuesta.isdigit() and 1 <= int(respuesta) <= len(opciones):
            texto, delta_fila, delta_col = opciones[int(respuesta) - 1]
            return delta_fila, delta_col
        print("Opción no válida, escribe uno de los números del menú.")

def continuar_comiendo(fila, col):
    while puede_capturar_desde(fila, col):
        imprimir_tablero()
        print(f"\n¡Sigue comiendo con la ficha en {nombre_casilla(fila, col)}!")
        delta_fila, delta_col = pedir_direccion(tablero[fila][col], False)
        destino = destino_de(fila, col, delta_fila, delta_col)

        if destino is None or abs(destino[0] - fila) != 2:
            print("Tienes que comer con esa ficha, elige otra dirección.")
            continue

        mover_ficha(fila, col, destino[0], destino[1])
        fila, col = destino

def jugar():
    inicializar_tablero()
    turno = 'c'

    while True:
        imprimir_tablero()

        if not jugador_puede_mover(turno):
            print("\n¡Fin del juego! Ganan las fichas", "OSCURAS" if turno == 'c' else "CLARAS")
            break

        print("\nTurno de:", etiqueta_de_jugador(turno))
        obligadas = fichas_que_pueden_comer(turno)
        if obligadas:
            print("¡Tienes que comer! Fichas que pueden comer:", ", ".join(obligadas))

        texto = input("Elige la ficha que quieres mover (ejemplo: c2) o escribe 'salir': ")
        if texto.strip().lower() == "salir":
            print("Juego terminado por acuerdo entre los jugadores. ¡Empate!")
            break

        casilla = leer_casilla(texto)
        if casilla is None:
            print("Casilla no válida. Escribe una letra (a-h) y un número (1-8), por ejemplo: c2")
            continue

        fo, co = casilla
        pieza = tablero[fo][co]
        if pieza == '.' or color_de(pieza) != turno:
            print("Ahí no hay una ficha tuya.")
            continue

        direccion = pedir_direccion(pieza, True)
        if direccion is None:
            print("Acción cancelada. Elige otra ficha.")
            continue

        delta_fila, delta_col = direccion
        destino = destino_de(fo, co, delta_fila, delta_col)
        if destino is None or (obligadas and abs(destino[0] - fo) == 1):
            print("Ese movimiento no es posible, intenta de nuevo.")
            continue

        fd, cd = destino
        mover_ficha(fo, co, fd, cd)
        if abs(fd - fo) == 2:
            continuar_comiendo(fd, cd)

        turno = 'o' if turno == 'c' else 'c'

if __name__ == "__main__":
    jugar()