import os
import sys

# Detectar se está rodando como executável compilado
def get_resource_path(relative_path):
    """Retorna o caminho correto para recursos (funciona com PyInstaller)"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Se não for executável, usa o diretório do script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# constrantes para fonte
FONT_PATH = get_resource_path("fonts/PressStart2P.ttf")
FONT_PIXEL_BIG_SIZE = 32
FONT_PIXEL_SIZE = 13

# caminho do arquivo json com as palavras
PATH_PALAVRAS_JSON = get_resource_path("data/palavras.json")

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