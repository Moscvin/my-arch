# my-arch

Instalare Arch Linux + i3 pentru **PC-ul meu**, pas cu pas.

| Componentă | Ce am | Notă |
|---|---|---|
| Placă de bază | ASUS PRIME H610M-R D4 (UEFI) | BIOS = **Del**, meniu boot = **F8** |
| Procesor | Intel Core i5-12400 | `intel-ucode` |
| Placă video | Intel UHD 730 (integrată) | **fără Nvidia**, Mesa + `intel-media-driver` |
| RAM | 16 GB | |
| Disc | NVMe 256 GB | în Linux: **`/dev/nvme0n1`** (NU `/dev/sda`) |
| Rețea | Realtek Ethernet (cablu) | **fără WiFi**, merge direct |
| Monitoare | 2× Acer SA242Y 1920×1080 | puse unul lângă altul automat |

---

## 0. Înainte (încă din Windows)

- [ ] **Salvează tot** ce-ți trebuie de pe C: (Desktop, Documents, Downloads, poze, parole din browser). Discul se șterge complet.
- [ ] Ai un stick cu **Arch Linux ISO** (https://archlinux.org/download/), scris cu Rufus (mod **DD**) sau balenaEtcher.
- [ ] Repo-ul ăsta e urcat pe GitHub-ul tău (ca să-l poți clona după instalare).

## 1. BIOS

1. Repornește și apasă **Del** → intri în BIOS ASUS.
2. **F7** (Advanced Mode) → **Boot → Secure Boot → OS Type: Other OS** (oprește Secure Boot).
3. **Boot → Fast Boot: Disabled** (opțional, dar ajută la stick-uri).
4. **F10** → Save & Exit.

## 2. Pornește de pe stick

1. Bagă stick-ul, repornește, apasă **F8**.
2. Alege **UEFI: Kingston …** (cel cu `UEFI` în față).
3. În meniu: **Arch Linux install medium**. Aștepți promptul `root@archiso ~ #`.

## 3. Verificări în live

```bash
ping -c 3 archlinux.org        # internet pe cablu, trebuie să meargă direct
lsblk                          # discul de ~238G = nvme0n1, stick-ul = sda
```

> ⚠️ **NU rula `cfdisk /dev/sda`**: `sda` e stick-ul de pe care instalezi. Discul tău e `nvme0n1`.
> Nici nu e nevoie de `cfdisk`, archinstall șterge singur discul.

Pacman mai rapid în live (opțional):

```bash
sed -i 's/^#ParallelDownloads.*/ParallelDownloads = 10/' /etc/pacman.conf
```

## 4. archinstall

```bash
archinstall
```

| Opțiune | Ce alegi |
|---|---|
| Archinstall language | English |
| Locales | Keyboard `us`, Language `en_US.UTF-8` (restul le face scriptul) |
| Mirrors | Mirror region: Romania (+ Germany) |
| **Disk configuration** | *Use a best-effort default partition layout* → **`/dev/nvme0n1`** (~238 GB, **NU** Kingston) → `ext4` → separate /home: **No** |
| Swap | True (zram) |
| Bootloader | `systemd-boot` |
| Hostname | ce vrei (ex: `arch-pc`) |
| Root password | o parolă |
| **User account** | adaugă userul tău → **superuser (sudo): Yes** |
| **Profile** | **Minimal** (desktop-ul îl instalează scriptul) |
| Audio | `pipewire` |
| Kernels | `linux` |
| **Additional packages** | `git python` |
| **Network configuration** | *Use NetworkManager* |
| Timezone | `Europe/Chisinau` sau `Europe/Bucharest` |
| Automatic time sync (NTP) | True |

→ **Install**. La final: *chroot into installation?* → **No**.

```bash
reboot
```

Scoate stick-ul când ecranul se stinge.

## 5. Primul login (în consolă, text)

Te loghezi cu userul tău (nu root). Verifică internetul:

```bash
ping -c 3 archlinux.org
```

Dacă nu merge: `sudo systemctl enable --now NetworkManager`.

## 6. Rulează scriptul

```bash
mkdir -p ~/Documents && cd ~/Documents
git clone https://github.com/USERUL-TAU/my-arch.git
cd my-arch
python main.py
```

Nu trebuie `pip` sau `venv`, scriptul folosește doar Python-ul standard.

Meniul:

```
0. Instaleaza TOT (pasii 1-13)
1. Config pacman.conf + oglinzi rapide
2. Pachete de baza
3. Drivere Intel UHD 730
4. Sunet (PipeWire)
5. Desktop i3 + LightDM + configuri
6. Fonturi
7. Aplicatii
8. yay + Google Chrome (AUR)
9. Zsh + Oh My Zsh
10. Neovim
11. nvm + Node LTS
12. Docker
13. Limbi + tastatura us/ro/ru
14. Git + cheie SSH (intreaba nume/email)
```

1. Alege **`0`** (instalează tot). Durează ~15–30 min. Îți cere parola de sudo din când în când.
2. La final scriptul îți arată ce comenzi au dat eroare (dacă au fost). Tot ce s-a întâmplat e în `install.log`.
3. Alege **`14`** → scrii numele și emailul pentru git → îți afișează cheia SSH. Pune-o pe https://github.com/settings/keys.
4. `q`, apoi:

```bash
sudo reboot
```

Poți rula oricând doar anumiți pași, ex: `3 5` sau `12`. Scriptul poate fi rulat de mai multe ori fără probleme (`--needed` sare peste ce e deja instalat; configurile vechi primesc backup `.bak`).

## 7. După reboot

Apare ecranul de login **LightDM** → te loghezi → pornește **i3**.

### Scurtături i3 (`Mod` = tasta Windows)

| Tastă | Ce face |
|---|---|
| `Mod + Enter` | terminal (Alacritty) |
| `Mod + d` | lansator aplicații (rofi) |
| `Mod + Tab` | listă ferestre |
| `Mod + b` | Google Chrome |
| `Mod + e` | Thunar (fișiere) |
| `Mod + q` | închide fereastra |
| `Mod + 1..5` | workspace-uri pe monitorul principal |
| `Mod + 6..0` | workspace-uri pe al doilea monitor |
| `Mod + Shift + 1..0` | mută fereastra pe workspace |
| `Mod + Shift + m` | mută workspace-ul pe celălalt monitor |
| `Mod + h/j/k/l` sau săgeți | focus stânga/jos/sus/dreapta |
| `Mod + f` | fullscreen |
| `Mod + Shift + Space` | fereastră plutitoare |
| `Mod + r` | mod redimensionare |
| `Mod + v` | istoric clipboard (CopyQ) |
| `Mod + .` | emoji |
| `Print` | screenshot (Flameshot) |
| `Mod + Esc` | blochează ecranul |
| `Mod + = / -` | volum |
| `Alt + Shift` | schimbă tastatura us → ro → ru |
| `Mod + Shift + c / r` | reîncarcă / repornește i3 |
| `Mod + Shift + e` | logout |

### Monitoare

Sunt puse automat unul lângă altul (primul = principal, stânga). Dacă sunt invers sau vrei altă rată (Hz):

```bash
arandr                 # le aranjezi cu mouse-ul, Apply
autorandr --save acasa # salvezi; de acum se aplică la fiecare pornire
```

### Stick-uri USB

Se montează automat (`udiskie`, iconiță în bară), inclusiv NTFS/exFAT/FAT32.

### Wallpaper

Pune o poză în `~/.config/wallpaper.jpg` și apasă `Mod + Shift + r`.

### Actualizare sistem

```bash
update     # = yay -Syu
cleanup    # șterge pachete orfane + cache
```

## Ce instalează scriptul

Listele complete sunt în [`packages.py`](packages.py) (toate verificate că există în repo-urile Arch). Pe scurt:

- **Bază:** base-devel, git, intel-ucode, linux-headers, reflector, btop, fastfetch, NTFS/exFAT, udiskie
- **Video:** mesa, vulkan-intel, intel-media-driver (accelerare video hardware)
- **Sunet:** pipewire, wireplumber, pavucontrol, pamixer
- **Desktop:** Xorg, i3, i3status, rofi, LightDM, picom, dunst, alacritty, thunar, arandr, autorandr, copyq, flameshot, nm-applet
- **Fonturi:** Noto (+emoji), JetBrains Mono Nerd, FiraCode Nerd
- **Aplicații:** Firefox, Google Chrome (AUR), Telegram, LibreOffice (+română), mpv, VLC, yazi, lazygit, fzf, ripgrep, zoxide, atuin, tesseract (eng+ron)
- **Dezvoltare:** zsh + Oh My Zsh, Neovim + LazyVim, nvm + Node LTS, Docker
- **Servicii activate:** NetworkManager, LightDM, Docker, fstrim.timer (TRIM pentru NVMe), paccache.timer

Configuri copiate: `configs/` → `~/.config/` (i3, i3status, alacritty, dunst, picom) și `~/.zshrc`.

## Probleme

| Problemă | Soluție |
|---|---|
| Nu bootează de pe stick | Secure Boot oprit? Alegi intrarea cu **UEFI:** în F8? |
| După reboot pornește Windows / nimic | BIOS → Boot → Boot Option #1 = **Linux Boot Manager** |
| Ecran negru după login în LightDM | `Ctrl+Alt+F2` → login → `cat ~/.local/share/xorg/Xorg.0.log` / rulează din nou pasul 5 |
| Nu e sunet | `systemctl --user restart pipewire wireplumber`, apoi `pavucontrol` → alegi ieșirea corectă |
| `docker: permission denied` | logout/login (sau reboot) după pasul 12 |
| Un pachet dă eroare | `sudo pacman -Syu`, apoi rulezi doar pasul respectiv din nou |
