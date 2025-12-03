"""
Script para compilar o jogo Caça Palavras em um executável (.exe)
Usa PyInstaller para criar um bundle standalone.
"""
import os
import sys
import subprocess

def build_exe():
    print("=" * 60)
    print("Compilando Caça Palavras (Windows/Linux)")
    print("=" * 60)
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print(f"✓ PyInstaller encontrado (versão {PyInstaller.__version__})")
    except ImportError:
        print("✗ PyInstaller não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller instalado com sucesso")
    
    # Caminhos importantes
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "main.py")
    font_path = os.path.join(script_dir, "fonts", "PressStart2P.ttf")
    data_path = os.path.join(script_dir, "data", "palavras.json")
    icon_path = os.path.join(script_dir, "icon.ico")  # opcional (Windows)

    # Detectar plataforma para ajustar sintaxe do PyInstaller
    is_windows = sys.platform.startswith("win")
    is_linux = sys.platform.startswith("linux")
    
    # Construir comando PyInstaller
    # Ajustar separador do --add-data conforme SO
    sep = ";" if is_windows else ":"

    cmd = [
        "pyinstaller",
        "--onefile",                    # Um único arquivo
        "--windowed",                   # Sem console (GUI)
        "--name=CacaPalavras",          # Nome do executável/app
        f"--add-data={font_path}{sep}fonts",  # Incluir fonte
        f"--add-data={data_path}{sep}data",   # Incluir palavras.json
        "--clean",                      # Limpar cache antes de compilar
    ]
    
    # Adicionar ícone se existir
    if is_windows and os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
        print(f"✓ Ícone encontrado: {icon_path}")
    
    cmd.append(main_script)
    
    print("\nExecutando PyInstaller...")
    print(f"Comando: {' '.join(cmd)}\n")
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "=" * 60)
        print("✓ Compilação concluída com sucesso!")
        print("=" * 60)
        # Caminho do artefato conforme SO
        if is_windows:
            out_path = os.path.join(script_dir, 'dist', 'CacaPalavras.exe')
            print(f"\nExecutável criado em: {out_path}")
            print("\nVocê pode distribuir o arquivo .exe sem precisar do Python instalado.")
        elif is_linux:
            out_path = os.path.join(script_dir, 'dist', 'CacaPalavras')
            print(f"\nBinário criado em: {out_path}")
            print("\nNota: no Linux não há extensão .exe; certifique-se de que o arquivo é executável.")
        else:
            print("\nSaída gerada na pasta 'dist' (plataforma não reconhecida).")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Erro durante a compilação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
