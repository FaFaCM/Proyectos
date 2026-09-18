tablero = [['.' for _ in range(8)] for _ in range(8)]

def inicializar_tablero():
    for fila in range(8):
        for col in range(8):
            tablero[fila][col] = '.'

    for fila in range(3):
        for col in range(8):
            if (fila + col) % 2 == 1:
                tablero[fila][col] = 'c'

    for fila in range(5, 8):
        for col in range(8):
            if (fila + col) % 2 == 1:
                tablero[fila][col] = 'o'

def imprimir_tablero():
    print()
    print("   0 1 2 3 4 5 6 7")
    for fila in range(8):
        print(fila, " ", end="")
        for col in range(8):
            print(tablero[fila][col], end=" ")
        print()

def dentro_del_tablero(fila, col):
    return 0 <= fila < 8 and 0 <= col < 8

def color_de(pieza):
    if pieza == 'c' or pieza == 'C':
        return 'c'
    return 'o'

def es_dama(pieza):
    return pieza == 'C' or pieza == 'O'

def contar_fichas(jugador):
    total = 0
    for fila in range(8):
        for col in range(8):
            pieza = tablero[fila][col]
            if pieza != '.' and color_de(pieza) == jugador:
                total += 1
    return total

def movimiento_valido(fo, co, fd, cd, turno, captura_obligatoria):
    if not dentro_del_tablero(fo, co) or not dentro_del_tablero(fd, cd):
        return False

    pieza = tablero[fo][co]
    if pieza == '.':
        return False
    if color_de(pieza) != turno:
        return False
    if tablero[fd][cd] != '.':
        return False

    diferencia_fila = fd - fo
    diferencia_col = cd - co

    if abs(diferencia_fila) != abs(diferencia_col):
        return False

    distancia = abs(diferencia_fila)
    if distancia != 1 and distancia != 2:
        return False

    if not es_dama(pieza):
        direccion_permitida = 1 if turno == 'c' else -1
        paso_fila = diferencia_fila // distancia
        if paso_fila != direccion_permitida:
            return False

    if distancia == 1:
        return not captura_obligatoria

    fila_media = (fo + fd) // 2
    col_media = (co + cd) // 2
    pieza_media = tablero[fila_media][col_media]

    if pieza_media == '.':
        return False
    if color_de(pieza_media) == turno:
        return False

    return True


def mover_ficha(fo, co, fd, cd):
    pieza = tablero[fo][co]
    tablero[fd][cd] = pieza
    tablero[fo][co] = '.'

    if abs(fd - fo) == 2:
        fila_media = (fo + fd) // 2
        col_media = (co + cd) // 2
        tablero[fila_media][col_media] = '.'
        return True

    return False

def coronar_si_corresponde(fila, col):
    pieza = tablero[fila][col]
    if pieza == 'c' and fila == 7:
        tablero[fila][col] = 'C'
    if pieza == 'o' and fila == 0:
        tablero[fila][col] = 'O'


def puede_capturar_desde(fila, col):
    pieza = tablero[fila][col]
    if pieza == '.':
        return False

    color = color_de(pieza)
    dama = es_dama(pieza)

    for delta_fila in (-1, 1):
        if not dama:
            direccion_permitida = 1 if color == 'c' else -1
            if delta_fila != direccion_permitida:
                continue

        for delta_col in (-1, 1):
            fila_media = fila + delta_fila
            col_media = col + delta_col
            fila_destino = fila + 2 * delta_fila
            col_destino = col + 2 * delta_col

            if not dentro_del_tablero(fila_destino, col_destino):
                continue
            if tablero[fila_destino][col_destino] != '.':
                continue

            enemigo = tablero[fila_media][col_media]
            if enemigo == '.' or color_de(enemigo) == color:
                continue

            return True

    return False

def puede_moverse_normal_desde(fila, col):
    pieza = tablero[fila][col]
    if pieza == '.':
        return False

    color = color_de(pieza)
    dama = es_dama(pieza)

    for delta_fila in (-1, 1):
        if not dama:
            direccion_permitida = 1 if color == 'c' else -1
            if delta_fila != direccion_permitida:
                continue

        for delta_col in (-1, 1):
            fila_destino = fila + delta_fila
            col_destino = col + delta_col
            if dentro_del_tablero(fila_destino, col_destino) and \
               tablero[fila_destino][col_destino] == '.':
                return True

    return False

def jugador_tiene_captura_obligatoria(jugador):
    for fila in range(8):
        for col in range(8):
            pieza = tablero[fila][col]
            if pieza != '.' and color_de(pieza) == jugador:
                if puede_capturar_desde(fila, col):
                    return True
    return False

def jugador_puede_mover(jugador):
    for fila in range(8):
        for col in range(8):
            pieza = tablero[fila][col]
            if pieza != '.' and color_de(pieza) == jugador:
                if puede_capturar_desde(fila, col) or puede_moverse_normal_desde(fila, col):
                    return True
    return False

def leer_movimiento(texto):
    partes = texto.split()
    if len(partes) != 4:
        return None
    try:
        return [int(p) for p in partes]
    except ValueError:
        return None

def leer_destino(texto):
    partes = texto.split()
    if len(partes) != 2:
        return None
    try:
        return [int(p) for p in partes]
    except ValueError:
        return None

def continuar_comiendo(fila, col, turno):
    while puede_capturar_desde(fila, col):
        imprimir_tablero()
        texto = input(f"Sigue comiendo con la ficha en ({fila},{col}) -> destino (fd cd): ")
        datos = leer_destino(texto)
        if datos is None:
            print("Entrada inválida, intenta de nuevo.")
            continue

        fd, cd = datos
        if not movimiento_valido(fila, col, fd, cd, turno, True):
            print("Movimiento inválido, intenta de nuevo.")
            continue

        mover_ficha(fila, col, fd, cd)
        coronar_si_corresponde(fd, cd)
        fila, col = fd, cd

def jugar():
    inicializar_tablero()
    turno = 'c'

    while True:
        imprimir_tablero()

        if contar_fichas(turno) == 0 or not jugador_puede_mover(turno):
            ganador = "OSCURAS" if turno == 'c' else "CLARAS"
            print(f"\n¡Fin del juego! Ganan las fichas {ganador}")
            break

        print(f"\nTurno: {'CLARAS (c/C)' if turno == 'c' else 'OSCURAS (o/O)'}")

        captura_obligatoria = jugador_tiene_captura_obligatoria(turno)
        if captura_obligatoria:
            print("¡Tienes que comer! Debes hacer un movimiento de captura.")

        texto = input("Movimiento (filaOrigen colOrigen filaDestino colDestino) o 'salir': ")

        if texto.strip().lower() == "salir":
            print("Juego terminado por acuerdo entre los jugadores. ¡Empate!")
            break

        datos = leer_movimiento(texto)
        if datos is None:
            print("Entrada inválida. Usa el formato: filaOrigen colOrigen filaDestino colDestino")
            continue

        fo, co, fd, cd = datos

        if not movimiento_valido(fo, co, fd, cd, turno, captura_obligatoria):
            print("Movimiento inválido, intenta de nuevo.")
            continue

        fue_captura = mover_ficha(fo, co, fd, cd)
        coronar_si_corresponde(fd, cd)

        if fue_captura and puede_capturar_desde(fd, cd):
            print("¡Puedes seguir comiendo con la misma ficha!")
            continuar_comiendo(fd, cd, turno)

        turno = 'o' if turno == 'c' else 'c'

if __name__ == "__main__":
    jugar()