import functions as f
from tablero import imprimir_tablero
from os.path import isfile


def main():
    print('\n\n*** Menu de Inicio ***\n')
    file_name = input('Indique el nombre del archivo que desea abrir: ')
    if not isfile(file_name):
        print(f'File {file_name} not found. Exit')
        return
    tablero = f.cargar_tablero(file_name)
    menu_text = '\n*** Menu de Acciones ***\n\
        \n[1] Mostrar tablero\
        \n[2] Validar tablero\
        \n[3] Revisar solucion\
        \n[4] Solucionar tablero\
        \n[5] Salir del programa\
        \n\nIndique su opcion (1, 2, 3, 4 o 5): '
    opcion = input(menu_text)
    while opcion != '5':
        if opcion == '1':
            imprimir_tablero(tablero)
        elif opcion == '2':
            if f.verificar_tortugas(tablero) or f.verificar_valor_bombas(tablero):
                print('Tablero no valido')
            else:
                print('Tablero valido')
        elif opcion == '3':
            if f.validar_solucion(tablero):
                print('El tablero es una solucion valida')
            else:
                print('La solucion no es valida')
        elif opcion == '4':
            sol_file_name = file_name[:-4] + '_sol.txt'
            tablero_sol = f.solucionar_tablero(tablero)
            f.guardar_tablero(sol_file_name, tablero_sol)
            f.imprimir_tablero(tablero_sol)
        else:
            print('Escoga una opcion del menu')
        opcion = input(menu_text)


if __name__ == '__main__':
    main()
   
    