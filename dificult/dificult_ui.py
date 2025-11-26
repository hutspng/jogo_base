"""
DIFICULT/DIFICULT_UI.PY - Interface de Seleção de Dificuldade
=============================================================
Este módulo define a segunda tela do jogo, onde o usuário escolhe o nível de dificuldade.
Responsável por:
- Exibir opções de dificuldade (Fácil, Médio, Difícil)
- Fornecer botão de retorno ao menu principal
- Aplicar tema visual consistente com o resto do jogo
- Implementar injeção de callbacks para cada nível
- Gerenciar layout centralizado dos elementos

Fluxo na aplicação:
Menu Principal → [botão "jogar"] → Seleção Dificuldade → [escolher nível] → Jogo
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase, QFont

from utils.ui import criar_botao
import dificult.dificult as dificult
from consts import FONT_PATH, FONT_PIXEL_SIZE

class DificultUI(QWidget):
    """
    Janela de seleção de dificuldade do jogo.
    
    Implementa o mesmo padrão de injeção de callbacks do menu principal,
    permitindo que a lógica de negócio seja definida externamente.
    """
    
    def __init__(self, easy_cb=None, medium_cb=None, hard_cb=None, back_cb=None):
        """
        Inicializa a tela de seleção de dificuldade.
        
        Args:
            easy_cb (callable): Callback executado quando "Fácil" é escolhido
            medium_cb (callable): Callback executado quando "Médio" é escolhido  
            hard_cb (callable): Callback executado quando "Difícil" é escolhido
            back_cb (callable): Callback executado quando "Voltar" é clicado
            
        Se algum callback não for fornecido, usa comportamento padrão simples.
        """
        super().__init__()
        
        # Armazenar callback de retorno para possível uso futuro
        self._back_cb = back_cb
        
        # ============================================================================
        # CONFIGURAÇÃO DA JANELA
        # ============================================================================
        self.setWindowTitle("Seleção de Dificuldade")
        self.setFixedSize(1280, 720)  # Mesmo tamanho das outras telas para consistência
        self.setStyleSheet("background-color: #111018;")  # Tema escuro consistente

        # ============================================================================
        # CARREGAMENTO DA FONTE PIXEL
        # ============================================================================
        # Tentar carregar fonte pixel com tratamento de erro robusto
        try:
            QFontDatabase.addApplicationFont(FONT_PATH)
            font_pixel = QFont("Press Start 2P", FONT_PIXEL_SIZE)
        except Exception:
            # Se falhar no carregamento, usar fonte padrão do sistema
            font_pixel = None

        # ============================================================================
        # LAYOUT E ORGANIZAÇÃO DOS ELEMENTOS
        # ============================================================================
        layout = QVBoxLayout(self)

        # Centralização vertical: espaço expansível antes dos botões
        layout.addStretch(1)

        # ============================================================================
        # BOTÕES DE SELEÇÃO DE DIFICULDADE
        # ============================================================================
        
        # Botão "Fácil" - matriz 10x10
        # Usa callback injetado ou função padrão que apenas retorna o tamanho
        btn_easy = criar_botao(
            "Fácil", 
            easy_cb if easy_cb is not None else (lambda: dificult.bnt_dificult_escolhida(1)), 
            font_pixel
        )
        layout.addWidget(btn_easy, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botão "Médio" - matriz 15x15
        btn_medium = criar_botao(
            "Médio", 
            medium_cb if medium_cb is not None else (lambda: dificult.bnt_dificult_escolhida(2)), 
            font_pixel
        )
        layout.addWidget(btn_medium, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botão "Difícil" - matriz 20x20
        btn_hard = criar_botao(
            "Difícil", 
            hard_cb if hard_cb is not None else (lambda: dificult.bnt_dificult_escolhida(3)), 
            font_pixel
        )
        layout.addWidget(btn_hard, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botão "Voltar" - retorna ao menu principal
        bnt_back = criar_botao(
            "Voltar", 
            back_cb if back_cb is not None else (lambda: self.close()), 
            font_pixel
        )
        layout.addWidget(bnt_back, alignment=Qt.AlignmentFlag.AlignCenter)

        # Centralização vertical: espaço expansível após os botões
        layout.addStretch(1)