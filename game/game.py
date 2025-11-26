"""
GAME/GAME.PY - Motor Principal do Jogo Caça Palavras  
====================================================
Este módulo implementa toda a lógica de geração do caça-palavras.
Responsável por:
- Carregar palavras e dicas do arquivo JSON
- Selecionar aleatoriamente as palavras para cada jogo
- Posicionar palavras na matriz em 8 direções diferentes
- Preencher espaços vazios com letras aleatórias
- Validar posicionamento (evitar sobreposições inválidas)
- Coordenar todo o processo de geração

Algoritmo de geração:
1. Carregar banco de palavras do JSON
2. Selecionar 10 palavras aleatórias 
3. Para cada palavra, tentar posicionar em posição/direção aleatória
4. Validar se cabe sem conflitos (máx 100 tentativas por palavra)
5. Preencher células vazias com letras aleatórias
6. Retornar matriz final e posições das palavras colocadas

Direções suportadas: horizontal, vertical, diagonal (8 direções totais)
"""

from consts import log, PATH_PALAVRAS_JSON
import json
import random
import string

# ============================================================================
# ESTADO GLOBAL DO JOGO
# ============================================================================
# Variáveis globais mantêm o estado atual da partida gerada
matriz = []                    # Matriz principal do jogo (lista 2D de caracteres)
palavras_selecionadas = []     # Lista das 10 palavras escolhidas aleatoriamente
posicoes_palavras = []         # Lista com info de cada palavra: posição, dica, coordenadas


def carregar_palavras():
    """
    Carrega e processa todas as palavras disponíveis do arquivo de dados.
    
    Lê o arquivo palavras.json que contém um dicionário de palavras com suas
    respectivas dicas. Cada entrada no JSON tem uma palavra (chave 'palavra' ou 
    'palvra' devido a erros de digitação) e uma dica explicativa.
    
    Returns:
        list: Lista de dicionários, cada um contendo:
              - 'palavra': texto da palavra em MAIÚSCULAS
              - 'dica': texto descritivo para ajudar o jogador
              
    Tratamento de erros:
    - Se arquivo não existir ou for inválido, retorna lista vazia
    - Ignora entradas sem texto de palavra válido
    - Normaliza todas as palavras para MAIÚSCULAS para consistência
    """
    try:
        with open(PATH_PALAVRAS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            palavras_dict = data.get('palavras', {})
            
            # Converter estrutura do JSON para lista de objetos palavra  
            palavras = []
            for key, value in palavras_dict.items():
                # Verificar chave 'palavra' com fallback para 'palvra' (erro de digitação no JSON)
                palavra_texto = value.get('palavra', value.get('palvra', '')).upper()
                dica = value.get('dica', 'Sem dica')
                
                # Só incluir se tiver texto válido para a palavra
                if palavra_texto:
                    palavras.append({'palavra': palavra_texto, 'dica': dica})
                    
            log(f"game.py", f"Carregadas {len(palavras)} palavras do JSON")
            return palavras
            
    except Exception as e:
        log("game.py", f"Erro ao carregar palavras: {e}")
        return []

def selecionar_palavras_aleatorias(palavras, quantidade=10):
    """
    Seleciona um subconjunto aleatório de palavras para usar no jogo atual.
    
    Args:
        palavras (list): Lista completa de palavras disponíveis
        quantidade (int): Número de palavras a selecionar (padrão: 10)
        
    Returns:
        list: Lista com as palavras selecionadas aleatoriamente
        
    Comportamento:
    - Se há menos palavras disponíveis que a quantidade solicitada,
      retorna todas as palavras disponíveis
    - Usa random.sample() para garantir seleção sem repetição
    - Cada jogo terá combinação diferente de palavras
    """
    if len(palavras) < quantidade:
        log("game.py", f"Apenas {len(palavras)} palavras disponíveis")
        return palavras
        
    selecionadas = random.sample(palavras, quantidade)
    log("game.py", f"Selecionadas {len(selecionadas)} palavras")
    return selecionadas


def pode_colocar_palavra(palavra, linha, coluna, direcao, size):
    """
    Valida se uma palavra pode ser posicionada na matriz sem conflitos.
    
    Verifica duas condições essenciais:
    1. A palavra cabe inteiramente dentro dos limites da matriz
    2. Não há conflitos com letras já posicionadas (permite sobreposição apenas 
       se a letra for exatamente a mesma)
    
    Args:
        palavra (str): Texto da palavra a ser posicionada
        linha (int): Linha inicial (0-indexed) 
        coluna (int): Coluna inicial (0-indexed)
        direcao (tuple): Vetor direção como (dx, dy) onde:
                        dx = deslocamento vertical (-1, 0, 1)
                        dy = deslocamento horizontal (-1, 0, 1)
        size (int): Tamanho da matriz (NxN)
        
    Returns:
        bool: True se a palavra pode ser posicionada, False caso contrário
        
    Exemplos de direções:
    - (0, 1): horizontal esquerda → direita
    - (1, 0): vertical cima → baixo  
    - (1, 1): diagonal cima-esq → baixo-dir
    - (-1, -1): diagonal baixo-dir → cima-esq
    """
    dx, dy = direcao
    comprimento = len(palavra)
    
    # Calcular posição final que a palavra ocupará
    end_linha = linha + dx * (comprimento - 1)
    end_coluna = coluna + dy * (comprimento - 1)
    
    # Verificar se a palavra sai dos limites da matriz
    if end_linha < 0 or end_linha >= size or end_coluna < 0 or end_coluna >= size:
        return False
    
    # Verificar cada posição que a palavra ocupará
    for i in range(comprimento):
        r = linha + dx * i
        c = coluna + dy * i
        
        # Se a célula já está ocupada, só permite se for exatamente a mesma letra
        # (permite cruzamento de palavras que compartilham letras)
        if matriz[r][c] != '' and matriz[r][c] != palavra[i]:
            return False
    
    return True

def colocar_palavra(palavra, linha, coluna, direcao):
    """
    Posiciona uma palavra na matriz e retorna as coordenadas ocupadas.
    
    Esta função assume que a validação já foi feita com pode_colocar_palavra().
    Modifica diretamente a matriz global inserindo cada letra da palavra na 
    posição calculada pela direção especificada.
    
    Args:
        palavra (str): Palavra a ser inserida na matriz
        linha (int): Linha inicial de posicionamento
        coluna (int): Coluna inicial de posicionamento  
        direcao (tuple): Vetor direção (dx, dy)
        
    Returns:
        list: Lista de tuplas (linha, coluna) com todas as posições ocupadas
              pela palavra. Essas coordenadas são usadas posteriormente para
              validação quando o jogador seleciona palavras.
              
    Efeitos colaterais:
    - Modifica a matriz global inserindo as letras
    - As posições retornadas são armazenadas em posicoes_palavras para consulta
    """
    dx, dy = direcao
    posicoes = []
    
    # Inserir cada letra da palavra na matriz seguindo a direção
    for i, letra in enumerate(palavra):
        r = linha + dx * i
        c = coluna + dy * i
        matriz[r][c] = letra
        posicoes.append((r, c))
    
    return posicoes


def posicionar_palavras(size, palavras):
    """
    Algoritmo principal para posicionar todas as palavras selecionadas na matriz.
    
    Este é o coração do gerador de caça-palavras. Tenta posicionar cada palavra
    em posições e direções aleatórias, validando conflitos e limites. Se uma 
    palavra não puder ser posicionada após muitas tentativas, é ignorada.
    
    Args:
        size (int): Tamanho da matriz (NxN)
        palavras (list): Lista de objetos palavra com 'palavra' e 'dica'
        
    Returns:
        list: Lista com nomes das palavras que foram posicionadas com sucesso
        
    Algoritmo:
    1. Inicializar matriz vazia 
    2. Para cada palavra:
       - Tentar até 100 posições/direções aleatórias
       - Validar se cabe sem conflitos
       - Se cabe, posicionar e registrar coordenadas
       - Se não cabe após 100 tentativas, pular palavra
    3. Retornar lista de palavras posicionadas
    
    Efeitos colaterais:
    - Modifica matriz global
    - Popula posicoes_palavras com metadados de cada palavra posicionada
    """
    global matriz, posicoes_palavras
    
    # Inicializar estado limpo para nova geração
    matriz = [['' for _ in range(size)] for _ in range(size)]
    posicoes_palavras = []
    
    # Definir todas as 8 direções possíveis para posicionamento
    # Cada direção é um vetor (dx, dy) que define o incremento por letra
    direcoes = [
        (0, 1),   # horizontal: esquerda → direita
        (1, 0),   # vertical: cima → baixo
        (1, 1),   # diagonal: cima-esquerda → baixo-direita
        (1, -1),  # diagonal: cima-direita → baixo-esquerda  
        (0, -1),  # horizontal reversa: direita → esquerda
        (-1, 0),  # vertical reversa: baixo → cima
        (-1, -1), # diagonal reversa: baixo-direita → cima-esquerda
        (-1, 1),  # diagonal reversa: baixo-esquerda → cima-direita
    ]
    
    palavras_colocadas = []
    
    # Tentar posicionar cada palavra individualmente
    for palavra_obj in palavras:
        palavra = palavra_obj['palavra']
        tentativas = 0
        max_tentativas = 100  # Limite para evitar loops infinitos
        colocada = False
        
        # Algoritmo de tentativa e erro para posicionamento
        while tentativas < max_tentativas and not colocada:
            # Escolher posição inicial aleatória
            linha = random.randint(0, size - 1)
            coluna = random.randint(0, size - 1)
            direcao = random.choice(direcoes)
            
            # Tentar posicionar nesta posição/direção
            if pode_colocar_palavra(palavra, linha, coluna, direcao, size):
                # Sucesso! Posicionar palavra e registrar metadados
                posicoes = colocar_palavra(palavra, linha, coluna, direcao)
                posicoes_palavras.append({
                    'palavra': palavra,
                    'dica': palavra_obj['dica'],
                    'posicoes': posicoes,        # Coordenadas para validação de seleção
                    'encontrada': False          # Status do jogo
                })
                palavras_colocadas.append(palavra)
                colocada = True
                log("game.py", f"Palavra '{palavra}' colocada na posição ({linha},{coluna}) direção {direcao}")
            
            tentativas += 1
        
        # Se não conseguiu posicionar após todas as tentativas
        if not colocada:
            log("game.py", f"Não foi possível colocar a palavra '{palavra}' após {max_tentativas} tentativas")
    
    log("game.py", f"Total de palavras colocadas: {len(palavras_colocadas)}/{len(palavras)}")
    return palavras_colocadas

def completar_matriz(size):
    """
    Preenche todas as células vazias da matriz com letras aleatórias.
    
    Esta é a etapa final da geração do caça-palavras. Após posicionar todas
    as palavras possíveis, as células restantes são preenchidas com letras
    aleatórias para "camuflar" as palavras e tornar o jogo desafiador.
    
    Args:
        size (int): Tamanho da matriz (NxN)
        
    Comportamento:
    - Percorre toda a matriz buscando células vazias (string vazia)
    - Substitui cada célula vazia por uma letra maiúscula aleatória (A-Z)
    - Usa string.ascii_uppercase para garantir distribuição uniforme
    
    Efeitos colaterais:
    - Modifica matriz global preenchendo células vazias
    """
    global matriz
    
    letras = string.ascii_uppercase  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Percorrer toda a matriz
    for i in range(size):
        for j in range(size):
            # Se a célula está vazia, preencher com letra aleatória
            if matriz[i][j] == '':
                matriz[i][j] = random.choice(letras)
    
    log("game.py", "Matriz completada com letras aleatórias")


def gerar(matriz_size):
    """
    Função coordenadora principal que executa todo o processo de geração.
    
    Orquestra todas as etapas necessárias para criar um caça-palavras completo:
    carregamento de dados, seleção aleatória, posicionamento e finalização.
    
    Args:
        matriz_size (int): Tamanho da matriz quadrada a ser gerada
        
    Returns:
        tuple: (matriz, posicoes_palavras) onde:
               - matriz: lista 2D com todas as letras posicionadas
               - posicoes_palavras: lista com metadados de cada palavra posicionada
               
    Fluxo de execução:
    1. Carregar todas as palavras disponíveis do arquivo JSON
    2. Selecionar 10 palavras aleatórias para este jogo
    3. Posicionar as palavras na matriz em posições/direções aleatórias  
    4. Preencher células restantes com letras aleatórias
    5. Retornar matriz completa e informações das palavras
    """
    log("game.py", f"Gerando caça-palavras com matriz {matriz_size}x{matriz_size}")
    
    # ETAPA 1: Carregamento e seleção de palavras
    todas_palavras = carregar_palavras()
    global palavras_selecionadas
    palavras_selecionadas = selecionar_palavras_aleatorias(todas_palavras, 10)
    
    # ETAPA 2: Posicionamento das palavras na matriz
    palavras_colocadas = posicionar_palavras(matriz_size, palavras_selecionadas)
    
    # ETAPA 3: Preenchimento de células vazias  
    completar_matriz(matriz_size)
    
    log("game.py", "Geração do caça-palavras concluída")
    
    return matriz, posicoes_palavras

def abrir_jogo(matriz_size):
    """
    Função de interface pública para inicializar uma partida.
    
    Esta é a função chamada pelos controladores externos (main.py) para
    criar um novo jogo. Ela encapsula o processo de geração e pode ser
    estendida futuramente para incluir outras inicializações necessárias.
    
    Args:
        matriz_size (int): Tamanho da matriz baseado na dificuldade escolhida
                          (10 para fácil, 15 para médio, 20 para difícil)
                          
    Returns:
        tuple: (matriz, posicoes_palavras) - dados necessários para a UI do jogo
        
    Uso típico:
        matriz, posicoes = game.abrir_jogo(15)  # Jogo médio
        # matriz contém a grade de letras para exibição
        # posicoes contém metadados das palavras para validação de seleção
    """
    log("game.py", f"Abrindo jogo com matriz de tamanho {matriz_size}")
    return gerar(matriz_size)
