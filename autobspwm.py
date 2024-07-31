import os
import subprocess
import sys

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
    # ... (instalación de kitty como en el script original)
    pass


def install_zsh():
    run_command("sudo apt install zsh zsh-autosuggestions zsh-syntax-highlighting -y", "Instalación de zsh y plugins")
    run_command(f"sudo usermod --shell /usr/bin/zsh {os.getenv('USER')}", "Configuración de zsh como shell predeterminada para el usuario")
    run_command("sudo usermod --shell /usr/bin/zsh root", "Configuración de zsh como shell predeterminada para root")


def install_fonts():
    # ... (instalación de fuentes como en el script original)
    pass


def install_powerlevel10k():
    run_command("git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k", "Clonando powerlevel10k")
    
    # Agregar la fuente al .zshrc
    with open(os.path.expanduser("~/.zshrc"), "a") as zshrc:
        zshrc.write('\nsource ~/powerlevel10k/powerlevel10k.zsh-theme\n')
    
    print(f"\n{YELLOW}[+]{END} Iniciando configuración interactiva de Powerlevel10k...")
    
    # Iniciar la configuración interactiva
    os.system("zsh -c 'source ~/powerlevel10k/powerlevel10k.zsh-theme && p10k configure'")
    
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
