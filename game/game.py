from consts import log, PATH_PALAVRAS_JSON
import json
import random
import string


# Variáveis globais do jogo
matriz = []
palavras_selecionadas = []
posicoes_palavras = []  # guarda onde cada palavra foi colocada


def carregar_palavras():
    """Carrega todas as palavras do arquivo JSON."""
    try:
        with open(PATH_PALAVRAS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            palavras_dict = data.get('palavras', {})
            # Converter dict para lista de objetos palavra
            palavras = []
            for key, value in palavras_dict.items():
                # Verificar se tem a chave 'palavra' (alguns itens têm 'palvra' por erro)
                palavra_texto = value.get('palavra', value.get('palvra', '')).upper()
                dica = value.get('dica', 'Sem dica')
                if palavra_texto:
                    palavras.append({'palavra': palavra_texto, 'dica': dica})
            log(f"game.py", f"Carregadas {len(palavras)} palavras do JSON")
            return palavras
    except Exception as e:
        log("game.py", f"Erro ao carregar palavras: {e}")
        return []


def selecionar_palavras_aleatorias(palavras, quantidade=10):
    """Seleciona N palavras aleatórias da lista."""
    if len(palavras) < quantidade:
        log("game.py", f"Apenas {len(palavras)} palavras disponíveis")
        return palavras
    selecionadas = random.sample(palavras, quantidade)
    log("game.py", f"Selecionadas {len(selecionadas)} palavras")
    return selecionadas


def pode_colocar_palavra(palavra, linha, coluna, direcao, size):
    """Verifica se a palavra cabe na posição e direção especificadas."""
    dx, dy = direcao
    comprimento = len(palavra)
    
    # Verificar se sai dos limites
    end_linha = linha + dx * (comprimento - 1)
    end_coluna = coluna + dy * (comprimento - 1)
    
    if end_linha < 0 or end_linha >= size or end_coluna < 0 or end_coluna >= size:
        return False
    
    # Verificar se as células estão vazias ou já têm a mesma letra
    for i in range(comprimento):
        r = linha + dx * i
        c = coluna + dy * i
        if matriz[r][c] != '' and matriz[r][c] != palavra[i]:
            return False
    
    return True


def colocar_palavra(palavra, linha, coluna, direcao):
    """Coloca uma palavra na matriz na posição e direção especificadas."""
    dx, dy = direcao
    posicoes = []
    
    for i, letra in enumerate(palavra):
        r = linha + dx * i
        c = coluna + dy * i
        matriz[r][c] = letra
        posicoes.append((r, c))
    
    return posicoes


def posicionar_palavras(size, palavras):
    """Tenta posicionar todas as palavras na matriz."""
    global matriz, posicoes_palavras
    
    # Inicializar matriz vazia
    matriz = [['' for _ in range(size)] for _ in range(size)]
    posicoes_palavras = []
    
    # Direções possíveis: horizontal, vertical, diagonal (4 direções diagonais)
    direcoes = [
        (0, 1),   # horizontal (esquerda -> direita)
        (1, 0),   # vertical (cima -> baixo)
        (1, 1),   # diagonal (cima-esquerda -> baixo-direita)
        (1, -1),  # diagonal (cima-direita -> baixo-esquerda)
        (0, -1),  # horizontal reversa (direita -> esquerda)
        (-1, 0),  # vertical reversa (baixo -> cima)
        (-1, -1), # diagonal reversa
        (-1, 1),  # diagonal reversa
    ]
    
    palavras_colocadas = []
    
    for palavra_obj in palavras:
        palavra = palavra_obj['palavra']
        tentativas = 0
        max_tentativas = 100
        colocada = False
        
        while tentativas < max_tentativas and not colocada:
            # Escolher posição e direção aleatórias
            linha = random.randint(0, size - 1)
            coluna = random.randint(0, size - 1)
            direcao = random.choice(direcoes)
            
            if pode_colocar_palavra(palavra, linha, coluna, direcao, size):
                posicoes = colocar_palavra(palavra, linha, coluna, direcao)
                posicoes_palavras.append({
                    'palavra': palavra,
                    'dica': palavra_obj['dica'],
                    'posicoes': posicoes,
                    'encontrada': False
                })
                palavras_colocadas.append(palavra)
                colocada = True
                log("game.py", f"Palavra '{palavra}' colocada na posição ({linha},{coluna}) direção {direcao}")
            
            tentativas += 1
        
        if not colocada:
            log("game.py", f"Não foi possível colocar a palavra '{palavra}' após {max_tentativas} tentativas")
    
    log("game.py", f"Total de palavras colocadas: {len(palavras_colocadas)}/{len(palavras)}")
    return palavras_colocadas


def completar_matriz(size):
    """Preenche as células vazias da matriz com letras aleatórias."""
    global matriz
    
    letras = string.ascii_uppercase
    
    for i in range(size):
        for j in range(size):
            if matriz[i][j] == '':
                matriz[i][j] = random.choice(letras)
    
    log("game.py", "Matriz completada com letras aleatórias")


def gerar(matriz_size):
    """Gera o caça-palavras completo."""
    log("game.py", f"Gerando caça-palavras com matriz {matriz_size}x{matriz_size}")
    
    # Carregar e selecionar palavras
    todas_palavras = carregar_palavras()
    global palavras_selecionadas
    palavras_selecionadas = selecionar_palavras_aleatorias(todas_palavras, 10)
    
    # Posicionar palavras
    palavras_colocadas = posicionar_palavras(matriz_size, palavras_selecionadas)
    
    # Completar matriz com letras aleatórias
    completar_matriz(matriz_size)
    
    log("game.py", "Geração do caça-palavras concluída")
    
    return matriz, posicoes_palavras


def abrir_jogo(matriz_size):
    """Inicia o jogo gerando a matriz e abrindo a janela."""
    log("game.py", f"Abrindo jogo com matriz de tamanho {matriz_size}")
    gerar(matriz_size)
    # TODO: abrir a janela do jogo com a matriz gerada
    return matriz, posicoes_palavras
