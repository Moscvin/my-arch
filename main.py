#!/usr/bin/env python3
"""my-arch: configureaza Arch Linux dupa archinstall, pentru PC-ul meu.

Ruleaza ca user normal (NU root):  python main.py
Foloseste doar biblioteca standard Python -> nu trebuie pip / venv.
"""
import getpass
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import packages as pk

ROOT = Path(__file__).resolve().parent
CONFIGS = ROOT / "configs"
HOME = Path.home()
LOG = ROOT / "install.log"

GREEN, BLUE, RED, YELLOW, RESET = "\033[32m", "\033[34m", "\033[31m", "\033[33m", "\033[0m"

failed = []


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now():%H:%M:%S}] {msg}\n")


def info(msg):
    print(f"{BLUE}==> {msg}{RESET}")
    log(msg)


def ok(msg):
    print(f"{GREEN}  ✓ {msg}{RESET}")


def warn(msg):
    print(f"{YELLOW}  ! {msg}{RESET}")
    log("WARN " + msg)


def run(cmd, check=False):
    """Ruleaza o comanda shell. Nu se opreste la eroare, doar o noteaza."""
    print(f"{YELLOW}$ {cmd}{RESET}")
    log("$ " + cmd)
    r = subprocess.run(cmd, shell=True)
    if r.returncode != 0:
        warn(f"eroare ({r.returncode}): {cmd}")
        failed.append(cmd)
        if check:
            sys.exit(1)
    return r.returncode == 0


def pacman(pkgs):
    run("sudo pacman -S --needed --noconfirm " + " ".join(pkgs))


def yay(pkgs):
    if not shutil.which("yay"):
        install_yay()
    run("yay -S --needed --noconfirm " + " ".join(pkgs))


def enable(service, user=False):
    if user:
        run(f"systemctl --user enable --now {service}")
    else:
        run(f"sudo systemctl enable {service}")


def copy_config(src_rel, dst):
    """Copiaza un fisier de config; daca exista deja, face backup .bak."""
    src = CONFIGS / src_rel
    dst = HOME / dst.removeprefix("~/")
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        bak = dst.with_name(dst.name + ".bak")
        shutil.copy2(dst, bak)
        warn(f"{dst} exista -> backup in {bak}")
    shutil.copy2(src, dst)
    ok(f"config: {dst}")


# ---------------------------------------------------------------- pasi

def step_pacman_conf():
    info("Configurare pacman.conf (Color, ParallelDownloads, ILoveCandy) + oglinzi rapide")
    conf = "/etc/pacman.conf"
    run(f"sudo sed -i 's/^#Color/Color/' {conf}")
    run(f"sudo sed -i 's/^#\\?ParallelDownloads.*/ParallelDownloads = 10/' {conf}")
    run(f"grep -q '^ILoveCandy' {conf} || sudo sed -i '/^Color/a ILoveCandy' {conf}")
    pacman(["reflector"])
    run("sudo reflector --country Romania,Moldova,Germany,Poland --protocol https "
        "--age 12 --sort rate --latest 15 --save /etc/pacman.d/mirrorlist")
    run("sudo pacman -Syu --noconfirm")


def step_base():
    info("Pachete de baza (+ intel-ucode, NTFS/exFAT pentru stick-uri)")
    pacman(pk.BASE)
    run("xdg-user-dirs-update")
    enable("fstrim.timer")          # TRIM saptamanal pentru NVMe
    enable("paccache.timer")        # curata cache-ul pacman
    enable("NetworkManager")


def step_intel_gpu():
    info("Drivere video Intel UHD 730")
    pacman(pk.INTEL_GPU)
    # accelerare video hardware in browser / mpv
    env = "/etc/environment"
    run(f"grep -q LIBVA_DRIVER_NAME {env} || echo 'LIBVA_DRIVER_NAME=iHD' | sudo tee -a {env}")


def step_audio():
    info("Sunet: PipeWire")
    pacman(pk.AUDIO)
    enable("pipewire pipewire-pulse wireplumber", user=True)


def step_desktop():
    info("Desktop: Xorg + i3 + LightDM + 2 monitoare")
    pacman(pk.DESKTOP_I3)
    copy_config("i3/config", "~/.config/i3/config")
    copy_config("i3status/config", "~/.config/i3status/config")
    copy_config("alacritty/alacritty.toml", "~/.config/alacritty/alacritty.toml")
    copy_config("dunst/dunstrc", "~/.config/dunst/dunstrc")
    copy_config("picom/picom.conf", "~/.config/picom/picom.conf")
    copy_config("monitors.sh", "~/.config/i3/monitors.sh")
    run("chmod +x ~/.config/i3/monitors.sh")
    run("sudo sed -i 's/^#\\?greeter-session=.*/greeter-session=lightdm-gtk-greeter/' "
        "/etc/lightdm/lightdm.conf")
    enable("lightdm")


def step_fonts():
    info("Fonturi (+ Nerd Fonts pentru terminal si neovim)")
    pacman(pk.FONTS)
    run("fc-cache -f")


def step_apps():
    info("Aplicatii")
    pacman(pk.APPS)


def install_yay():
    if shutil.which("yay"):
        ok("yay e deja instalat")
        return
    info("Instalez yay (AUR helper)")
    pacman(["base-devel", "git"])
    build = HOME / "Downloads" / "yay-bin"
    if build.exists():
        shutil.rmtree(build)
    build.parent.mkdir(parents=True, exist_ok=True)
    run(f"git clone https://aur.archlinux.org/yay-bin.git {build}", check=True)
    run(f"cd {build} && makepkg -si --noconfirm", check=True)


def step_aur():
    info("Pachete din AUR: " + ", ".join(pk.AUR))
    install_yay()
    yay(pk.AUR)


def step_zsh():
    info("Zsh + Oh My Zsh")
    pacman(pk.ZSH)
    if not (HOME / ".oh-my-zsh").exists():
        run('RUNZSH=no CHSH=no KEEP_ZSHRC=yes sh -c "$(curl -fsSL '
            'https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')
    copy_config("zsh/zshrc", "~/.zshrc")
    run(f"sudo chsh -s /usr/bin/zsh {getpass.getuser()}")


def step_neovim():
    info("Neovim (+ LazyVim ca punct de pornire)")
    pacman(pk.NEOVIM)
    nvim = HOME / ".config" / "nvim"
    if nvim.exists():
        warn(f"{nvim} exista deja, nu il ating")
    else:
        run(f"git clone https://github.com/LazyVim/starter {nvim} && rm -rf {nvim}/.git")


def step_nvm():
    info("nvm (Node Version Manager) + Node LTS")
    if not (HOME / ".nvm").exists():
        run("curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh "
            "| PROFILE=/dev/null bash")
    run('bash -c \'export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; '
        'nvm install --lts && nvm alias default "lts/*"\'')


def step_docker():
    info("Docker")
    pacman(pk.DOCKER)
    enable("docker.service")
    run(f"sudo usermod -aG docker {getpass.getuser()}")
    warn("Docker merge fara sudo dupa delogare/reboot")


def step_locale():
    info("Limbi: en_US + ro_RO + ru_RU, tastatura us/ro/ru (Alt+Shift)")
    for loc in ("en_US.UTF-8 UTF-8", "ro_RO.UTF-8 UTF-8", "ru_RU.UTF-8 UTF-8"):
        run(f"sudo sed -i 's/^#{loc}/{loc}/' /etc/locale.gen")
    run("sudo locale-gen")
    # interfata in engleza, dar data/ora/moneda in format romanesc
    run("sudo localectl set-locale LANG=en_US.UTF-8 LC_TIME=ro_RO.UTF-8 "
        "LC_MONETARY=ro_RO.UTF-8 LC_PAPER=ro_RO.UTF-8 LC_MEASUREMENT=ro_RO.UTF-8")
    run('sudo localectl set-x11-keymap us,ro,ru pc105 ",std," grp:alt_shift_toggle')
    run("sudo timedatectl set-ntp true")


def step_git_ssh():
    info("Git + cheie SSH pentru GitHub")
    name = input("  Nume pentru git (ex: Ion Popescu): ").strip()
    email = input("  Email pentru git: ").strip()
    if name:
        run(f'git config --global user.name "{name}"')
    if email:
        run(f'git config --global user.email "{email}"')
    run("git config --global init.defaultBranch main")
    run("git config --global pull.rebase false")
    key = HOME / ".ssh" / "id_ed25519"
    key.parent.mkdir(mode=0o700, exist_ok=True)
    if key.exists():
        ok("cheia SSH exista deja")
    else:
        run(f'ssh-keygen -t ed25519 -C "{email or getpass.getuser()}" -f {key} -N ""')
    print(f"\n{GREEN}Cheia ta publica (pune-o pe https://github.com/settings/keys):{RESET}")
    run(f"cat {key}.pub")


STEPS = [
    ("Config pacman.conf + oglinzi rapide", step_pacman_conf),
    ("Pachete de baza", step_base),
    ("Drivere Intel UHD 730", step_intel_gpu),
    ("Sunet (PipeWire)", step_audio),
    ("Desktop i3 + LightDM + configuri", step_desktop),
    ("Fonturi", step_fonts),
    ("Aplicatii", step_apps),
    ("yay + Google Chrome (AUR)", step_aur),
    ("Zsh + Oh My Zsh", step_zsh),
    ("Neovim", step_neovim),
    ("nvm + Node LTS", step_nvm),
    ("Docker", step_docker),
    ("Limbi + tastatura us/ro/ru", step_locale),
]
# Git/SSH cere date de la tine, de aceea nu intra in "Instaleaza tot"
EXTRA = [("Git + cheie SSH (intreaba nume/email)", step_git_ssh)]


def menu():
    print(f"\n{GREEN}===== my-arch ====={RESET}")
    print(f"  {GREEN}0{RESET}. Instaleaza TOT (pasii 1-{len(STEPS)})")
    for i, (name, _) in enumerate(STEPS + EXTRA, 1):
        print(f"  {i}. {name}")
    print("  q. Iesire")
    return input("\nAlege (ex: 0  sau  1 2 5): ").strip().lower()


def main():
    if os.geteuid() == 0:
        print(f"{RED}Nu rula ca root! Ruleaza ca userul tau: python main.py{RESET}")
        sys.exit(1)
    if not shutil.which("pacman"):
        print(f"{RED}Scriptul e doar pentru Arch Linux.{RESET}")
        sys.exit(1)

    all_steps = STEPS + EXTRA
    while True:
        choice = menu()
        if choice in ("q", ""):
            break
        if choice == "0":
            selected = STEPS
        else:
            try:
                selected = [all_steps[int(x) - 1] for x in choice.replace(",", " ").split()]
            except (ValueError, IndexError):
                print(f"{RED}Optiune invalida{RESET}")
                continue

        run("sudo -v", check=True)  # cere parola o data la inceput
        failed.clear()
        for name, fn in selected:
            fn()
            ok(f"gata: {name}")

        if failed:
            print(f"\n{RED}Comenzi care au dat eroare ({len(failed)}), vezi si {LOG}:{RESET}")
            for c in failed:
                print(f"  - {c}")
        else:
            print(f"\n{GREEN}Totul a mers fara erori.{RESET}")
        if choice == "0":
            print(f"{GREEN}Acum ruleaza optiunea {len(all_steps)} (Git + SSH), apoi: sudo reboot{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOprit.")
