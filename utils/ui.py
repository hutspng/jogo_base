from PyQt6.QtWidgets import QPushButton


def criar_botao(texto, func, font_pixel=None):
    """Cria um botão estilizado para o jogo.

    Args:
        texto (str): Texto do botão
        func (callable): Função chamada quando o botão é clicado
        font_pixel (QFont, optional): Fonte pixel a usar. Se None, usa a fonte padrão.
    """
    btn = QPushButton(texto)
    # aplicar fonte se fornecida
    if font_pixel:
        btn.setFont(font_pixel)

    # comportamento e estilo aplicados sempre
    btn.setFixedSize(260, 45)
    if func:
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