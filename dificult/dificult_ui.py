#aqui vai ficar a segunda tela que de seleção de dificuldade
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase, QFont

from utils.ui import criar_botao
import dificult.dificult as dificult
from consts import FONT_PATH, FONT_PIXEL_SIZE


class DificultUI(QWidget):
    def __init__(self, easy_cb=None, medium_cb=None, hard_cb=None, back_cb=None):
        super().__init__()
        self._back_cb = back_cb
        self.setWindowTitle("Seleção de Dificuldade")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #111018;")

        # carregar fonte pixel (se existir)
        try:
            QFontDatabase.addApplicationFont(FONT_PATH)
            font_pixel = QFont("Press Start 2P", FONT_PIXEL_SIZE)
        except Exception:
            font_pixel = None

        layout = QVBoxLayout(self)

        # centralizar verticalmente: stretch antes
        layout.addStretch(1)

        # Botões de dificuldade (passar callbacks corretamente, sem chamar durante a construção)
        btn_easy = criar_botao("Fácil", easy_cb if easy_cb is not None else (lambda: dificult.bnt_dificult_escolhida(1)), font_pixel)
        layout.addWidget(btn_easy, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_medium = criar_botao("Médio", medium_cb if medium_cb is not None else (lambda: dificult.bnt_dificult_escolhida(2)), font_pixel)
        layout.addWidget(btn_medium, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_hard = criar_botao("Difícil", hard_cb if hard_cb is not None else (lambda: dificult.bnt_dificult_escolhida(3)), font_pixel)
        layout.addWidget(btn_hard, alignment=Qt.AlignmentFlag.AlignCenter)

        bnt_back = criar_botao("Voltar", back_cb if back_cb is not None else (lambda: self.close()), font_pixel)
        layout.addWidget(bnt_back, alignment=Qt.AlignmentFlag.AlignCenter)

        # centralizar verticalmente: stretch depois
        layout.addStretch(1)