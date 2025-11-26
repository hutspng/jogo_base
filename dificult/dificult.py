"""
DIFICULT/DIFICULT.PY - Lógica de Seleção de Dificuldade
=======================================================
Este módulo contém a lógica para conversão de níveis de dificuldade em tamanhos de matriz.
Responsável por:
- Mapear códigos de dificuldade (1, 2, 3) para tamanhos de matriz
- Fornecer tamanho padrão para códigos inválidos
- Manter estado da dificuldade selecionada (opcional, para referência futura)

Mapeamento de dificuldades:
- Código 1 (Fácil): Matriz 10x10 (100 células)
- Código 2 (Médio): Matriz 15x15 (225 células)  
- Código 3 (Difícil): Matriz 20x20 (400 células)
"""

from consts import EASY_SIZE, MEDIUM_SIZE, HARD_SIZE

# Variável global para manter referência do último tamanho selecionado
# (usado principalmente para debugging/logging)
matriz_size = 0

def bnt_dificult_escolhida(dificuldade):
    """
    Converte código de dificuldade em tamanho de matriz para o jogo.
    
    Esta função mapeia os níveis de dificuldade selecionados pelo usuário
    nos tamanhos apropriados de matriz que serão usados na geração do 
    caça-palavras.
    
    Args:
        dificuldade (int): Código da dificuldade selecionada
                          1 = Fácil, 2 = Médio, 3 = Difícil
                          
    Returns:
        int: Tamanho da matriz (N para uma matriz NxN)
        
    Comportamento:
    - Dificuldade 1: Retorna EASY_SIZE (10) para matriz 10x10
    - Dificuldade 2: Retorna MEDIUM_SIZE (15) para matriz 15x15  
    - Dificuldade 3: Retorna HARD_SIZE (20) para matriz 20x20
    - Outros valores: Retorna MEDIUM_SIZE como padrão seguro
    
    Efeitos colaterais:
    - Atualiza variável global matriz_size para referência futura
    """
    global matriz_size
    
    # Mapear código de dificuldade para tamanho de matriz
    if dificuldade == 1:
        matriz_size = EASY_SIZE      # 10x10 - 100 células
    elif dificuldade == 2:
        matriz_size = MEDIUM_SIZE    # 15x15 - 225 células
    elif dificuldade == 3:
        matriz_size = HARD_SIZE      # 20x20 - 400 células
    else:
        # Valor padrão para entradas inválidas
        matriz_size = MEDIUM_SIZE    # Fallback seguro para médio
    
    return matriz_size
    
