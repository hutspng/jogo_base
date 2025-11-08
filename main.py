from main_ui import MenuInicial
from PyQt6.QtWidgets import QApplication
from dificult.dificult_ui import DificultUI
import dificult.dificult as dificult
import sys


# variaveis globais
log_counter = 0
janela = None  # referência à janela principal

#log de mensagens
def log(msg):
    global log_counter
    log_counter += 1
    print(f"LOG[{log_counter}] {msg}")

# funções chamadas pelos botões
def bnt_jogar_clicado():
    log("botão jogar clicado")
    # abrir a janela de seleção de dificuldade e fechar a janela principal
    global janela
    try:
        # criar DificultUI passando callbacks que selecionam a dificuldade
        def select_difficulty(d):
            size = dificult.bnt_dificult_escolhida(d)
            log(f"Dificuldade {d} escolhida -> size={size}")
            # aqui você pode iniciar o jogo com 'size'
            # fechar a janela de dificuldade (janela global aponta para ela)
            
            global janela
            if janela is not None:
                janela.close()

        nova = DificultUI(
            easy_cb=lambda: select_difficulty(1),
            medium_cb=lambda: select_difficulty(2),
            hard_cb=lambda: select_difficulty(3),
        )
        nova.show()

        # fecha a janela principal (se existir)
        if janela is not None:
            janela.close()
        janela = nova

    except Exception as e:
        log(f"falha ao abrir DificultUI: {e}")

def bnt_como_clicar():
    log("botão como jogar clicado")
    global janela
    if janela:
        janela.show_como_jogar()
    else:
        log("janela principal não está aberta.")


def bnt_sair_clicado():
    log("botão sair clicado")
    sys.exit(0)

def atalho_menu():
    log("ESC pressionado")
    global janela
    if janela:
        janela.show()
    else:
        log("janela principal não está aberta.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # criar a janela injetando callbacks (separação UI <-> lógica)
    janela = MenuInicial(
        jogar_cb=bnt_jogar_clicado,
        como_cb=bnt_como_clicar,
        sair_cb=bnt_sair_clicado,
    )
    janela.show()
    sys.exit(app.exec())