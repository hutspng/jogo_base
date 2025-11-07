from main_ui import MenuInicial
from PyQt6.QtWidgets import QApplication
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
    # iniciar o jogo (a implementar)

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