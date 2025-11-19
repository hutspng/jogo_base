from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QGridLayout
    , QScrollArea, QMessageBox
)
from PyQt6.QtGui import QFontDatabase, QFont, QCursor
from PyQt6.QtCore import Qt
from consts import FONT_PATH, FONT_PIXEL_SIZE, FONT_PIXEL_BIG_SIZE


class TelaJogo(QWidget):
    def __init__(self, matriz, palavras_info, on_finish=None):
        super().__init__()

        self.setWindowTitle("Caça Palavras - Jogo")
        self.setStyleSheet("background-color: #111018;")
        self.setFixedSize(1280, 720)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Estado do jogo / referências
        self.matriz = matriz
        self.palavras_info = palavras_info
        self._grid_labels = []  # 2D de células
        self._found_cells = set()  # {(i,j)}
        self._selecting = False
        self._start_cell = None  # (i,j)
        self._current_path = []  # [(i,j), ...]
        self._coords_map = {}  # {tuple(coords): idx}
        self._coords_map_rev = {}  # reversed path -> idx
        self._on_finish = on_finish
        self._game_over = False

        # carregar fonte pixel
        QFontDatabase.addApplicationFont(FONT_PATH)
        font_title = QFont("Press Start 2P", FONT_PIXEL_BIG_SIZE)
        font_pixel = QFont("Press Start 2P", FONT_PIXEL_SIZE)
        self._font_pixel = font_pixel

        # ==========================
        # LAYOUT PRINCIPAL (HORIZONTAL)
        # ==========================
        layout_main = QHBoxLayout(self)
        layout_main.setContentsMargins(10, 10, 10, 10)
        layout_main.setSpacing(10)

        # ==========================
        # ÁREA ESQUERDA (matriz)
        # ==========================
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

        # grade com a matriz gerada
        grid = QGridLayout()
        grid.setSpacing(4)

        n = len(matriz)
        cell_size = 40 if n <= 12 else 28


        # Estilos de célula
        STYLE_DEFAULT = (
            "QLabel {"
            "background-color: #1a1a24;"
            "color: white;"
            "border: 2px solid #2a2a3a;"
            "border-radius: 6px;"
            "}"
        )
        STYLE_SELECTED = (
            "QLabel {"
            "background-color: #2d3d5a;"
            "color: white;"
            "border: 2px solid #4b6aa8;"
            "border-radius: 6px;"
            "}"
        )
        STYLE_FOUND = (
            "QLabel {"
            "background-color: #2f8f46;"
            "color: white;"
            "border: 2px solid #45c165;"
            "border-radius: 6px;"
            "}"
        )

        # Guardar referência ao contêiner da grade para hit-testing durante o arrasto
        self._esquerda = esquerda

        # Classe de célula clicável
        parent = self

        class CellLabel(QLabel):
            def __init__(self, i, j, letra):
                super().__init__(letra)
                self.i = i
                self.j = j
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setFont(font_pixel)
                self.setFixedSize(cell_size, cell_size)
                self.setStyleSheet(STYLE_DEFAULT)
                self.setMouseTracking(True)

            def enterEvent(self, event):
                if parent._selecting:
                    parent._update_selection(self.i, self.j)
                super().enterEvent(event)

            def mousePressEvent(self, event):
                if event.button() == Qt.MouseButton.LeftButton:
                    parent._start_selection(self.i, self.j)
                super().mousePressEvent(event)

            def mouseReleaseEvent(self, event):
                if parent._selecting:
                    parent._finalize_selection()
                super().mouseReleaseEvent(event)

            def mouseMoveEvent(self, event):
                # Durante o arrasto, calcular qual célula está sob o cursor (mesmo que não seja este label)
                if parent._selecting:
                    global_pos = event.globalPosition().toPoint()
                    local_in_esquerda = parent._esquerda.mapFromGlobal(global_pos)
                    target = parent._esquerda.childAt(local_in_esquerda)
                    if isinstance(target, CellLabel):
                        parent._update_selection(target.i, target.j)
                super().mouseMoveEvent(event)

        # Criar grid de labels
        for i, linha in enumerate(matriz):
            row = []
            for j, letra in enumerate(linha):
                lbl = CellLabel(i, j, letra)
                grid.addWidget(lbl, i, j)
                row.append(lbl)
            self._grid_labels.append(row)

        esquerda_layout.addLayout(grid)
        esquerda.setLayout(esquerda_layout)

        # ==========================
        # ÁREA DIREITA (lista de palavras)
        # ==========================
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

        # Título (usar tamanho menor = FONT_PIXEL_SIZE)
        total = len(palavras_info)
        titulo_palavras = QLabel(f"palavras encontradas: 0/{total}")
        titulo_palavras.setFont(font_pixel)
        titulo_palavras.setStyleSheet("color: white;")
        titulo_palavras.setAlignment(Qt.AlignmentFlag.AlignCenter)
        direita_container_layout.addWidget(titulo_palavras)
        self._titulo_palavras = titulo_palavras

        # ==========================
        # LISTA DE DICAS (ocultas; revelam ao clicar)
        # ==========================
        # Área rolável somente para as dicas
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
        class DicaItem(QLabel):
            def __init__(self, dica_texto: str):
                super().__init__("clique para revelar dica")
                self._dica = dica_texto or "(sem dica)"
                self._revealed = False
                self._locked = False
                self.setFont(font_pixel)
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setWordWrap(True)
                self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.setStyleSheet("""
                    QLabel {
                        background-color: #2a2a3a;
                        color: #cccccc;
                        border-radius: 8px;
                        padding: 10px;
                        border: 1px solid #3a3a4a;
                    }
                """)

            def mousePressEvent(self, event):
                if self._locked:
                    return
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
                else:
                    # opcional: permitir esconder novamente
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
                # Revela e aplica estilo verde (encontrada) e trava
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

        # Mostrar as dicas das palavras (não as palavras) e mapear por palavra
        self._mapa_dicas = {}
        for info in palavras_info:
            dica = info.get('dica', '(sem dica)')
            palavra = info.get('palavra', '')
            item = DicaItem(dica)
            self._dicas_layout.addWidget(item)
            if palavra:
                self._mapa_dicas[palavra] = item

        # preenchimento para empurrar itens para o topo no conteúdo rolável
        self._dicas_layout.addStretch(1)
        # adicionar área rolável à direita
        direita_container_layout.addWidget(scroll, stretch=1)

        # expandir a área direita
        # (stretch final tratado no scroll area)

        # adicionar bloco esquerdo e direito ao layout principal
        layout_main.addWidget(esquerda, stretch=2)
        layout_main.addWidget(direita, stretch=1)

        # Pré-computar mapeamento de coordenadas das palavras (frente e reverso)
        for idx, info in enumerate(self.palavras_info):
            coords = tuple(info.get('posicoes', []))
            if not coords:
                continue
            self._coords_map[coords] = idx
            self._coords_map_rev[tuple(reversed(coords))] = idx

        # dar foco para receber atalhos
        self.setFocus()

    # ==========================
    # Seleção na grade
    # ==========================
    def _start_selection(self, i: int, j: int):
        if (i, j) in self._found_cells:
            return
        self._selecting = True
        self._start_cell = (i, j)
        self._set_temporary_path([(i, j)])

    def _update_selection(self, i: int, j: int):
        if not self._selecting or self._start_cell is None:
            return
        si, sj = self._start_cell
        di = i - si
        dj = j - sj
        # Restringir a 8 direções: horizontal, vertical, diagonais
        if di == 0 and dj == 0:
            path = [(si, sj)]
        elif di == 0:
            step = 1 if dj > 0 else -1
            path = [(si, sj)] + [(si, sj + k) for k in range(step, dj + step, step)]
        elif dj == 0:
            step = 1 if di > 0 else -1
            path = [(si, sj)] + [(si + k, sj) for k in range(step, di + step, step)]
        elif abs(di) == abs(dj):
            stepi = 1 if di > 0 else -1
            stepj = 1 if dj > 0 else -1
            length = abs(di)
            path = [(si + k * stepi, sj + k * stepj) for k in range(0, length + 1)]
        else:
            # fora das 8 direções, ignore
            return
        # garantir limites
        n = len(self.matriz)
        for (pi, pj) in path:
            if pi < 0 or pj < 0 or pi >= n or pj >= n:
                return
        self._set_temporary_path(path)

    def _finalize_selection(self):
        if self._game_over or not self._current_path:
            self._reset_temporary_selection()
            return
        path_tuple = tuple(self._current_path)
        idx = self._coords_map.get(path_tuple)
        if idx is None:
            idx = self._coords_map_rev.get(path_tuple)
        if idx is not None:
            info = self.palavras_info[idx]
            if not info.get('encontrada', False):
                # marcar como encontrada
                info['encontrada'] = True
                for (i, j) in path_tuple:
                    self._found_cells.add((i, j))
                    self._grid_labels[i][j].setStyleSheet(
                        "QLabel {background-color: #2f8f46; color: white; border: 2px solid #45c165; border-radius: 6px;}"
                    )
                # atualizar contador
                self._update_counter()
                # revelar dica correspondente (e travar)
                palavra = info.get('palavra', '')
                dica_item = self._mapa_dicas.get(palavra)
                if dica_item:
                    dica_item.mark_found()
                # checar vitória
                if self._all_found():
                    self._game_over = True
                    self._mostrar_vitoria_e_finalizar()
        # resetar seleção temporária
        self._reset_temporary_selection()

    def _set_temporary_path(self, path):
        # limpar seleção temporária anterior
        self._clear_temp_styles()
        self._current_path = path
        for (i, j) in path:
            if (i, j) in self._found_cells:
                continue
            self._grid_labels[i][j].setStyleSheet(
                "QLabel {background-color: #2d3d5a; color: white; border: 2px solid #4b6aa8; border-radius: 6px;}"
            )

    def _reset_temporary_selection(self):
        self._selecting = False
        self._start_cell = None
        self._current_path = []
        self._clear_temp_styles()

    def _clear_temp_styles(self):
        # volta estilo padrão para não-encontradas
        for i, row in enumerate(self._grid_labels):
            for j, lbl in enumerate(row):
                if (i, j) in self._found_cells:
                    continue
                lbl.setStyleSheet(
                    "QLabel {background-color: #1a1a24; color: white; border: 2px solid #2a2a3a; border-radius: 6px;}"
                )

    def _mostrar_vitoria_e_finalizar(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Vitória!")
        msg.setText("parabens você venceu, sua reconpensa é... absolutamente nada!")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Close)
        btn = msg.button(QMessageBox.StandardButton.Close)
        if btn is not None:
            btn.setText("Fechar")
        # garantir botão de fechar da janela ativo
        msg.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, True)
        msg.setStyleSheet(
            "QMessageBox { background-color: #111018; }"
            "QLabel { color: white; font-family: 'Press Start 2P'; }"
        )
        msg.exec()
        # Após fechar no 'X', volta ao menu principal
        if callable(self._on_finish):
            self._on_finish()
        else:
            self.close()

    def _update_counter(self):
        total = len(self.palavras_info)
        encontrados = sum(1 for p in self.palavras_info if p.get('encontrada'))
        self._titulo_palavras.setText(f"palavras encontradas: {encontrados}/{total}")

    def _all_found(self) -> bool:
        return all(p.get('encontrada') for p in self.palavras_info)

    def _reveal_all_hints(self):
        for item in self._mapa_dicas.values():
            item.reveal(lock=False)

    def _desistir_mark_all_found(self):
        # marcar todas as palavras como encontradas e pintar a matriz
        for info in self.palavras_info:
            if not info.get('encontrada'):
                info['encontrada'] = True
                for (i, j) in info.get('posicoes', []):
                    self._found_cells.add((i, j))
                    self._grid_labels[i][j].setStyleSheet(
                        "QLabel {background-color: #2f8f46; color: white; border: 2px solid #45c165; border-radius: 6px;}"
                    )
                dica_item = self._mapa_dicas.get(info.get('palavra', ''))
                if dica_item:
                    dica_item.mark_found()
        self._update_counter()
        if not self._game_over:
            self._game_over = True
            self._mostrar_vitoria_e_finalizar()

    def show_como_jogar(self):
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

    def keyPressEvent(self, event):
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
            # Voltar ao menu principal
            if callable(self._on_finish):
                self._on_finish()
            else:
                self.close()
            event.accept()
            return
        super().keyPressEvent(event)
