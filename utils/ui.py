"""
UTILS/UI.PY - Utilitários de Interface Gráfica
===============================================
Este módulo contém funções auxiliares para criação de elementos da interface.
Responsável por:
- Padronizar a criação de botões em todo o jogo
- Manter consistência visual entre as telas
- Centralizar estilos CSS dos componentes reutilizáveis
"""

from PyQt6.QtWidgets import QPushButton


def criar_botao(texto, func, font_pixel=None):
    """
    Fábrica de botões padronizados para o jogo Caça Palavras.
    
    Esta função centraliza a criação de botões com estilo consistente em todas as telas,
    aplicando automaticamente cores, tamanhos e comportamentos padronizados.

    Args:
        texto (str): Texto a ser exibido no botão
        func (callable): Função callback a ser executada quando o botão for clicado
                        Se None, nenhuma ação será vinculada
        font_pixel (QFont, optional): Fonte personalizada para aplicar no botão
                                     Se None, usa a fonte padrão do sistema

    Returns:
        QPushButton: Botão configurado e estilizado, pronto para uso

    Características dos botões criados:
    - Tamanho fixo: 260x45 pixels
    - Cor de fundo: laranja (#ff8c00) 
    - Texto: preto
    - Bordas arredondadas (20px de raio)
    - Efeito hover: laranja mais claro (#ffa733)
    - Conecta automaticamente o evento clicked à função fornecida
    """
    # Criar o widget botão com o texto especificado
    btn = QPushButton(texto)
    
    # Aplicar fonte personalizada se fornecida (geralmente fonte pixel do jogo)
    if font_pixel:
        btn.setFont(font_pixel)

    # Definir tamanho fixo para manter consistência visual
    btn.setFixedSize(260, 45)
    
    # Conectar função callback ao evento de clique se fornecida
    if func:
        btn.clicked.connect(func)
    
    # Aplicar estilo CSS padronizado
    btn.setStyleSheet("""
        QPushButton {
            background-color: #ff8c00;  /* Laranja padrão */
            color: black;               /* Texto preto para contraste */
            border-radius: 20px;        /* Bordas arredondadas */
            font-size: 18px;           /* Tamanho da fonte */
        }
        QPushButton:hover {
            background-color: #ffa733;  /* Laranja mais claro no hover */
        }
    """)
    
    return btn