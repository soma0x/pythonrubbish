
from pathlib import Path
import re
import tomllib


PROJECT_DIR = Path(__file__).resolve().parent
INVENTORY_FILE = Path.home() / "savefiles" / "packages-explicit.txt"
MANIFEST_FILE = PROJECT_DIR / "config" / "packages.toml"
OUTPUT_FILE = PROJECT_DIR / "config" / "packages-review.toml"



RULES = {
    "cachyos": [
        "cachyos-", "chwd", "hwdetect",
    ],
    "desktop": [
        "hyprland", "hypridle", "hyprlock", "noctalia",
        "dolphin", "plymouth", "wallpapers",
        "cantarell-fonts", "noto-fonts",
        "awesome-terminal-fonts", "bitstream-vera",
        "ttf-dejavu", "ttf-jetbrains-mono",
        "ttf-liberation", "ttf-meslo-nerd", "ttf-opensans",
    ],
    "shell": [
        "zsh", "fish", "bash-completion",
        "cachyos-fish-config", "cachyos-zsh-config",
        "alacritty", "kitty", "micro", "neovim",
        "nano", "vim", "less", "ripgrep",
        "fastfetch", "btop", "duf", "glances",
    ],
    "development": [
        "base-devel", "git", "python", "nodejs", "npm",
        "pnpm", "go", "uv", "code", "meld",
        "perl", "texinfo", "python-defusedxml",
        "python-packaging", "python-pip",
    ],
    "security": [
        "nmap", "gobuster", "metasploit", "wireshark",
        "openssh", "ufw", "tailscale", "bind",
        "ethtool",
    ],
    "networking": [
        "dnsmasq", "inetutils", "netctl",
        "nss-mdns", "xl2tpd",
    ],
    "storage": [
        "dmraid", "fsarchiver", "hdparm",
        "lsscsi", "mtools", "nilfs-utils",
        "sg3_utils",
    ],
    "maintenance": [
        "cpupower", "diffutils", "logrotate",
        "lsb-release", "pacman-contrib",
        "rebuild-detector", "reflector",
        "rsync", "sysfsutils",
    ],
    "utilities": [
        "fprintd", "hwinfo", "man-db",
        "man-pages", "pkgfile", "plocate",
        "pv", "s-nail", "unrar", "unzip",
        "wget", "which", "xdg-user-dirs",
    ],
    "media-support": [
        "gst-plugin-va", "libgsf",
        "libopenraw", "poppler-glib",
    ],
    "graphics": [
        "mesa", "vulkan", "opencl", "intel-media-driver",
        "vpl-gpu-rt", "lib32-",
    ],
    "audio": [
        "alsa", "pipewire", "wireplumber",
        "gst-plugin-pipewire", "pavucontrol", "sof-firmware",
    ],
    "media": [
        "firefox", "zen-browser", "vlc",
        "ffmpegthumbnailer", "gst-libav",
        "gst-plugins-", "libdvdcss",
    ],
    "gaming": [
        "steam",
    ],
    "system": [
        "base", "linux-", "linux-firmware",
        "intel-ucode", "intel-lpmd", "dmidecode",
        "accountsservice", "bluez", "btrfs",
        "cryptsetup", "device-mapper", "efibootmgr",
        "efitools", "limine", "mkinitcpio",
        "networkmanager", "iwd", "wpa_supplicant",
        "dosfstools", "e2fsprogs", "exfatprogs",
        "f2fs-tools", "jfsutils", "xfsprogs",
        "lvm2", "mdadm", "nfs-utils", "snapper",
        "sudo", "systemd", "modemmanager",
        "usbutils", "usb_modeswitch", "smartmontools",
        "os-prober", "power-profiles-daemon", "realtime-privileges",
    ],
    "package-management": [
        "shelly",
    ],
}



def load_names(path):
    if not path.exists():
        raise FileNotFoundError(path)

    return sorted({
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip()
    })


def load_existing_categories():
    with MANIFEST_FILE.open("rb") as file:
        manifest = tomllib.load(file)

    return {
        package: category
        for category, details in manifest.items()
        for package in details.get("packages", [])
    }


def suggest_category(package):
    name = package.lower()

    for category, keywords in RULES.items():
        if any(keyword in name for keyword in keywords):
            return category

    return "review"


def write_review(packages, existing):
    grouped = {}

    for package in packages:
        category = existing.get(package)

        if category is None:
            category = suggest_category(package)

        grouped.setdefault(category, []).append(package)

    lines = [
        "# IMS suggested package classifications",
        "# Review before using these categories for restoration.",
        "",
    ]

    for category, names in sorted(grouped.items()):
        lines.append(f"[{category}]")
        lines.append("packages = [")

        for name in sorted(names):
            lines.append(f'    "{name}",')

        lines.extend(["]", ""])

    OUTPUT_FILE.write_text("\n".join(lines))
    return grouped


def main():
    packages = load_names(INVENTORY_FILE)
    existing = load_existing_categories()
    grouped = write_review(packages, existing)

    print(f"Inventory: {len(packages)} packages")
    print(f"Review file: {OUTPUT_FILE}")
    print("\nSuggested categories:")

    for category, names in sorted(grouped.items()):
        print(f"  {category}: {len(names)}")

    print("\nNo packages installed. OG manifest is normal")


if __name__ == "__main__":
    main()
