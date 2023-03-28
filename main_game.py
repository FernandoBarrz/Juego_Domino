from random import shuffle
from itertools import combinations_with_replacement, chain
from collections import Counter
from funciones_utils import set_turno

dominos = list(combinations_with_replacement(range(0, 7), 2)) # Define la lista de dominos
dominos = [list(x) for x in dominos] # Convierte lista de tuples a lista de listas
shuffle(dominos) # Mezcla las fichas
coeficiente = len(dominos) // 2 # Definir coeficiente igual a la mitad del número de fichas de dominó
piezas_en_stock = dominos[:coeficiente] # Tomar la primera mitad de los dominos
piezas_computadora = dominos[coeficiente:int(coeficiente * 1.5)] # Tomar las piezas de la computadora y el jugador
piezas_jugador = dominos[int(coeficiente * 1.5):]

snake = [max([[x, y] for x, y in piezas_computadora + piezas_jugador if x == y])] # Algoritmo encontrar la "serpiente" (patron que siguen las fichas)

numero_turno = 0 if len(piezas_jugador) > len(piezas_computadora) else 1

def set_turno_func(entrada_func, piezas_func):
    if int(entrada_func) == 0 and len(piezas_en_stock) == 0: # Si no hay piezas, Se detiene 
        return None
    elif int(entrada_func) == 0 and len(piezas_en_stock) > 0: # Da piezas al jugador
        piezas_func.append(piezas_en_stock[-1])
        piezas_en_stock.remove(piezas_en_stock[-1])
        return None
    if int(entrada_func) > 0: # Coloca la pieza despues de la última ficha
        piece_to_end = piezas_func[int(entrada_func) - 1] # Tomar pieza del jugador o de la computadora.
        if piece_to_end[1] == snake[-1][-1]: # Invertir pieza
            piece_to_end.reverse()
        snake.append(piece_to_end) # Colocar pieza
        piezas_func.remove(piezas_func[int(entrada_func) - 1]) # Eliminar pieza del jugador o computadora
    else: # Colocar pieza a la izquierda
        piece_to_start = piezas_func[-int(entrada_func) - 1] # Tomar pieza del jugador o de la computadora.
        if piece_to_start[0] == snake[0][0]: # Invertir pieza
            piece_to_start.reverse()
        snake.insert(0, piece_to_start) # Colocar pieza
        piezas_func.remove(piezas_func[-int(entrada_func) - 1]) # Eliminar pieza del jugador o de la computadora

while True: # Empezar el juego
    print("*"*50)
    print("\n\n\tBienvenido al juego de Domino!!! \n\n")
    print("*"*50)
    print("\n")
    i = input("Ver reglas del juego?: (s/n)\n")
    if i == 's' or i == 'S':
        print('1. El juego se puede jugar con dos a cuatro jugadores.')
        print('2. Las fichas se barajan boca abajo y se reparten siete fichas a cada jugador.')
        print('3. El jugador con la ficha más alta comienza el juego, colocando la ficha en la mesa.')
        print('4. Los jugadores toman turnos para colocar una ficha en la mesa, siempre conectando los puntos de una ficha a los puntos de otra ficha que ya esté en la mesa. Si un jugador no puede jugar una ficha, debe pasar el turno.')
        print('5. El juego continúa hasta que un jugador se queda sin fichas o hasta que nadie puede jugar más fichas.')
        print('6. El jugador que primero se queda sin fichas gana la ronda.')
        print('7. El juego se puede jugar por varias rondas, y el jugador con más rondas ganadas al final del juego es el ganador.')
        break
    elif i == 'n' or i == 'N':
        break
    else:
        print("!"*50)
        print("\n\tElección no valida.\n")
        print("!"*50)
        continue

while True:
    print('=' * 70) # Mostrar el total de fichas, fichas del jugador y de la computadora.
    print('Piezas (almacen):', len(piezas_en_stock))
    print('Piezas de la computadora:', len(piezas_computadora), '\n')
    print(*snake, '\n', sep='') if len(snake) <= 6 else print(*snake[:3], '...', *snake[-3:], '\n', sep='')
    print("Tus piezas:")
    for num, piece in enumerate(piezas_jugador):
        print(f"{num + 1}: {piece}")

    if len(piezas_jugador) == 0 or set_turno.patron_win(snake) and numero_turno == 0: # Condición para que el jugador gane
        print("\n\nEstatus: El juego terminó. Tu ganaste!!!\n\n")
        break

    if len(piezas_computadora) == 0 or set_turno.patron_win(snake) and numero_turno == 1: # Condición para que la computadora gane.
        print("\nEstatus: El juego terminó. La computadora ganó!!!")
        break
    
    llaves_conexion = [snake[0][0], snake[-1][-1]] # Se forman los pares de llaves. EJ: [6:4][4:1]
    
    if len(piezas_en_stock) == 0 and \
            not any(item in llaves_conexion for item in list(chain(*(piezas_jugador + piezas_computadora)))): # Condición para empate
        print("\nEstatus: El juego terminó. Es un empate!!!")
        break
    
    if numero_turno % 2 == 0: # Turno del jugador
        numero_turno += 1 
        print("\nEstatus: Es tu turno de mover. Ingresa tu opción.")
        input_usuario = input()
        if input_usuario.lstrip("-").isdigit() and int(input_usuario) in range(-len(piezas_jugador), len(piezas_jugador) + 1): # Revisa que el input sea valido
            if int(input_usuario) == 0: # Dar pieza al jugador
                set_turno_func(input_usuario, piezas_jugador)
                continue
        
            pieza_actual = piezas_jugador[int(input_usuario) - 1] if int(input_usuario) > 0 \
                else piezas_jugador[-int(input_usuario) - 1] # Define al jugador actual
            
            if llaves_conexion[-1] in pieza_actual and int(input_usuario) > 0 or \
                    llaves_conexion[0] in pieza_actual and int(input_usuario) < 0: # Revisar si la pieza es valida
                set_turno_func(input_usuario, piezas_jugador)
            else:
                print("!"*50)
                print("\n\tMovimiento ilegal. Ingresa otra opción.\n")
                print("!"*50)
                numero_turno -= 1
                continue
        else:
            print("Opción invalida. Ingresa otra opción.")
            numero_turno -= 1
            continue
    else: # Turno de la computadora
        numero_turno += 1
        print("\nEstatus: La computadora va a realizar un movimiento. Presiona Enter para continuar...\n")
        input()
        count_nums = Counter(chain(*(piezas_computadora + snake)))
        puntajes = list() # Define los puntajes para cada pieza
        for piece in piezas_computadora: # iterar a través de todas las piezas para obtener puntaje
            puntaje = count_nums[piece[0]] + count_nums[piece[1]]
            puntajes.append(puntaje)
        
        piezas_computadora = [x for _, x in sorted(zip(puntajes, piezas_computadora), reverse=True)] # Ordenar piezas por puntaje
        
        for piece in piezas_computadora: # Hacer el movimiento de la computadora
            if llaves_conexion[-1] in piece: # Revisar como conectar las fichas
                set_turno_func(str(piezas_computadora.index(piece) + 1), piezas_computadora)
                break
            elif llaves_conexion[0] in piece:
                set_turno_func(str(-piezas_computadora.index(piece) - 1), piezas_computadora)
                break
        else: # Dar pieza a la computadora
            set_turno_func('0', piezas_computadora)

