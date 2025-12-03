# Caça-Palavras – Projeto PyQt6

Aplicativo de caça-palavras feito em Python 3.12 com PyQt6. O jogo possui menu inicial, seleção de dificuldade, geração de matriz com palavras em 8 direções, seleção por clique e arrasto, lista de dicas, atalhos de teclado e popup de vitória. Compatível com execução direta em Python e empacotamento via PyInstaller.

## Estrutura do Projeto

```text
consts.py               # Constantes e resolução de caminhos (PyInstaller)
main.py                 # Controlador principal e ciclo de janelas
main_ui.py              # Menu inicial (UI)
README.md               # Este documento
data/palavras.json      # Lista de palavras e dicas
dificult/
  dificult.py           # Lógica de dificuldade (mapeia 1/2/3 → tamanhos)
  dificult_ui.py        # Tela de seleção de dificuldade
```

## Pré‑requisitos

- Python 3.12 (recomendado)
- Windows (testado) e shell `cmd.exe`

Instale dependências:

```cmd
pip install -r requirements.txt
```

Se não houver `requirements.txt`, instale manualmente:

```cmd
pip install PyQt6 pyinstaller
```

## Executando em Desenvolvimento

Na raiz do projeto `c:\github\caca_palavra\jogo_base`:

```cmd
python main.py
```

## Controles do Jogo

- Clique e arraste: seleciona letras em linha reta
- Soltar mouse: valida a palavra selecionada
- `E`: revela todas as dicas
- `D`: desiste e marca todas as palavras como encontradas
- `C`: abre o guia “Como jogar”
- `ESC`: volta ao menu principal

## Estrutura do Projeto

```text
consts.py               # Constantes e resolução de caminhos (PyInstaller)
main.py                 # Controlador principal e ciclo de janelas
main_ui.py              # Menu inicial (UI)
README.md               # Este documento
data/palavras.json      # Lista de palavras e dicas
dificult/
  dificult.py           # Lógica de dificuldade (mapeia 1/2/3 → tamanhos)
  dificult_ui.py        # Tela de seleção de dificuldade
fonts/                  # Fonte "Press Start 2P" (TTF)
game/
  game.py               # Geração da matriz e posicionamento das palavras
  game_ui.py            # Tela do jogo (grade, seleção, dicas, vitória)
```

## Arquitetura e Fluxo

- `main.py` cria e mantém a referência global `janela` (evita que a app feche quando trocar de janela).
- `MenuInicial` (main_ui.py) chama callbacks: jogar/como/sair.
- Ao clicar em “jogar”, abre `DificultUI` com callbacks para dificuldades e um `back_cb` para voltar ao menu.
- Selecionada a dificuldade, `game.abrir_jogo(size)` gera a matriz e `TelaJogo` é exibida.
- Ao finalizar (vitória ou `ESC`), `on_finish` fecha a tela atual e recria `MenuInicial`.

## Empacotar em Executável (.exe)

Exemplo simples com PyInstaller (ajuste caminhos conforme necessário):

```cmd
pyinstaller --noconfirm --onefile --windowed ^
  --add-data "data\palavras.json;data" ^
  --add-data "fonts\PressStart2P-Regular.ttf;fonts" ^
  main.py
```

O projeto usa resolução de caminho em `consts.py` para funcionar tanto no desenvolvimento quanto no executável (detecta `sys._MEIPASS`). Certifique‑se de que os arquivos em `data/` e `fonts/` estejam incluídos com `--add-data`.

Saída esperada: `dist\main.exe`

## Logs e Debug

- Função `log(tag, msg)` centralizada em `consts.py` para rastrear eventos.
- Em caso de erro ao iniciar jogo, o stack trace é impresso no console.

## Dicas de Desenvolvimento

- Evite acoplamento: UI recebe callbacks para ações (abrir jogo, voltar ao menu).
- Use `global janela` dentro de callbacks que trocam de janela (`select_difficulty`, `voltar_menu`).
- Prefira importações “lazy” dentro de callbacks para evitar dependências circulares.

## Problemas Comuns

- Erro “cannot access local variable 'janela'…”: faltou `global janela` dentro da função.
- Recursos não encontrados no `.exe`: confira `--add-data` e a resolução de caminho em `consts.py`.
- Fonte não carrega: verifique `FONT_PATH` e que o TTF foi incluído no build.

## Licença

Projeto educacional. Sem licença explícita; use com bom senso.

