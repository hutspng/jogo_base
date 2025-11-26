"""
GAME/GAME_UI.PY - Interface Principal do Jogo Caça Palavras
===========================================================
Este módulo implementa a tela principal onde o jogador interage com o caça-palavras.
Responsável por:
- Renderizar a matriz de letras como grade interativa
- Implementar seleção de palavras por clique e arrasto
- Exibir lista de dicas (ocultas, reveladas por clique)
- Validar seleções contra palavras posicionadas
- Gerenciar estado do jogo (palavras encontradas, contador)
- Processar atalhos de teclado (E, D, C, ESC)
- Mostrar popup de vitória ao completar todas as palavras

Características interativas:
- Clique e arrasto em 8 direções (horizontal, vertical, diagonal)
- Destacar path temporário durante seleção
- Validação exata contra coordenadas das palavras posicionadas
- Auto-revelação de dicas quando palavra é encontrada
- Sidebar rolável com dicas
- Atalhos: E (revelar todas dicas), D (desistir), C (ajuda), ESC (sair)
"""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QGridLayout
    , QScrollArea, QMessageBox
)
from PyQt6.QtGui import QFontDatabase, QFont, QCursor
from PyQt6.QtCore import Qt
from consts import FONT_PATH, FONT_PIXEL_SIZE, FONT_PIXEL_BIG_SIZE

class TelaJogo(QWidget):
    """
    Tela principal do jogo onde o usuário interage com o caça-palavras.
    
    Esta classe gerencia toda a interface e lógica de interação do jogo,
    desde a renderização da matriz até a validação de seleções e controle
    de estado da partida.
    """
    
    def __init__(self, matriz, palavras_info, on_finish=None):
        """
        Inicializa a tela de jogo com dados gerados pelo motor do jogo.
        
        Args:
            matriz (list): Matriz 2D de caracteres gerada pelo game.py
            palavras_info (list): Lista de dicionários com metadados das palavras:
                                 {'palavra': str, 'dica': str, 'posicoes': list, 'encontrada': bool}
            on_finish (callable): Callback executado quando jogo termina (vitória/ESC)
        """
        super().__init__()

        # ============================================================================
        # CONFIGURAÇÃO BÁSICA DA JANELA
        # ============================================================================
        self.setWindowTitle("Caça Palavras - Jogo")
        self.setStyleSheet("background-color: #111018;")
        self.setFixedSize(1280, 720)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Para receber eventos de teclado

        # ============================================================================
        # ESTADO DO JOGO E DADOS
        # ============================================================================
        self.matriz = matriz                    # Matriz 2D com as letras do jogo
        self.palavras_info = palavras_info      # Metadados das palavras posicionadas
        self._grid_labels = []                  # Matriz 2D de widgets QLabel (células da UI)
        self._found_cells = set()               # Set de tuplas (i,j) das células já encontradas
        self._selecting = False                 # Flag indicando se está fazendo seleção
        self._start_cell = None                 # Tupla (i,j) onde iniciou a seleção atual
        self._current_path = []                 # Lista de tuplas (i,j) do path sendo selecionado
        self._coords_map = {}                   # Mapa {tupla_coordenadas: índice_palavra}
        self._coords_map_rev = {}               # Mapa para coordenadas reversas
        self._on_finish = on_finish             # Callback para fim de jogo
        self._game_over = False                 # Flag para prevenir interações após vitória

        # ============================================================================
        # CONFIGURAÇÃO DE FONTE E ESTILOS
        # ============================================================================
        # Carrega fonte personalizada pixel art para manter consistência visual
        QFontDatabase.addApplicationFont(FONT_PATH)
        font_title = QFont("Press Start 2P", FONT_PIXEL_BIG_SIZE)
        font_pixel = QFont("Press Start 2P", FONT_PIXEL_SIZE)
        self._font_pixel = font_pixel

        # ============================================================================
        # LAYOUT PRINCIPAL HORIZONTAL (matriz + sidebar dicas)
        # ============================================================================
        layout_main = QHBoxLayout(self)
        layout_main.setContentsMargins(10, 10, 10, 10)
        layout_main.setSpacing(10)

        # ============================================================================
        # ÁREA ESQUERDA - MATRIZ INTERATIVA
        # ============================================================================
        # Container principal da grade de letras
        esquerda = QFrame()
        esquerda.setStyleSheet("""
            QFrame {
                background-color: #0c0c12;
                border: 4px solid #0a0a0f;
            }
        """)
        esquerda_layout = QVBoxLayout()
        esquerda_layout.setContentsMargins(16, 16, 16, 16)
        esquerda_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Grade QGridLayout para organizar células da matriz
        grid = QGridLayout()
        grid.setSpacing(4)  # Espaçamento entre células

        # Tamanho dinâmico das células baseado no tamanho da matriz
        n = len(matriz)
        cell_size = 40 if n <= 12 else 28  # Células menores para matrizes grandes


        # ============================================================================
        # ESTILOS CSS PARA ESTADOS DAS CÉLULAS
        # ============================================================================
        STYLE_DEFAULT = (
            "QLabel {"
            "background-color: #1a1a24;"     # Cinza escuro padrão
            "color: white;"
            "border: 2px solid #2a2a3a;"
            "border-radius: 6px;"
            "}"
        )
        STYLE_SELECTED = (
            "QLabel {"
            "background-color: #2d3d5a;"     # Azul durante seleção temporária
            "color: white;"
            "border: 2px solid #4b6aa8;"
            "border-radius: 6px;"
            "}"
        )
        STYLE_FOUND = (
            "QLabel {"
            "background-color: #2f8f46;"     # Verde para palavras já encontradas
            "color: white;"
            "border: 2px solid #45c165;"
            "border-radius: 6px;"
            "}"
        )

        # Referência ao container para cálculos de hit-testing durante arrasto
        self._esquerda = esquerda

        # ============================================================================
        # CLASSE CELLLABEL - CÉLULA INTERATIVA DA MATRIZ
        # ============================================================================
        # Definir classe interna para evitar problemas de escopo com referências parent
        parent = self

        class CellLabel(QLabel):
            """
            Célula individual da matriz que responde a eventos de mouse.
            
            Cada célula conhece sua posição (i, j) na matriz e implementa
            a lógica de seleção por clique e arrasto. Os eventos são delegados
            para a classe pai TelaJogo que gerencia o estado global da seleção.
            """
            
            def __init__(self, i, j, letra):
                """
                Inicializa uma célula da matriz com sua posição e letra.
                
                Args:
                    i, j (int): Coordenadas da célula na matriz
                    letra (str): Caractere a ser exibido na célula
                """
                super().__init__(letra)
                self.i = i
                self.j = j
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setFont(font_pixel)
                self.setFixedSize(cell_size, cell_size)
                self.setStyleSheet(STYLE_DEFAULT)
                self.setMouseTracking(True)  # Necessário para capturar movimento durante arrasto

            def enterEvent(self, event):
                """Atualiza seleção quando mouse entra na célula durante arrasto."""
                if parent._selecting:
                    parent._update_selection(self.i, self.j)
                super().enterEvent(event)

            def mousePressEvent(self, event):
                """Inicia seleção quando clique esquerdo é pressionado."""
                if event.button() == Qt.MouseButton.LeftButton:
                    parent._start_selection(self.i, self.j)
                super().mousePressEvent(event)

            def mouseReleaseEvent(self, event):
                """Finaliza seleção quando botão do mouse é solto."""
                if parent._selecting:
                    parent._finalize_selection()
                super().mouseReleaseEvent(event)

            def mouseMoveEvent(self, event):
                """
                Processa movimento do mouse durante arrasto.
                
                Durante o arrasto, identifica qual célula está sob o cursor
                mesmo que o mouse não esteja exatamente sobre esta célula específica.
                """
                if parent._selecting:
                    # Converte posição global do mouse para coordenadas locais do container
                    global_pos = event.globalPosition().toPoint()
                    local_in_esquerda = parent._esquerda.mapFromGlobal(global_pos)
                    
                    # Identifica qual widget filho está sob o cursor (hit-testing)
                    target = parent._esquerda.childAt(local_in_esquerda)
                    if isinstance(target, CellLabel):
                        parent._update_selection(target.i, target.j)
                super().mouseMoveEvent(event)

        # ============================================================================
        # CONSTRUÇÃO DA GRADE DE CÉLULAS INTERATIVAS
        # ============================================================================
        # Cria matriz bidimensional de widgets CellLabel correspondente à matriz de dados
        for i, linha in enumerate(matriz):
            row = []
            for j, letra in enumerate(linha):
                lbl = CellLabel(i, j, letra)
                grid.addWidget(lbl, i, j)  # Adiciona na posição (i,j) do layout de grade
                row.append(lbl)
            self._grid_labels.append(row)

        # Monta estrutura da área esquerda
        esquerda_layout.addLayout(grid)
        esquerda.setLayout(esquerda_layout)

        # ============================================================================
        # ÁREA DIREITA - SIDEBAR COM CONTADOR E DICAS
        # ============================================================================
        # Container da sidebar com lista de dicas clicáveis
        direita = QFrame()
        direita.setStyleSheet("""
            QFrame {
                background-color: #0c0c12;
                border-left: 6px solid #000;
            }
        """)

        direita_container_layout = QVBoxLayout(direita)
        direita_container_layout.setContentsMargins(30, 20, 30, 20)
        direita_container_layout.setSpacing(15)

        # ============================================================================
        # CONTADOR DE PROGRESSO
        # ============================================================================
        # Exibe quantas palavras foram encontradas do total
        total = len(palavras_info)
        titulo_palavras = QLabel(f"palavras encontradas: 0/{total}")
        titulo_palavras.setFont(font_pixel)
        titulo_palavras.setStyleSheet("color: white;")
        titulo_palavras.setAlignment(Qt.AlignmentFlag.AlignCenter)
        direita_container_layout.addWidget(titulo_palavras)
        self._titulo_palavras = titulo_palavras

        # ============================================================================
        # ÁREA DE DICAS ROLÁVEIS
        # ============================================================================
        # Container scrollável para lista de dicas (inicialmente ocultas)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; }
            QScrollBar:vertical { background: #0c0c12; width: 12px; }
            QScrollBar::handle:vertical { background: #2a2a3a; min-height: 24px; border-radius: 6px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)
        scroll_content = QWidget()
        dicas_layout = QVBoxLayout(scroll_content)
        dicas_layout.setContentsMargins(0, 0, 0, 0)
        dicas_layout.setSpacing(12)
        scroll.setWidget(scroll_content)
        self._dicas_layout = dicas_layout
        # ============================================================================
        # CLASSE DICAITEM - ITEM CLICÁVEL DA LISTA DE DICAS
        # ============================================================================
        class DicaItem(QLabel):
            """
            Widget interativo para exibir dicas das palavras.
            
            Comportamentos:
            - Inicialmente oculta ("clique para revelar dica")
            - Clique revela o texto real da dica (cor laranja)
            - Segundo clique permite ocultar novamente (toggle)
            - Quando palavra é encontrada: auto-revela e trava (cor verde)
            - Suporte ao atalho 'E' para revelar todas as dicas
            """
            
            def __init__(self, dica_texto: str):
                """
                Inicializa item de dica em estado oculto.
                
                Args:
                    dica_texto (str): Texto da dica a ser revelado quando clicado
                """
                super().__init__("clique para revelar dica")
                self._dica = dica_texto or "(sem dica)"
                self._revealed = False    # Se a dica está sendo exibida
                self._locked = False      # Se o item está travado (palavra encontrada)
                self.setFont(font_pixel)
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setWordWrap(True)
                self.setMinimumHeight(40)
                self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.setStyleSheet("""
                    QLabel {
                        background-color: #2a2a3a;
                        color: #cccccc;
                        border-radius: 8px;
                        padding: 10px;
                        border: 1px solid #3a3a4a;
                        min-height: 40px;
                    }
                """)

            def mousePressEvent(self, event):
                """
                Toggle de revelação da dica ao clicar (se não estiver travada).
                
                Estados:
                - Oculta -> Revelada (laranja): mostra texto da dica
                - Revelada -> Oculta (cinza): volta ao texto padrão
                - Travada: ignora cliques (palavra já foi encontrada)
                """
                if self._locked:
                    return
                
                if not self._revealed:
                    # Revela a dica
                    self._revealed = True
                    self.setText(self._dica)
                    self.setStyleSheet("""
                        QLabel {
                            background-color: #ff8c00;
                            color: black;
                            border-radius: 8px;
                            padding: 10px;
                            border: 1px solid #cc6f00;
                        }
                    """)
                else:
                    # Oculta a dica novamente (toggle)
                    self._revealed = False
                    self.setText("clique para revelar dica")
                    self.setStyleSheet("""
                        QLabel {
                            background-color: #2a2a3a;
                            color: #cccccc;
                            border-radius: 8px;
                            padding: 10px;
                            border: 1px solid #3a3a4a;
                        }
                    """)

            def reveal(self, lock: bool = False):
                """
                Força revelação da dica (usado pelo atalho 'E').
                
                Args:
                    lock (bool): Se deve travar o item após revelação
                """
                if not self._revealed:
                    self._revealed = True
                    self.setText(self._dica)
                    self.setStyleSheet("""
                        QLabel {
                            background-color: #ff8c00;
                            color: black;
                            border-radius: 8px;
                            padding: 10px;
                            border: 1px solid #cc6f00;
                        }
                    """)
                self._locked = lock or self._locked

            def mark_found(self):
                """
                Marca dica como encontrada (verde) e trava interação.
                
                Chamado automaticamente quando palavra correspondente é descoberta.
                Estado final: revelada + travada + estilo verde.
                """
                self._revealed = True
                self._locked = True
                self.setText(self._dica)
                self.setStyleSheet("""
                    QLabel {
                        background-color: #2f8f46;
                        color: white;
                        border-radius: 8px;
                        padding: 10px;
                        border: 1px solid #45c165;
                    }
                """)

        # ============================================================================
        # CONSTRUÇÃO DA LISTA DE DICAS E MAPEAMENTO
        # ============================================================================
        # Cria widgets DicaItem para cada palavra e mapeia palavra->widget para acesso direto
        self._mapa_dicas = {}
        for info in palavras_info:
            dica = info.get('dica', '(sem dica)')
            palavra = info.get('palavra', '')
            item = DicaItem(dica)
            self._dicas_layout.addWidget(item)
            if palavra:
                self._mapa_dicas[palavra] = item  # Permite marcar dica quando palavra for encontrada

        # Espaçador para empurrar itens para o topo da área rolável
        self._dicas_layout.addStretch(1)
        
        # Adiciona área rolável ao container da sidebar
        direita_container_layout.addWidget(scroll, stretch=1)

        # ============================================================================
        # MONTAGEM FINAL DO LAYOUT PRINCIPAL
        # ============================================================================
        # Layout horizontal: matriz (esquerda) + sidebar (direita)
        layout_main.addWidget(esquerda, stretch=2)   # Matriz ocupa 2/3 do espaço
        layout_main.addWidget(direita, stretch=1)    # Sidebar ocupa 1/3 do espaço

        # ============================================================================
        # PRÉ-COMPUTAÇÃO DE MAPEAMENTO DE COORDENADAS
        # ============================================================================
        # Cria lookup tables para validação eficiente de seleções
        # Mapeia coordenadas -> índice da palavra (ambas direções)
        for idx, info in enumerate(self.palavras_info):
            coords = tuple(info.get('posicoes', []))
            if not coords:
                continue
            self._coords_map[coords] = idx                        # Direção original
            self._coords_map_rev[tuple(reversed(coords))] = idx  # Direção reversa

        # Define foco para receber eventos de teclado (atalhos)
        self.setFocus()

    # ============================================================================
    # MÉTODOS DE GERENCIAMENTO DA SELEÇÃO POR CLIQUE E ARRASTO
    # ============================================================================
    
    def _start_selection(self, i: int, j: int):
        """
        Inicia processo de seleção quando usuário clica em uma célula.
        
        Args:
            i, j (int): Coordenadas da célula onde iniciou a seleção
        """
        # Não permite iniciar seleção em células já encontradas
        if (i, j) in self._found_cells:
            return
        self._selecting = True
        self._start_cell = (i, j)
        self._set_temporary_path([(i, j)])

    def _update_selection(self, i: int, j: int):
        """
        Atualiza seleção atual baseada na posição do mouse durante arrasto.
        
        Calcula path em linha reta nas 8 direções possíveis:
        - Horizontal (esquerda/direita)
        - Vertical (cima/baixo)  
        - Diagonais (4 direções)
        
        Args:
            i, j (int): Coordenadas da célula atual do mouse
        """
        if not self._selecting or self._start_cell is None:
            return
        
        # Calcula diferenças de posição para determinar direção
        si, sj = self._start_cell
        di = i - si  # Delta vertical
        dj = j - sj  # Delta horizontal
        
        # ====================================================================
        # ALGORITMO DE RESTRIÇÃO ÀS 8 DIREÇÕES
        # ====================================================================
        # Constrói path apenas se movimento está em uma das 8 direções válidas
        
        if di == 0 and dj == 0:
            # Mesmo ponto: path de uma célula
            path = [(si, sj)]
        elif di == 0:
            # Movimento horizontal (mesma linha)
            step = 1 if dj > 0 else -1
            path = [(si, sj)] + [(si, sj + k) for k in range(step, dj + step, step)]
        elif dj == 0:
            # Movimento vertical (mesma coluna)
            step = 1 if di > 0 else -1
            path = [(si, sj)] + [(si + k, sj) for k in range(step, di + step, step)]
        elif abs(di) == abs(dj):
            # Movimento diagonal (45°): delta X == delta Y
            stepi = 1 if di > 0 else -1
            stepj = 1 if dj > 0 else -1
            length = abs(di)
            path = [(si + k * stepi, sj + k * stepj) for k in range(0, length + 1)]
        else:
            # Movimento fora das 8 direções válidas: ignora
            return
        
        # Verifica se todas as coordenadas estão dentro dos limites da matriz
        n = len(self.matriz)
        for (pi, pj) in path:
            if pi < 0 or pj < 0 or pi >= n or pj >= n:
                return
        
        # Atualiza UI com o path temporário
        self._set_temporary_path(path)

    def _finalize_selection(self):
        """
        Finaliza seleção quando usuário solta o botão do mouse.
        
        Processo:
        1. Verifica se o path selecionado corresponde a alguma palavra
        2. Se encontrou palavra válida:
           - Marca células como encontradas (verde permanente)
           - Atualiza contador de progresso
           - Revela e trava a dica correspondente
           - Verifica condição de vitória
        3. Limpa seleção temporária
        """
        if self._game_over or not self._current_path:
            self._reset_temporary_selection()
            return
        
        # Converte path para tupla para busca nos mapas de coordenadas
        path_tuple = tuple(self._current_path)
        
        # Busca palavra correspondente (direção normal e reversa)
        idx = self._coords_map.get(path_tuple)
        if idx is None:
            idx = self._coords_map_rev.get(path_tuple)  # Tenta direção reversa
        
        if idx is not None:
            info = self.palavras_info[idx]
            if not info.get('encontrada', False):
                # ============================================================
                # PALAVRA ENCONTRADA - ATUALIZAR ESTADO DO JOGO
                # ============================================================
                info['encontrada'] = True
                
                # Marca células da palavra como encontradas (estilo verde permanente)
                for (i, j) in path_tuple:
                    self._found_cells.add((i, j))
                    self._grid_labels[i][j].setStyleSheet(
                        "QLabel {background-color: #2f8f46; color: white; border: 2px solid #45c165; border-radius: 6px;}"
                    )
                
                # Atualiza contador de palavras encontradas
                self._update_counter()
                
                # Revela e trava dica correspondente
                palavra = info.get('palavra', '')
                dica_item = self._mapa_dicas.get(palavra)
                if dica_item:
                    dica_item.mark_found()
                
                # Verifica se todas as palavras foram encontradas (condição de vitória)
                if self._all_found():
                    self._game_over = True
                    self._mostrar_vitoria_e_finalizar()
        
        # Limpa seleção temporária independentemente do resultado
        self._reset_temporary_selection()

    def _set_temporary_path(self, path):
        """
        Aplica estilo temporário (azul) às células do path atual durante seleção.
        
        Args:
            path (list): Lista de tuplas (i, j) representando o caminho selecionado
        """
        self._clear_temp_styles()  # Remove estilos temporários anteriores
        self._current_path = path
        
        # Aplica estilo azul temporário às células do path (exceto já encontradas)
        for (i, j) in path:
            if (i, j) in self._found_cells:
                continue  # Não sobrescreve estilo de células já encontradas
            self._grid_labels[i][j].setStyleSheet(
                "QLabel {background-color: #2d3d5a; color: white; border: 2px solid #4b6aa8; border-radius: 6px;}"
            )

    def _reset_temporary_selection(self):
        """
        Reseta completamente o estado de seleção temporária.
        
        Chamado quando:
        - Seleção é finalizada (com ou sem palavra encontrada)
        - Usuário cancela seleção
        - Novo clique inicia nova seleção
        """
        self._selecting = False
        self._start_cell = None
        self._current_path = []
        self._clear_temp_styles()

    def _clear_temp_styles(self):
        """
        Remove estilos temporários e restaura aparência padrão das células.
        
        Preserva células já encontradas (verde) e restaura células
        não encontradas ao estilo padrão (cinza escuro).
        """
        for i, row in enumerate(self._grid_labels):
            for j, lbl in enumerate(row):
                if (i, j) in self._found_cells:
                    continue  # Preserva estilo verde das células encontradas
                lbl.setStyleSheet(
                    "QLabel {background-color: #1a1a24; color: white; border: 2px solid #2a2a3a; border-radius: 6px;}"
                )

    def _mostrar_vitoria_e_finalizar(self):
        """
        Exibe popup de vitória e retorna ao menu principal.
        
        Chamado quando todas as palavras foram encontradas.
        Após o usuário fechar o popup, executa callback de finalização
        para retornar ao menu principal.
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("Vitória!")
        msg.setText("parabens você venceu, sua reconpensa é... absolutamente nada!")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Close)
        
        # Traduz texto do botão para português
        btn = msg.button(QMessageBox.StandardButton.Close)
        if btn is not None:
            btn.setText("Fechar")
        
        # Habilita botão X da janela
        msg.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, True)
        
        # Aplica estilo consistente com o tema do jogo
        msg.setStyleSheet(
            "QMessageBox { background-color: #111018; }"
            "QLabel { color: white; font-family: 'Press Start 2P'; }"
        )
        
        msg.exec()
        
        # Após fechar popup, retorna ao menu principal
        if callable(self._on_finish):
            self._on_finish()
        else:
            self.close()

    def _update_counter(self):
        """
        Atualiza display do contador de palavras encontradas.
        
        Chamado sempre que uma nova palavra é descoberta.
        Formato: "palavras encontradas: X/Y"
        """
        total = len(self.palavras_info)
        encontrados = sum(1 for p in self.palavras_info if p.get('encontrada'))
        self._titulo_palavras.setText(f"palavras encontradas: {encontrados}/{total}")

    def _all_found(self) -> bool:
        """
        Verifica se todas as palavras foram encontradas (condição de vitória).
        
        Returns:
            bool: True se todas as palavras estão marcadas como encontradas
        """
        return all(p.get('encontrada') for p in self.palavras_info)

    def _reveal_all_hints(self):
        """
        Revela todas as dicas sem travar (atalho 'E').
        
        Permite ao usuário ver todas as dicas de uma vez para facilitar
        a localização das palavras restantes.
        """
        for item in self._mapa_dicas.values():
            item.reveal(lock=False)  # Revela mas permite ocultar novamente

    def _desistir_mark_all_found(self):
        """
        Marca todas as palavras como encontradas e finaliza o jogo (atalho 'D').
        
        Funcionalidade de "desistir":
        - Revela posição de todas as palavras na matriz (verde)
        - Marca todas as dicas como encontradas e travadas
        - Atualiza contador para 100%
        - Exibe popup de vitória
        """
        for info in self.palavras_info:
            if not info.get('encontrada'):
                info['encontrada'] = True
                # Pinta todas as células da palavra como encontradas
                for (i, j) in info.get('posicoes', []):
                    self._found_cells.add((i, j))
                    self._grid_labels[i][j].setStyleSheet(
                        "QLabel {background-color: #2f8f46; color: white; border: 2px solid #45c165; border-radius: 6px;}"
                    )
                # Marca dica correspondente como encontrada
                dica_item = self._mapa_dicas.get(info.get('palavra', ''))
                if dica_item:
                    dica_item.mark_found()
        
        self._update_counter()
        
        # Finaliza jogo se ainda não estava terminado
        if not self._game_over:
            self._game_over = True
            self._mostrar_vitoria_e_finalizar()

    def show_como_jogar(self):
        """
        Exibe popup com instruções do jogo (atalho 'C').
        
        Mostra explicação dos controles:
        - Mecânica de clique e arrasto
        - Atalhos de teclado disponíveis
        - Como validar seleções
        """
        texto = (
            "Como jogar:\n\n"
            "- Clique e arraste para selecionar letras em linha reta.\n"
            "- Solte para validar a palavra selecionada.\n"
            "- 'E' revela todas as dicas.\n"
            "- 'D' desiste e marca todas as palavras.\n"
            "- 'C' abre este guia."
        )
        msg = QMessageBox(self)
        msg.setWindowTitle("Como jogar")
        msg.setText(texto)
        msg.setStyleSheet(
            "QMessageBox { background-color: #111018; }"
            "QMessageBox QLabel { color: white; font-family: 'Press Start 2P'; }"
            "QLabel { color: white; font-family: 'Press Start 2P'; }"
            "QPushButton { background-color: #2a2a3a; color: white; }"
        )
        msg.exec()

    # ============================================================================
    # PROCESSAMENTO DE ATALHOS DE TECLADO
    # ============================================================================
    
    def keyPressEvent(self, event):
        """
        Processa atalhos de teclado durante o jogo.
        
        Atalhos disponíveis:
        - E: Revela todas as dicas
        - D: Desiste (marca todas as palavras como encontradas)
        - C: Abre guia "Como jogar"
        - ESC: Sai do jogo e volta ao menu (processado pela classe pai)
        
        Args:
            event: Evento de teclado do Qt
        """
        key = event.key()
        
        if key in (Qt.Key.Key_E,):
            self._reveal_all_hints()
            event.accept()
            return
        
        if key in (Qt.Key.Key_D,):
            self._desistir_mark_all_found()
            event.accept()
            return
        
        if key in (Qt.Key.Key_C,):
            self.show_como_jogar()
            event.accept()
            return
            
        if key in (Qt.Key.Key_Escape,):
            # Atalho ESC: volta ao menu principal
            if callable(self._on_finish):
                self._on_finish()
            else:
                self.close()
            event.accept()
            return
        
        # Delega eventos não tratados para a classe pai
        super().keyPressEvent(event)
