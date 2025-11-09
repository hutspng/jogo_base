from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
)
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt
from consts import FONT_PATH, FONT_PIXEL_SIZE, FONT_PIXEL_BIG_SIZE


class TelaJogo(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Caça Palavras - Jogo")
        self.setStyleSheet("background-color: #111018;")
        self.setFixedSize(1280, 720)

        # carregar fonte pixel
        QFontDatabase.addApplicationFont(FONT_PATH)
        font_title = QFont("Press Start 2P", FONT_PIXEL_BIG_SIZE)
        font_pixel = QFont("Press Start 2P", FONT_PIXEL_SIZE)

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
        esquerda_layout.setContentsMargins(0, 0, 0, 0)
        esquerda_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        placeholder_matriz = QLabel("Aqui vai ficar a matriz do caça-palavras")
        placeholder_matriz.setStyleSheet("color: white;")
        placeholder_matriz.setFont(font_pixel)
        esquerda_layout.addWidget(placeholder_matriz)

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

        direita_layout = QVBoxLayout(direita)
        direita_layout.setContentsMargins(30, 20, 30, 20)
        direita_layout.setSpacing(15)

        # Título
        titulo_palavras = QLabel("palavras encontradas: 0/10")
        titulo_palavras.setFont(font_title)
        titulo_palavras.setStyleSheet("color: white;")
        titulo_palavras.setAlignment(Qt.AlignmentFlag.AlignCenter)
        direita_layout.addWidget(titulo_palavras)

        # ==========================
        # LISTA DE PALAVRAS (placeholder)
        # ==========================
        def criar_item_palavra(texto):
            item = QLabel(texto)
            item.setFont(font_pixel)
            item.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setStyleSheet("""
                QLabel {
                    background-color: #ff6347;
                    color: black;
                    border-radius: 8px;
                    padding: 10px;
                }
            """)
            return item

        # exemplo: 5 palavras (você pode alterar)
        for _ in range(5):
            direita_layout.addWidget(
                criar_item_palavra("dica oculta (dica das palavras)")
            )

        # expandir a área direita
        direita_layout.addStretch(1)

        # adicionar bloco esquerdo e direito ao layout principal
        layout_main.addWidget(esquerda, stretch=2)
        layout_main.addWidget(direita, stretch=1)
