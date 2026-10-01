# Liste de pachete pentru PC-ul meu:
# ASUS PRIME H610M-R D4 | Intel i5-12400 | Intel UHD 730 | 16 GB RAM
# NVMe 256 GB | Realtek Ethernet (fara WiFi) | 2x Acer SA242Y (1920x1080)

BASE = [
    "base-devel", "git", "wget", "curl", "rsync", "openssh",
    "intel-ucode", "linux-firmware", "linux-headers",
    "man-db", "man-pages", "bash-completion",
    "htop", "btop", "fastfetch", "reflector", "pacman-contrib",
    "unzip", "zip", "7zip", "unrar",
    "xdg-user-dirs", "xdg-utils",
    # stick-uri si discuri (NTFS de la Windows, exFAT, FAT32)
    "ntfs-3g", "exfatprogs", "dosfstools", "mtools",
    "udisks2", "udiskie", "gvfs", "gvfs-mtp",
]

# Intel UHD 730 (Alder Lake): Mesa + Vulkan + accelerare video (VA-API)
INTEL_GPU = [
    "mesa", "mesa-utils", "vulkan-intel", "vulkan-tools",
    "intel-media-driver", "libva-utils",
]

AUDIO = [
    "pipewire", "pipewire-pulse", "pipewire-alsa", "wireplumber",
    "pavucontrol", "pamixer", "playerctl",
]

DESKTOP_I3 = [
    # Xorg
    "xorg-server", "xorg-xinit", "xorg-xrandr", "xorg-xinput", "xorg-xset",
    "xorg-xsetroot", "xorg-xprop",
    # i3
    "i3-wm", "i3status", "i3lock", "xss-lock", "dmenu", "rofi",
    # ecran de login
    "lightdm", "lightdm-gtk-greeter",
    # 2 monitoare
    "arandr", "autorandr",
    # utilitare desktop
    "alacritty", "dunst", "libnotify", "picom", "feh",
    "polkit", "polkit-gnome", "gnome-keyring", "network-manager-applet",
    "thunar", "thunar-volman", "thunar-archive-plugin", "tumbler",
    "xclip", "xsel", "copyq", "flameshot", "lxappearance",
]

FONTS = [
    "ttf-dejavu", "noto-fonts", "noto-fonts-emoji", "noto-fonts-cjk",
    "ttf-jetbrains-mono-nerd", "ttf-firacode-nerd", "ttf-nerd-fonts-symbols",
    "awesome-terminal-fonts", "woff2",
]

APPS = [
    "firefox", "telegram-desktop", "libreoffice-fresh", "libreoffice-fresh-ro",
    "mpv", "vlc", "ffmpeg", "imagemagick", "jpegoptim",
    "mousepad", "yazi", "lazygit", "jq", "bat", "lsd", "fd", "ripgrep",
    "fzf", "zoxide", "tldr", "atuin", "entr", "poppler",
    "translate-shell", "tesseract", "tesseract-data-eng", "tesseract-data-ron",
    "rofimoji",
]

# din AUR (prin yay)
AUR = [
    "google-chrome",
]

ZSH = ["zsh", "zsh-autosuggestions", "zsh-syntax-highlighting", "zsh-completions"]

NEOVIM = ["neovim", "python-pynvim", "nodejs", "npm", "tree-sitter-cli"]

DOCKER = ["docker", "docker-compose", "docker-buildx"]

ALL_GROUPS = {
    "BASE": BASE, "INTEL_GPU": INTEL_GPU, "AUDIO": AUDIO,
    "DESKTOP_I3": DESKTOP_I3, "FONTS": FONTS, "APPS": APPS,
    "ZSH": ZSH, "NEOVIM": NEOVIM, "DOCKER": DOCKER,
}
