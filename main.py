"""
MAIN.PY - Controlador Principal do Jogo Caça Palavras
=====================================================
Este é o ponto de entrada e controlador principal da aplicação.
Responsável por:
- Inicializar a aplicação PyQt6
- Gerenciar o fluxo entre as diferentes telas (menu, dificuldade, jogo)
- Manter referência à janela ativa para evitar que a app termine prematuramente
- Implementar a lógica de negócio (callbacks dos botões)
- Coordenar a comunicação entre os módulos de UI e game logic

Arquitetura:
- Usa padrão de injeção de dependência para separar UI da lógica
- Cada tela recebe callbacks em vez de ter lógica acoplada
- Controla o ciclo de vida das janelas (abrir/fechar/alternar)
"""

from main_ui import MenuInicial
from PyQt6.QtWidgets import QApplication
from dificult.dificult_ui import DificultUI
import dificult.dificult as dificult
import sys
from consts import log

# ============================================================================
# ESTADO GLOBAL DA APLICAÇÃO
# ============================================================================
# Mantém referência à janela atualmente ativa para evitar que o Qt termine
# a aplicação quando uma janela é fechada (Qt termina quando não há janelas abertas)
janela = None  # referência à janela principal ativa

# ============================================================================
# CALLBACKS DE AÇÕES DOS BOTÕES (LÓGICA DE NEGÓCIO)
# ============================================================================

def bnt_jogar_clicado():
    """
    Callback executado quando o botão "jogar" é clicado no menu principal.
    Inicia o fluxo de seleção de dificuldade e posterior início do jogo.
    Fluxo:
    1. Cria e exibe a tela de seleção de dificuldade
    2. Define callbacks para cada nível de dificuldade
    3. Fecha o menu principal e mantém referência da nova tela
    """
    log("main", "botão jogar clicado")
    global janela
    try:
        # Função interna que será executada quando uma dificuldade for selecionada
        def select_difficulty(d):
            """
            Callback interno para quando uma dificuldade é escolhida.
            
            Args:
                d (int): Código da dificuldade (1=fácil, 2=médio, 3=difícil)
            """
            global janela  # Necessário para acessar e modificar a variável global
            # Converter código de dificuldade em tamanho da matriz
            size = dificult.bnt_dificult_escolhida(d)
            log("main", f"Dificuldade {d} escolhida -> size={size}")
            
            # Tentar inicializar o jogo
            try:
                # Importações lazy para evitar dependências circulares
                from game import game
                from game.game_ui import TelaJogo
                
                # Gerar matriz do jogo com palavras posicionadas
                matriz, posicoes = game.abrir_jogo(size)
                log("main", f"Jogo iniciado com matriz {size}x{size}")

                # Callback para retornar ao menu quando o jogo terminar
                def voltar_menu():
                    """
                    Callback executado quando o jogo termina (vitória ou ESC).
                    Fecha a tela do jogo e reabre o menu principal.
                    """
                    global janela
                    try:
                        # Fechar janela atual se existir
                        if janela is not None:
                            janela.close()
                        
                        # Recriar menu principal com os mesmos callbacks
                        nova_menu = MenuInicial(
                            jogar_cb=bnt_jogar_clicado,
                            como_cb=bnt_como_clicar,
                            sair_cb=bnt_sair_clicado,
                        )
                        nova_menu.show()
                        janela = nova_menu
                    except Exception as e:
                        log("main", f"Erro ao voltar ao menu: {e}")

                # Criar e exibir tela do jogo
                jogo = TelaJogo(matriz, posicoes, on_finish=voltar_menu)
                jogo.show()
                
                # Fechar tela de dificuldade e atualizar referência
                if janela is not None:
                    janela.close()
                janela = jogo
                return
                
            except Exception as e:
                log("main", f"Erro ao iniciar jogo: {e}")
                import traceback
                traceback.print_exc()
                # Se falhar, não fecha a janela atual para o usuário ver o erro

        # Função para voltar ao menu principal a partir da tela de dificuldade
        def voltar_ao_menu():
            """Volta ao menu principal fechando a tela atual e criando nova instância do menu."""
            global janela
            try:
                # Fechar janela atual (tela de dificuldade)
                if janela is not None:
                    janela.close()
                
                # Recriar menu principal com os mesmos callbacks
                nova_menu = MenuInicial(
                    jogar_cb=bnt_jogar_clicado,
                    como_cb=bnt_como_clicar,
                    sair_cb=bnt_sair_clicado,
                )
                nova_menu.show()
                janela = nova_menu
                log("main", "Retorno ao menu principal realizado com sucesso")
            except Exception as e:
                log("main", f"Erro ao voltar ao menu: {e}")
        
        # Criar tela de seleção de dificuldade com callbacks para cada opção
        nova = DificultUI(
            easy_cb=lambda: select_difficulty(1),    # Callback para fácil
            medium_cb=lambda: select_difficulty(2),  # Callback para médio
            hard_cb=lambda: select_difficulty(3),    # Callback para difícil
            back_cb=voltar_ao_menu,                 # Callback para voltar ao menu
        )
        nova.show()

        # Fechar menu principal e atualizar referência global
        if janela is not None:
            janela.close()
        janela = nova

    except Exception as e:
        log("main", f"falha ao abrir DificultUI: {e}")

def bnt_como_clicar():
    """
    Callback executado quando o botão "como jogar?" é clicado.
    Delega para a janela atual mostrar o popup de instruções.
    """
    log("main", "botão como jogar clicado")
    global janela
    if janela:
        # Chamar método show_como_jogar da janela atual
        janela.show_como_jogar()
    else:
        log("main", "janela principal não está aberta.")

def bnt_sair_clicado():
    """
    Callback executado quando o botão "sair" é clicado.
    Termina a aplicação imediatamente.
    """
    log("main", "botão sair clicado")
    sys.exit(0)

def atalho_menu():
    """
    Callback para atalho ESC - traz a janela atual para frente.
    (Função atualmente não utilizada, mas mantida para compatibilidade)
    """
    log("main", "ESC pressionado")
    global janela
    if janela:
        janela.show()
    else:
        log("main", "janela principal não está aberta.")

# ============================================================================
# PONTO DE ENTRADA DA APLICAÇÃO
# ============================================================================
if __name__ == "__main__":
    # Criar aplicação Qt
    app = QApplication(sys.argv)
    
    # Criar janela principal do menu com injeção de callbacks
    # Isso separa a UI da lógica - a UI não sabe o que fazer, apenas chama os callbacks
    janela = MenuInicial(
        jogar_cb=bnt_jogar_clicado,   # O que fazer quando "jogar" for clicado
        como_cb=bnt_como_clicar,     # O que fazer quando "como jogar" for clicado
        sair_cb=bnt_sair_clicado,    # O que fazer quando "sair" for clicado
    )
    
    # Exibir a janela principal
    janela.show()
    
    # Iniciar loop de eventos do Qt e sair quando a aplicação terminar
    sys.exit(app.exec())