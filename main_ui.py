"""
MAIN_UI.PY - Interface do Menu Principal
========================================
Este módulo define a tela inicial do jogo Caça Palavras.
Responsável por:
- Exibir o menu principal com título e botões
- Gerenciar atalhos de teclado (C para ajuda, ESC para mostrar janela)
- Mostrar popup de instruções do jogo
- Aplicar tema visual consistente (fundo escuro, fonte pixel)
- Implementar padrão de injeção de dependência para callbacks

Características visuais:
- Fundo escuro (#111018) para tema "gaming"
- Fonte "Press Start 2P" para estética retrô
- Botões centralizados com espaçamento adequado
- Layout responsivo com centralização vertical
"""

from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QMessageBox)
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtCore import Qt
import consts as c
from textwrap import dedent
from utils.ui import criar_botao

class MenuInicial(QWidget):
    """
    Janela principal do menu inicial do jogo.
    
    Implementa padrão de injeção de dependência onde recebe callbacks externos
    em vez de implementar a lógica internamente, permitindo separação entre
    UI e lógica de negócio.
    """
    
    def __init__(self, jogar_cb=None, como_cb=None, sair_cb=None):
        """
        Inicializa o menu principal.
        
        Args:
            jogar_cb (callable): Callback executado quando "jogar" é clicado
            como_cb (callable): Callback executado quando "como jogar" é clicado  
            sair_cb (callable): Callback executado quando "sair" é clicado
            
        Se algum callback não for fornecido, usa comportamento padrão.
        """
        super().__init__()

        # Armazenar callback para uso em atalhos de teclado
        self._como_cb = como_cb

        # Configurar widget para receber eventos de teclado
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # ============================================================================
        # CONFIGURAÇÃO DA JANELA
        # ============================================================================
        self.setWindowTitle("Caça Palavras")
        self.setFixedSize(1280, 720)  # Tamanho fixo para consistência visual
        self.setStyleSheet("background-color: #111018;")  # Fundo escuro tema gaming

        # ============================================================================
        # CARREGAMENTO E CONFIGURAÇÃO DAS FONTES
        # ============================================================================
        # Carregar fonte pixel "Press Start 2P" para estética retrô de videogame
        QFontDatabase.addApplicationFont(c.FONT_PATH)
        font_pixel_big = QFont("Press Start 2P", c.FONT_PIXEL_BIG_SIZE)  # Para títulos
        font_pixel = QFont("Press Start 2P", c.FONT_PIXEL_SIZE)          # Para textos

        # ============================================================================
        # ESTRUTURA DE LAYOUT
        # ============================================================================
        # Layout principal vertical que ocupa toda a janela
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Container interno para centralizar verticalmente o conteúdo
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # ============================================================================
        # ELEMENTOS DA INTERFACE
        # ============================================================================
        
        # Título principal do jogo
        titulo = QLabel("caça palavras")
        titulo.setFont(font_pixel_big)
        titulo.setStyleSheet("color: white")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Texto de instrução sobre atalhos
        desc = QLabel("pressione c para ver os atalhos")
        desc.setFont(font_pixel)
        desc.setStyleSheet("color: white")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)

        # ============================================================================
        # BOTÕES DE AÇÃO
        # ============================================================================
        # Usar função criar_botao para padronização visual
        
        # Botão "Jogar" - inicia o fluxo do jogo
        btn_jogar = criar_botao("jogar", jogar_cb if jogar_cb is not None else (lambda: None), font_pixel)
        layout.addWidget(btn_jogar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botão "Como Jogar" - mostra instruções
        btn_como = criar_botao("como jogar?", como_cb if como_cb is not None else self.show_como_jogar, font_pixel)
        layout.addWidget(btn_como, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botão "Sair" - fecha a aplicação
        btn_sair = criar_botao("sair", sair_cb if sair_cb is not None else self.close, font_pixel)
        layout.addWidget(btn_sair, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # ============================================================================
        # CENTRALIZAÇÃO VERTICAL DO CONTEÚDO
        # ============================================================================
        # Adicionar espaços flexíveis acima e abaixo para centralizar verticalmente
        layout_principal.addStretch(1)      # Espaço expansível acima
        layout_principal.addWidget(container)
        layout_principal.addStretch(1)      # Espaço expansível abaixo

    def show_como_jogar(self):
        """
        Exibe popup modal com instruções detalhadas do jogo.
        
        Mostra informações sobre:
        - Atalhos de teclado disponíveis
        - Regras do jogo
        - Como selecionar palavras
        - Orientações das palavras na matriz
        
        Aplica tema escuro consistente com fonte pixel.
        """
        popup = QMessageBox(self)
        popup.setWindowTitle("Como Jogar")
        popup.setText(dedent("""
        ➡ ATALHOS
        Geral:
        ESC - voltar
        C - abrir esta tela
                             
        Jogo:
        E - exibe todas as dicas no jogo  
        D - desiste do jogo
                             
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

        # Aplicar estilo consistente com o tema do jogo
        popup.setStyleSheet("""
            QMessageBox {
                background-color: #111018;  /* Fundo escuro */
            }
            QMessageBox QLabel {
                color: white;               /* Texto branco */
                font-family: 'Press Start 2P';  /* Fonte pixel */
                font-size: 14px;
            }
            QLabel {
                color: white;
                font-family: 'Press Start 2P';
            }
            QPushButton {
                background-color: #ff8c00;  /* Botão laranja */
                color: black;
                border-radius: 10px;
                padding: 8px 16px;
                font-family: 'Press Start 2P';
            }
            QPushButton:hover {
                background-color: #ffa733;  /* Hover laranja claro */
            }
        """)

        popup.exec()

    def keyPressEvent(self, event):
        """
        Gerencia eventos de teclado para atalhos.
        
        Atalhos implementados:
        - C: Abre popup "Como Jogar"
        - ESC: Traz a janela para frente (caso esteja minimizada)
        
        Args:
            event: Evento de teclado do Qt
        """
        key = event.key()
        
        if key == Qt.Key.Key_C:
            # Tentar usar callback injetada primeiro (separação UI/lógica)
            if self._como_cb is not None:
                try:
                    c.log("main_ui", "atalho C clicado")
                    self._como_cb()
                except Exception:
                    # Se callback falhar, usar método local como fallback
                    c.log("main_ui", "atalho C clicado")
                    self.show_como_jogar()
            else:
                # Se não há callback, usar método local diretamente
                c.log("main_ui", "atalho C clicado")
                self.show_como_jogar()
                
        elif key == Qt.Key.Key_Escape:
            # ESC traz a janela para frente (útil se estiver minimizada)
            c.log("main_ui", "atalho ESC clicado")
            self.show()
            
        else:
            # Delegar outros eventos para o comportamento padrão
            super().keyPressEvent(event)

