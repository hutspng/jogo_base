from main_ui import MenuInicial
from PyQt6.QtWidgets import QApplication
from dificult.dificult_ui import DificultUI
import dificult.dificult as dificult
import sys
from consts import log

# variaveis globais
janela = None  # referência à janela principal

# funções chamadas pelos botões
def bnt_jogar_clicado():
    log("main", "botão jogar clicado")
    # abrir a janela de seleção de dificuldade e fechar a janela principal
    global janela
    try:
        # criar DificultUI passando callbacks que selecionam a dificuldade
        def select_difficulty(d):
            size = dificult.bnt_dificult_escolhida(d)
            log("main", f"Dificuldade {d} escolhida -> size={size}")
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
        log("main", f"falha ao abrir DificultUI: {e}")

def bnt_como_clicar():
    log("main", "botão como jogar clicado")
    global janela
    if janela:
        janela.show_como_jogar()
    else:
        log("main", "janela principal não está aberta.")


def bnt_sair_clicado():
    log("main", "botão sair clicado")
    sys.exit(0)

def atalho_menu():
    log("main", "ESC pressionado")
    global janela
    if janela:
        janela.show()
    else:
        log("main", "janela principal não está aberta.")


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