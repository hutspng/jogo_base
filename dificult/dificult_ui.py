#aqui vai ficar a segunda tela que de seleção de dificuldade
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt6.QtCore import Qt

import sys
from utils.ui import criar_botao
import dificult.dificult as dificult

class DificultUI(QWidget):
    def __init__(self, easy_cb=None, medium_cb=None, hard_cb=None):
        super().__init__()
        self.setWindowTitle("Seleção de Dificuldade")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #111018;")

        layout = QVBoxLayout(self)

        # Botões de dificuldade (passar callbacks corretamente, sem chamar durante a construção)
        btn_easy = criar_botao("Fácil", easy_cb if easy_cb is not None else (lambda: dificult.bnt_dificult_escolhida(1)))
        layout.addWidget(btn_easy, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_medium = criar_botao("Médio", medium_cb if medium_cb is not None else (lambda: dificult.bnt_dificult_escolhida(2)))
        layout.addWidget(btn_medium, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_hard = criar_botao("Difícil", hard_cb if hard_cb is not None else (lambda: dificult.bnt_dificult_escolhida(3)))
        layout.addWidget(btn_hard, alignment=Qt.AlignmentFlag.AlignCenter)

        # centralizar
        layout.addStretch(1)