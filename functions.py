from tablero import imprimir_tablero
from copy import deepcopy


def is_bomb(obj: str | int) -> bool:
    '''Revisa si el objeto es una bomba o no'''
    return isinstance(obj, int) or obj.isnumeric()


def cargar_tablero(nombre_archivo: str) -> list[list[str]]:
    '''Recibe un archivo y transforma los datos en una 
    lista de listas'''
    with open(nombre_archivo) as file:
        size, *data = file.readline().split(',')
    size = int(size)

    _tablero = [['' for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            _tablero[i][j] = data[size*i+j]
    return _tablero


def guardar_tablero(nombre_archivo: str, _tablero: list) -> None:
    '''Guarda un tablero en el archivo'''
    if _tablero == None:
        return
    size = len(_tablero)
    data = str(size)
    for i in range(size):
        for j in range(size):
            data += ',' + _tablero[i][j]
    with open(nombre_archivo, 'w') as file:
        file.write(data)
        

def verificar_valor_bombas(_tablero: list[list[str]]) -> int:
    '''Devuelve la cantidad de bombas cuyo valor este fuera del
    rango [2, 2 * size - 1]'''
    counter = 0
    size = len(_tablero)
    for fila in _tablero:
        for obj in fila:
            if is_bomb(obj):
                if not (2 <= int(obj) <= 2*size - 1):
                    counter += 1
    return counter


def transponer_matriz(_tablero: list[list[str]]) -> list[list[str]]:
    '''Devuelva la transpuesta de una matriz'''
    size = len(_tablero)
    return [[_tablero[col][row] for col in range(size)] for row in range(size)]


def alcance_bomba_linea(_tablero: list[list[str]], coordenada: tuple[int, int]) -> int:
    '''Devuelve la cantidad de celdas de la misma fila que alcanca la bomba
    en la coordenada, en el tablero dado'''
    row, col = coordenada
    size = len(_tablero)
    counter = 0
    for i in range(size):
        counter += _tablero[row][i] != 'T'
        if _tablero[row][i] == 'T':
            if i < col:
                counter = 0
            else:
                break
    return counter


def verificar_alcance_bomba(_tablero: list[list[str]], coordenada: tuple[int, int]) -> int:
    '''Devuelve la cantidad de celdas que alcanca la bomba en la coordenada, en el tablero'''
    if not is_bomb(_tablero[coordenada[0]][coordenada[1]]):
        return 0
    counter_fila = alcance_bomba_linea(_tablero, coordenada) # cantidad de celdas en la fila
    tablero_transpuesto = transponer_matriz(_tablero) # obtiene la transpuesta del _tablero
    counter_col = alcance_bomba_linea(tablero_transpuesto, coordenada[::-1]) # cantidad de celdas en la columna
    return counter_fila + counter_col - 1 # cantidad de celdas totales


def get(_tablero: list[list[str]], coordenada: tuple[int, int]) -> str | None:
    '''Retorna el elemento del _tablero en la coordenada.
    Si la coordenada excede las dimensiones de la tabla, devuelve None'''
    size = len(_tablero)
    row, col = coordenada
    if 0 <= row < size and 0 <= col < size:
        return _tablero[row][col]
    return None


def check_surround(_tablero: list[list[str]], coordenada: tuple[int, int]) -> bool:
    '''Revisa si hay alguna tortuga en las celdas contiguas'''
    row, col = coordenada
    surround = (
        get(_tablero, (row-1, col)),
        get(_tablero, (row+1, col)),
        get(_tablero, (row, col-1)),
        get(_tablero, (row, col+1)),
    )
    return 'T' in surround


def verificar_tortugas(_tablero: list) -> int:
    '''Cuenta la cantidad de tortugas que tengan otra tortuga vecina'''
    counter = 0
    size = len(_tablero)
    for i in range(size):
        for j in range(i % 2, size, 2):
            if _tablero[i][j] == 'T':
                counter += check_surround(_tablero, (i, j))
    return counter


def verificar_posicion_tortuga(_tablero: list[list[str]], coordenadas: tuple[int, int]) -> bool:
    '''Revisa si es posible poner una tortuga en esa posicion'''
    row, col = coordenadas
    size = len(_tablero)
    if not ((0 <= row <= size) and (0 <= col <= size)):
        return False
    a = _tablero[row][col]
    return _tablero[row][col] == '-' and not check_surround(_tablero, coordenadas)


def next_coord(size: int, coord: tuple[int, int]) -> tuple[int, int]:
    '''Devuelve la coordenada de la celda siguiente (avanzando a la derecha en una
    misma fila)'''
    row = coord[0] + (coord[1] == size - 1)
    if row == size:
        return False
    return row, (coord[1] + 1) % size


def put_turtle(_tablero: list[list[str]], coordenada: tuple[int, int]) -> None:
    '''Inserta una tortuga en la coordenada'''
    _tablero[coordenada[0]][coordenada[1]] = 'T'


def validar_solucion(_tablero: list[list[str]]) -> bool:
    '''Revisa si un _tablero es solucion valida o no'''
    if verificar_valor_bombas(_tablero) or verificar_tortugas(_tablero):
        return False
    size = len(_tablero)
    for i in range(size):
        for j in range(size):
            alcance_bomba = verificar_alcance_bomba(_tablero, (i, j))
            if alcance_bomba != 0 and str(alcance_bomba) != str(_tablero[i][j]):
                return False
    return True


def copy_reference(tablero_copy: list[list[str]], tablero_a_copiar: list[list[str]]) -> None:
    for i, fila in enumerate(tablero_a_copiar):
        tablero_copy[i] = fila


def solucionar(_tablero: list[list[str]], coordenada: tuple[int, int]) -> list[list[str]] | None:
    if validar_solucion(_tablero): # si es solucion estamos listos
        return _tablero
    
    size = len(_tablero)
    
    while coordenada and not verificar_posicion_tortuga(_tablero, coordenada):
        # mientras la coordenada este dentro del _tablero y no se pueda poner una tortuga ahi, va a la siguiente coordenada
        coordenada = next_coord(size, coordenada)

    if not coordenada:
        return None
    
    new_tablero = deepcopy(_tablero)
    put_turtle(new_tablero, coordenada)

    if solucionar(new_tablero, coordenada):
        copy_reference(_tablero, new_tablero)
        return _tablero
    
    coordenada = next_coord(size, coordenada)
    return solucionar(_tablero, coordenada)


def alone(tablero: list[list[str]], coordenada: tuple[int, int]):
    row, col = coordenada
    size = len(tablero)
    for i in range(size):
        if is_bomb(tablero[row][i]) or is_bomb(tablero[i][col]):
            return False
    return True


def remove_unnecesary_turtles(tablero: list[list[str]]):
    for i, fila in enumerate(tablero):
        for j, obj in enumerate(fila):
            if obj == 'T':
                if alone(tablero, (i, j)):
                    tablero[i][j] = '-'
    return tablero


def solucionar_tablero(_tablero: list[list[str]]) -> list[list[str]]:
    solucion = solucionar(deepcopy(_tablero), (0, 0))
    solucion_simple = remove_unnecesary_turtles(solucion)
    return solucion_simple


def main():
    file = 'Archivos/4x4.txt'
    # file_solucion = file[:-4] + '_sol.txt'

    tablero = cargar_tablero(file)
    # _tablero_solucion = cargar_tablero(file_solucion)

    imprimir_tablero(tablero)

    _tablero = solucionar_tablero(tablero)

    imprimir_tablero(_tablero)
    # imprimir_tablero(tablero_solucion)


if __name__ == '__main__':
    main()