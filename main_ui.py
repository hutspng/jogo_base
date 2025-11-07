import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox)
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt
import consts as c
from textwrap import dedent


class MenuInicial(QWidget):
    def __init__(self, jogar_cb=None, como_cb=None, sair_cb=None):
        super().__init__()

        # guardar callbacks para uso em atalhos/slots
        self._como_cb = como_cb

        # permitir que o widget receba eventos de teclado
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setWindowTitle("Caça Palavras")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #111018;")

        # carregar fonte pixel
        QFontDatabase.addApplicationFont(c.FONT)
        font_pixel_big = QFont("Press Start 2P", c.FONT_PIXEL_BIG_SIZE)
        font_pixel = QFont("Press Start 2P", c.FONT_PIXEL_SIZE)

        # ================================
        # LAYOUT PRINCIPAL
        # ================================
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ================================
        # CONTAINER PARA CONTER TUDO
        # ================================
        container = QWidget()
        layout = QVBoxLayout(container)

        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # ---------- TÍTULO ----------
        titulo = QLabel("caça palavras")
        titulo.setFont(font_pixel_big)
        titulo.setStyleSheet("color: white")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # ---------- DESCRIÇÃO ----------
        desc = QLabel("pressione c para ver os atalhos")
        desc.setFont(font_pixel)
        desc.setStyleSheet("color: white")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)

        # ---------- BOTÕES ----------
        def criar_botao(texto, func):
            btn = QPushButton(texto)
            btn.setFont(font_pixel)
            btn.setFixedSize(260, 45)
            btn.clicked.connect(func)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff8c00;
                    color: black;
                    border-radius: 20px;
                    font-size: 18px;
                }
                QPushButton:hover {
                    background-color: #ffa733;
                }
            """)
            return btn
        
        # criação e definição dos botões
        btn_jogar = criar_botao("jogar", jogar_cb if jogar_cb is not None else (lambda: None))
        layout.addWidget(btn_jogar, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_como = criar_botao("como jogar?", como_cb if como_cb is not None else self.show_como_jogar)
        layout.addWidget(btn_como, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_sair = criar_botao("sair", sair_cb if sair_cb is not None else self.close)
        layout.addWidget(btn_sair, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # CENTRALIZAR O CONTAINER NO MEIO
        layout_principal.addStretch(1)      # espaço acima
        layout_principal.addWidget(container)
        layout_principal.addStretch(1)      # espaço abaixo

    def show_como_jogar(self):
        popup = QMessageBox(self)
        popup.setWindowTitle("Como Jogar")
        popup.setText(dedent("""
        ➡ ATALHOS
        ESC - voltar
        C - abrir esta tela
        E - exibe todas as dicas no jogo  

        ➡ Encontre todas as palavras escondidas no quadro.

        ➡ As palavras podem estar:
        • na horizontal
        • na vertical
        • na diagonal
        • invertidas

        ➡ Clique e arraste para selecionar uma palavra.

        ➡ Encontre todas para vencer!
                    """))

        popup.setIcon(QMessageBox.Icon.Information)

        # estilo do popup (tema escuro + pixel font)
        popup.setStyleSheet("""
            QMessageBox {
                background-color: #111018;
                color: white;
                font-family: 'Press Start 2P';
                font-size: 14px;
            }

            QPushButton {
                background-color: #ff8c00;
                color: black;
                border-radius: 10px;
                padding: 8px 16px;
                font-family: 'Press Start 2P';
            }

            QPushButton:hover {
                background-color: #ffa733;
            }
        """)

        popup.exec()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_C:
            # prefere usar callback injetada (para manter separação lógica/ui)
            if self._como_cb is not None:
                try:
                    self._como_cb()
                except Exception:
                    # se o callback falhar, mostrar diretamente
                    self.show_como_jogar()
            else:
                self.show_como_jogar()
        elif key == Qt.Key.Key_Escape:
            #  ESC volta ao menu
            self.show()
            
        else:
            super().keyPressEvent(event)

