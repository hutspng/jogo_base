# Caça Palavras - Build Instructions

## Como compilar para .exe

### Opção 1: Usando o script automático (Recomendado)

```cmd
python build_exe.py
```

Este script vai:
- Verificar/instalar PyInstaller automaticamente
- Compilar o jogo em um único arquivo .exe
- Incluir todos os recursos necessários (fontes, palavras.json)

### Opção 2: Manualmente com PyInstaller

1. Instalar PyInstaller:
```cmd
pip install pyinstaller
```

2. Compilar:
```cmd
pyinstaller --onefile --windowed --name=CacaPalavras --add-data="fonts\PressStart2P.ttf;fonts" --add-data="data\palavras.json;data" --clean main.py
```

## Linux (Ubuntu/Debian) – Instalação e Build

### Pré‑requisitos

- Python 3.10+ e `pip`
- Ambiente bash (Terminal)

Instalar Python e pip (se necessário):

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

Opcional: criar ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

Instalar dependências e PyInstaller:

```bash
pip install PyQt6 pyinstaller
```

Compilar (note os separadores `:` em `--add-data` no Linux):

```bash
pyinstaller --onefile --windowed \
  --name CacaPalavras \
  --add-data "fonts/PressStart2P.ttf:fonts" \
  --add-data "data/palavras.json:data" \
  --clean main.py
```

Resultado: `dist/CacaPalavras`

### Observações (Linux)

- Em `--add-data`, use `origem:destino` (dois pontos) no Linux e `origem;destino` (ponto e vírgula) no Windows.
- Caminhos são sensíveis a maiúsculas/minúsculas.
- Se houver erro de plugins do Qt, instale pacotes do sistema: `sudo apt install -y libxcb-xinerama0`.
- Fonts: garanta que `PressStart2P.ttf` exista em `fonts/`.

### Resultado

O executável será criado em:
```
dist\CacaPalavras.exe
```

### Notas importantes

- `--onefile`: Cria um único arquivo .exe (mais fácil de distribuir)
- `--windowed`: Sem janela de console (apenas a interface gráfica)
- `--add-data`: Inclui fontes e dados no executável
- O .exe pode ser distribuído sem Python instalado

### Tamanho esperado

O executável terá aproximadamente 20-30 MB devido às dependências PyQt6.

### Troubleshooting

Se houver erro de "módulo não encontrado":
```cmd
pip install PyQt6
```

Se o .exe não abrir, tente compilar sem `--onefile` para ver erros:
```cmd
pyinstaller --windowed --name=CacaPalavras --add-data="fonts\PressStart2P.ttf;fonts" --add-data="data\palavras.json;data" main.py
```
