import os
import subprocess
import sys
import shutil
import pexpect


# Colores ANSI
GREEN = "\033[0;32m\033[1m"
RED = "\033[0;31m\033[1m"
YELLOW = "\033[0;33m\033[1m"
END = "\033[0m\033[0m"


def run_command(command, description):
    print(f"\n{YELLOW}[+]{END} {description}")
    result = subprocess.run(command, shell=True, check=False)
    if result.returncode == 0:
        print(f"\n{GREEN}[OK]{END} {description}")
    else:
        print(f"\n{RED}[ERROR]{END} {description}")
        sys.exit(1)


def install_bspwm():
    run_command("sudo apt install libxcb-xinerama0-dev libxcb-icccm4-dev libxcb-randr0-dev libxcb-util0-dev libxcb-ewmh-dev libxcb-keysyms1-dev libxcb-shape0-dev -y", "Instalación de dependencias de bspwm")
    run_command("git clone https://github.com/baskerville/bspwm.git ~/Downloads/bspwm", "Clonando bspwm")
    run_command("git clone https://github.com/baskerville/sxhkd.git ~/Downloads/sxhkd", "Clonando sxhkd")
    run_command("sudo make -C ~/Downloads/bspwm", "Compilando bspwm")
    run_command("sudo make -C ~/Downloads/bspwm install", "Instalando bspwm")
    run_command("which bspwm", "Verificación de la instalación de bspwm")


def install_sxhkd():
    run_command("cd ~/Downloads/sxhkd && sudo make", "Compilando sxhkd")
    run_command("cd ~/Downloads/sxhkd && sudo make install", "Instalando sxhkd")
    run_command("which sxhkd", "Verificación de la instalación sxhkd")


def configure_bspwm_sxhkd():
    print(f"\n{YELLOW}[+]{END} Configurando bspwm y sxhkd...")

    # Crear directorios necesarios
    os.makedirs(os.path.expanduser("~/.config/bspwm"), exist_ok=True)
    os.makedirs(os.path.expanduser("~/.config/sxhkd"), exist_ok=True)

    # Copiar archivos de configuración
    run_command("cp ~/Downloads/bspwm/examples/bspwmrc ~/.config/bspwm/", "Copiando bspwmrc")
    run_command("chmod +x ~/.config/bspwm/bspwmrc", "Haciendo ejecutable bspwmrc")
    run_command("sudo apt install bspwm -y", "Instalando bspwm")
    run_command("cp ~/Downloads/bspwm/examples/sxhkdrc ~/.config/sxhkd/", "Copiando sxhkdrc")

    # Modificar sxhkdrc
    sxhkdrc_path = os.path.expanduser("~/.config/sxhkd/sxhkdrc")
    with open(sxhkdrc_path, "r") as file:
        content = file.read()

    content = content.replace("super + {_,shift + }{h,j,k,l}", "super + {_,shift + }{Left,Down,Up,Right}")
    content = content.replace("super + ctrl + {h,j,k,l}", "super + ctrl + alt + {Left,Down,Up,Right}")
    content = content.replace("super + {h,j,k,l}", "super + alt + shift + {Left,Down,Up,Right}")

    content += "\n# custom resize\nsuper + alt + {Left,Down,Up,Right}\n    ~/.config/bspwm/scripts/bspwm_resize {west,south,north,east}"

    # Eliminar líneas específicas
    lines_to_remove = [
        "# expand a window by moving one of its side outward",
        "super + alt + {h,j,k,l}",
        "	bspc node -z {left -20 0,bottom 0 20,top 0 -20,right 20 0}",
        "# contract a window by moving one of its side inward",
        "super + alt + shift + {h,j,k,l}",
        "	bspc node -z {right -20 0,top 0 20,bottom 0 -20,left 20 0}"
    ]
    
    content = "\n".join([line for line in content.split("\n") if line.strip() not in lines_to_remove])

    with open(sxhkdrc_path, "w") as file:
        file.write(content)

    print(f"{GREEN}[OK]{END} Modificación de sxhkd")

    # Crear script bspwm_resize
    os.makedirs(os.path.expanduser("~/.config/bspwm/scripts"), exist_ok=True)
    resize_script = """#!/usr/bin/env dash

if bspc query -N -n focused.floating > /dev/null; then
    step=20
else
    step=100
fi

case "$1" in
    west) dir=right; falldir=left; x="-$step"; y=0;;
    east) dir=right; falldir=left; x="$step"; y=0;;
    north) dir=top; falldir=bottom; x=0; y="-$step";;
    south) dir=top; falldir=bottom; x=0; y="$step";;
esac

bspc node -z "$dir" "$x" "$y" || bspc node -z "$falldir" "$x" "$y"
"""

    with open(os.path.expanduser("~/.config/bspwm/scripts/bspwm_resize"), "w") as file:
        file.write(resize_script)

    run_command("chmod +x ~/.config/bspwm/scripts/bspwm_resize", "Haciendo ejecutable bspwm_resize")

    # Agregar configuración para VMware
    with open(os.path.expanduser("~/.config/bspwm/bspwmrc"), "a") as file:
        file.write("\nvmware-user-suid-wrapper &\n")

    # Agregar atajo para Firefox
    with open(sxhkdrc_path, "a") as file:
        file.write("\n# open firefox\nsuper + shift + f\n    /usr/bin/firefox\n")

    print(f"{GREEN}[OK]{END} Configuración de bspwm y sxhkd completada")


def install_kitty():
    print(f"\n{YELLOW}[+]{END} Instalando kitty...")

    # Crear directorio para kitty con sudo
    run_command("sudo mkdir -p /opt/kitty", "Creando directorio para kitty")

    # Descargar kitty
    run_command("wget -P ~/Downloads https://github.com/kovidgoyal/kitty/releases/download/v0.34.1/kitty-0.34.1-x86_64.txz", "Descargando kitty")

    # Extraer kitty
    temp_dir = os.path.expanduser("~/Downloads/kitty_temp")
    os.makedirs(temp_dir, exist_ok=True)
    run_command(f"tar -xf ~/Downloads/kitty-0.34.1-x86_64.txz -C {temp_dir}", "Extrayendo kitty")

    # Eliminar archivo comprimido
    os.remove(os.path.expanduser("~/Downloads/kitty-0.34.1-x86_64.txz"))

    # Mover kitty a /opt con sudo
    run_command(f"sudo mv {temp_dir}/* /opt/kitty/", "Moviendo kitty a /opt")
    shutil.rmtree(temp_dir)

    print(f"{GREEN}[OK]{END} Instalación de kitty")

    # Configurar sxhkd para usar kitty
    sxhkdrc_path = os.path.expanduser("~/.config/sxhkd/sxhkdrc")
    with open(sxhkdrc_path, "r") as file:
        content = file.read()
    content = content.replace("urxvt", "/opt/kitty/bin/kitty")
    with open(sxhkdrc_path, "w") as file:
        file.write(content)
    print(f"{GREEN}[OK]{END} Configuración de sxhkd para kitty")

    # Configurar kitty
    kitty_config_dir = os.path.expanduser("~/.config/kitty")
    os.makedirs(kitty_config_dir, exist_ok=True)
    kitty_config = """font_family HackNerdFont
cursor_shape beam

map ctrl+left neighboring_window left
map ctrl+right neighboring_window right
map ctrl+up neighboring_window up
map ctrl+down neighboring_window down

map ctrl+shift+enter new_window_with_cwd
map ctrl+shift+t new_tab_with_cwd

map f1 copy_to_buffer a
map f2 paste_from_buffer a
map f3 copy_to_buffer b
map f4 paste_from_buffer b

map ctrl+shift+z toggle_layout stack
tab_bar_style powerline

inactive_tab_background #e06c75
active_tab_background #98c379
inactive_tab_foreground #000000
tab_bar_margin_color #000000

background_opacity 0.95
"""
    with open(os.path.join(kitty_config_dir, "kitty.conf"), "w") as file:
        file.write(kitty_config)
    print(f"{GREEN}[OK]{END} Configuración de kitty")

    # Crear un enlace simbólico en /usr/local/bin para kitty
    run_command("sudo ln -sf /opt/kitty/bin/kitty /usr/local/bin/kitty", "Creando enlace simbólico para kitty")

    # Copiar configuración para root
    run_command("sudo mkdir -p /root/.config/kitty", "Creando directorio de configuración para root")
    run_command(f"sudo cp {kitty_config_dir}/kitty.conf /root/.config/kitty/", "Copiando configuración de kitty para root")

    print(f"{GREEN}[OK]{END} Instalación y configuración de kitty completada")


def install_zsh():
    run_command("sudo apt install zsh zsh-autosuggestions zsh-syntax-highlighting -y", "Instalación de zsh y plugins")
    run_command(f"sudo usermod --shell /usr/bin/zsh {os.getenv('USER')}", "Configuración de zsh como shell predeterminada para el usuario")
    run_command("sudo usermod --shell /usr/bin/zsh root", "Configuración de zsh como shell predeterminada para root")


def install_fonts():
    print(f"\n{YELLOW}[+]{END} Instalando fuentes...")

    # Descargar Hack Nerd Font
    run_command("sudo wget -P /usr/local/share/fonts https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/Hack.zip", "Descargando Hack Nerd Font")

    # Descomprimir Hack Nerd Font
    run_command("sudo unzip /usr/local/share/fonts/Hack.zip -d /usr/local/share/fonts", "Descomprimiendo Hack Nerd Font")

    # Eliminar archivos innecesarios
    run_command("sudo rm -rf /usr/local/share/fonts/Hack.zip /usr/local/share/fonts/README.md /usr/local/share/fonts/LICENSE.md", "Limpiando archivos innecesarios")

    print(f"{GREEN}[OK]{END} Instalación de Hack Nerd Font")

    # Clonar repositorio blue-sky
    run_command("git clone https://github.com/VaughnValle/blue-sky.git ~/Downloads/blue-sky", "Clonando repositorio blue-sky")

    # Copiar fuentes adicionales
    try:
        for font in os.listdir(os.path.expanduser("~/Downloads/blue-sky/polybar/fonts")):
            shutil.copy2(os.path.join(os.path.expanduser("~/Downloads/blue-sky/polybar/fonts"), font), "/usr/share/fonts/truetype/")
    except Exception as e:
        print(f"{RED}[ERROR]{END} No se pudieron copiar algunas fuentes: {str(e)}")

    # Actualizar cache de fuentes
    run_command("sudo fc-cache -v", "Actualizando cache de fuentes")

    # Limpiar
    shutil.rmtree(os.path.expanduser("~/Downloads/blue-sky"))

    print(f"{GREEN}[OK]{END} Instalación de fuentes adicionales")


def install_powerlevel10k():
    print(f"\n{YELLOW}[+]{END} Instalando powerlevel10k...")

    # Clonar powerlevel10k
    run_command("git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k", "Clonando powerlevel10k")

    # Agregar la fuente al .zshrc
    with open(os.path.expanduser("~/.zshrc"), "a") as zshrc:
        zshrc.write('\nsource ~/powerlevel10k/powerlevel10k.zsh-theme\n')

    print(f"\n{YELLOW}[+]{END} Iniciando configuración interactiva de Powerlevel10k...")

    # Iniciar la configuración interactiva
    child = pexpect.spawn('zsh -c "source ~/powerlevel10k/powerlevel10k.zsh-theme && p10k configure"', encoding='utf-8')
    
    # Configuración según la tabla proporcionada
    configs = [
        ("Prompt Style", "2"),
        ("Character Set", "1"),
        ("Prompt Color", "2"),
        ("Show current time?", "n"),
        ("Prompt Separators", "1"),
        ("Prompt Heads", "3"),
        ("Prompt Tails", "4"),
        ("Prompt Height", "1"),
        ("Prompt Spacing", "2"),
        ("Icons", "2"),
        ("Prompt Flow", "2"),
        ("Enable Transient Prompt?", "y"),
        ("Instant Prompt Mode", "1"),
        ("Apply changes to ~/.zshrc?", "y")
    ]

    for config, choice in configs:
        child.expect_exact(config)
        child.sendline(choice)
        time.sleep(0.5)  # Pequeña pausa para asegurar que la entrada sea procesada

    # Esperar a que termine la configuración
    child.expect(pexpect.EOF, timeout=None)

    print(f"\n{GREEN}[OK]{END} Configuración de Powerlevel10k completada")


def main():
    print(f"\n{YELLOW}[+]{END} Comenzando la personalización del sistema...")
    install_bspwm()
    install_sxhkd()
    configure_bspwm_sxhkd()
    install_kitty()
    install_zsh()
    install_fonts()
    install_powerlevel10k()

if __name__ == "__main__":
    main()
