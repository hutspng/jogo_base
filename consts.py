"""
CONSTS.PY - Arquivo de constantes globais do jogo Caça Palavras
====================================================================
Este módulo centraliza todas as configurações e constantes utilizadas em todo o projeto.
Responsável por:
- Definir caminhos de recursos (fontes, dados)
- Configurar tamanhos de fonte
- Definir dificuldades do jogo
- Fornecer função de logging
- Compatibilidade com executáveis compilados (PyInstaller)
"""

import os
import sys

# ============================================================================
# GERENCIAMENTO DE RECURSOS PARA EXECUTÁVEIS COMPILADOS
# ============================================================================
def get_resource_path(relative_path):
    """
    Função para localização de recursos que funciona tanto no desenvolvimento quanto em executáveis compilados.
    
    Args:
        relative_path (str): Caminho relativo do recurso (ex: "fonts/font.ttf")
    
    Returns:
        str: Caminho absoluto correto para o recurso
        
    Funcionamento:
    - Em desenvolvimento: usa o diretório do script atual
    - Em executável compilado: usa a pasta temporária do PyInstaller (sys._MEIPASS)
    """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        # quando o programa roda como executável compilado
        base_path = sys._MEIPASS
    except AttributeError:
        # Se não for executável compilado, usa o diretório do script atual
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# ============================================================================
# CONFIGURAÇÕES DE FONTE
# ============================================================================
# Caminho para a fonte pixelizada "Press Start 2P" - estilo retrô de videogame
FONT_PATH = get_resource_path("fonts/PressStart2P.ttf")
FONT_PIXEL_BIG_SIZE = 32  # Tamanho grande para títulos principais
FONT_PIXEL_SIZE = 13      # Tamanho padrão para textos e botões

# ============================================================================
# ARQUIVOS DE DADOS
# ============================================================================
# Caminho para o arquivo JSON que contém todas as palavras e dicas do jogo
PATH_PALAVRAS_JSON = get_resource_path("data/palavras.json")

# ============================================================================
# CONFIGURAÇÕES DE DIFICULDADE
# ============================================================================
# Define os tamanhos das matrizes para cada nível de dificuldade
EASY_SIZE = 10    # Matriz 10x10 - nível fácil (100 células)
MEDIUM_SIZE = 15  # Matriz 15x15 - nível médio (225 células)
HARD_SIZE = 20    # Matriz 20x20 - nível difícil (400 células)

# ============================================================================
# SISTEMA DE LOGGING
# ============================================================================
log_counter = 0  # Contador global para numerar logs sequencialmente

def log(archive="desconhecido", msg="sem mensagem de log"):
    """
    Sistema simples de logging para debug e acompanhamento do fluxo do programa.
    
    Args:
        archive (str): Nome do arquivo/módulo que está fazendo o log
        msg (str): Mensagem a ser logada
        
    Imprime no formato: LOG[número][arquivo]: mensagem
    Útil para rastrear execução durante desenvolvimento e debug
    """
    global log_counter
    log_counter += 1
    print(f"LOG[{log_counter}][{archive}]: {msg}")