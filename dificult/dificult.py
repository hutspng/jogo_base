from consts import EASY_SIZE, MEDIUM_SIZE, HARD_SIZE


matriz_size = 0


def bnt_dificult_escolhida(dificuldade):
    """Retorna o tamanho da matriz correspondente à dificuldade escolhida.

    Não faz logging ou manipula janelas — isso deve ficar na camada de lógica (main).
    """
    global matriz_size
    if dificuldade == 1:
        matriz_size = EASY_SIZE
    elif dificuldade == 2:
        matriz_size = MEDIUM_SIZE
    elif dificuldade == 3:
        matriz_size = HARD_SIZE
    else:
        matriz_size = MEDIUM_SIZE

    return matriz_size
    
