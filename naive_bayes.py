import csv, math, random

def loadCsv(filename):
    data = list(csv.reader(open(filename)))
    try: float(data[0][0])
    except: data.pop(0) # Remove header if present
    return [[float(x) for x in row] for row in data]

def splitData(data, ratio):
    random.seed(1)
    shuffled = list(data)
    random.shuffle(shuffled)
    split_idx = int(len(data) * ratio)
    return shuffled[:split_idx], shuffled[split_idx:]

def separate(data):
    d = {}
    for row in data:
        d.setdefault(row[-1], []).append(row)
    return d

def mean(x): return sum(x)/len(x)

def stdev(x):
    avg = mean(x)
    variance = sum((i-avg)**2 for i in x) / (len(x)-1)
    return math.sqrt(variance)

def summarize(data):
    # zip(*data) transposes rows to columns. [:-1] ignores class label
    return [(mean(col), stdev(col)) for col in zip(*data)][:-1]

def summarizeByClass(data):
    return {c: summarize(rows) for c, rows in separate(data).items()}

def prob(x, m, s):
    if s == 0: return 0
    exponent = math.exp(-(x-m)**2 / (2*s**2))
    return (1 / (math.sqrt(2*math.pi) * s)) * exponent

def predict(summs, row):
    probs = {}
    for c, stats in summs.items():
        probs[c] = 1
        for i, (m, s) in enumerate(stats):
            probs[c] *= prob(row[i], m, s)
    return max(probs, key=probs.get)

def accuracy(test, preds):
    correct = sum(1 for i in range(len(test)) if test[i][-1] == preds[i])
    return correct / len(test) * 100

def main():
    filename = 'diabetes.csv'
    try:
        data = loadCsv(filename)
        train, test = splitData(data, 0.67)
        print(f"Split {len(data)} rows into train={len(train)} and test={len(test)}")
        
        summaries = summarizeByClass(train)
        preds = [predict(summaries, row) for row in test]
        
        print(f"Accuracy: {accuracy(test, preds):.2f}%")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")

if __name__ == "__main__":
    main()


#!/bin/bash

# --- CONFIGURATION ---
# We use a variable so the directory name is always correct.
REPO_NAME="Luno-os"
# ---------------------

# Install necessary packages via pacman
cd $HOME
sudo pacman -S --noconfirm github-cli stow pamixer brightnessctl playerctl ncspot rofi-wayland hyprlock hypridle hyprpaper yazi neovim bottom networkmanager rustup zsh imagemagick acpi pavucontrol

# Backup Existing Config
CONFIG_DIR="$HOME/.config"
DOTFILES_CONFIG="$HOME/$REPO_NAME/.config"
BACKUP_SUFFIX=".bak"

echo "Backing up configuration directories in $CONFIG_DIR based on dotfiles in $DOTFILES_CONFIG"
# Change to the .config folder
cd "$CONFIG_DIR" || { echo "Could not access $CONFIG_DIR"; exit 1; }

# Loop over every directory in the dotfiles repo
for dir in "$DOTFILES_CONFIG"/*/; do
  folder_name=$(basename "$dir")
  if [ -d "$CONFIG_DIR/$folder_name" ]; then
    echo "Backing up directory: $folder_name"
    mv "$CONFIG_DIR/$folder_name" "$CONFIG_DIR/${folder_name}${BACKUP_SUFFIX}"
  else
    echo "Directory $folder_name not found in $CONFIG_DIR; skipping backup"
  fi
done

FILES=(.zshrc .zshenv .tmux.conf .p10k.zsh wallpapers scripts screenshots)

echo "Backing up individual files in $HOME"
for file in "${FILES[@]}"; do
  if [ -f "$HOME/$file" ]; then
    echo "Backing up file: $file"
    mv "$HOME/$file" "$HOME/${file}${BACKUP_SUFFIX}"
  else
    echo "File $file not found; skipping backup"
  fi
done

CACHE_WAL="$HOME/.cache/wal"
CACHE_WAL_BAK="$HOME/.cache/wal.bak"

echo "Checking for $CACHE_WAL..."
if [ -d "$CACHE_WAL" ]; then
  echo "Backing up $CACHE_WAL to $CACHE_WAL_BAK"
  mv "$CACHE_WAL" "$CACHE_WAL_BAK"
else
  echo "$CACHE_WAL not found; skipping..."
fi

echo "Applying dotfiles with stow"
# FIX 1: Point to the correct Repo Name
cd "$HOME/$REPO_NAME" || { echo "Could not access $HOME/$REPO_NAME"; exit 1; }
stow .

# Go back to home directory
cd $HOME

# Install yay (AUR helper)
# FIX 2: Remove existing folder to prevent "already exists" error
rm -rf yay
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si --noconfirm

# Install additional packages via yay
yay -S --noconfirm neofetch cmatrix cava python-pywal ttf-iosevka otf-hermit-nerd gvfs dbus libdbusmenu-glib libdbusmenu-gtk3 gtk-layer-shell brave-bin zoxide eza fzf thefuck jq socat tmux nvm btop hyprshot bluez bluez-utils bluez-obex bluetuith python-gobject 

# Install Powerlevel10k for zsh
yay -S --noconfirm zsh-theme-powerlevel10k-git
echo 'source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme' >> ~/.zshrc

# Eww installation
cd $HOME

# Install Rust
curl --proto '=https' -- tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# FIX 3: Load the cargo environment so we can use it immediately
source "$HOME/.cargo/env"

git clone https://github.com/elkowar/eww
cd eww
cargo build --release --no-default-features --features=wayland
cd target/release
chmod +x ./eww
sudo cp ./eww /usr/local/bin/

# Network Manager setup
sudo systemctl disable systemd-resolved
sudo systemctl disable systemd-networkd
sudo systemctl enable NetworkManager
sudo systemctl start NetworkManager
sudo systemctl enable bluetooth.service
sudo systemctl start bluetooth.service

# Change shell to zsh
chsh -s /usr/bin/zsh

# Reboot the system
echo "Installation complete. The system will now reboot."
sudo reboot
 
