# constrantes para fonte
FONT_PATH = "fonts/PressStart2P.ttf"
FONT_PIXEL_BIG_SIZE = 32
FONT_PIXEL_SIZE = 13

# caminho do arquivo json com as palavras
PATH_PALAVRAS_JSON = "data/palavras.json"

# tamanhos do tabuleiro conforme dificuldade
EASY_SIZE = 10
MEDIUM_SIZE = 15
HARD_SIZE = 20

log_counter = 0
#log de mensagens
def log(archive="desconhecido", msg="sem mensagem de log"):
    global log_counter
    log_counter += 1
    print(f"LOG[{log_counter}][{archive}]: {msg}")